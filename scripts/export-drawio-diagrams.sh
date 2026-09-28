#!/usr/bin/env bash
#
# Export draw.io diagram sources (*.drawio) in the documentation to SVG images.
#
# Some diagrams in docs/ are maintained as draw.io files with the rendered SVG
# committed next to the source under the same base name (e.g.
# images/foo.drawio -> images/foo.svg). After editing a .drawio file, run this
# script to regenerate the SVG(s) and commit both files.
#
# Usage:
#   scripts/export-drawio-diagrams.sh            # export every *.drawio below docs/
#   scripts/export-drawio-diagrams.sh <path>...  # export the given files or directories
#
# Requires Docker. Uses the rlespinasse/drawio-export image, which runs the
# draw.io desktop application headless. The image is pulled on first use
# (about 1 GB; the download can take a while).
#
# Rules enforced by this script:
#   - A .drawio file holds exactly one page. The exporter names the output of a
#     multi-page file <name>-<page>.svg, which would leave a previously
#     exported <name>.svg stale while the docs keep referencing it.
#   - The exported SVG must be self-contained. An SVG that references an
#     external file or URL is rejected, because an SVG shown through an <img>
#     tag cannot load external resources and the picture would silently be
#     missing on the doc site. Pictures used in a diagram must therefore be
#     embedded in the diagram (draw.io: Edit > Edit Image..., choose the file),
#     not linked by path — the headless exporter does not resolve paths
#     relative to the .drawio file.
#
# Export settings match what draw.io produces by default for an embedded
# diagram: a 10 px border, fonts not embedded (keeps the SVG small; the
# diagrams use the browser's default Helvetica/Arial), light theme, no copy of
# the diagram XML in the SVG (the .drawio file next to it is the source).

set -euo pipefail

# Pinned by digest so that regenerating an unchanged source yields the same SVG
# on every machine. To upgrade, change the tag and digest together (see
# https://hub.docker.com/r/rlespinasse/drawio-export/tags), re-export all
# diagrams and review the rendering.
DEFAULT_IMAGE="rlespinasse/drawio-export:v4.60.0@sha256:2c133c2bbb42ba97fb3c8aca83fd62be3927fef8c7caeba2673d4092b7f6c578"
IMAGE="${DRAWIO_EXPORT_IMAGE:-$DEFAULT_IMAGE}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v docker >/dev/null 2>&1; then
    echo "error: docker is required but not installed" >&2
    exit 1
fi

if [ "$#" -eq 0 ]; then
    set -- "$REPO_ROOT/docs"
fi

# Resolve a path argument to its path relative to the repository root.
relative_path() {
    local path="$1" abs
    if [ -d "$path" ]; then
        abs="$(cd "$path" && pwd)"
    elif [ -f "$path" ]; then
        abs="$(cd "$(dirname "$path")" && pwd)/$(basename "$path")"
    else
        echo "error: $path does not exist" >&2
        exit 1
    fi
    case "$abs" in
        "$REPO_ROOT") echo "." ;;
        "$REPO_ROOT"/*) echo "${abs#"$REPO_ROOT"/}" ;;
        *) echo "error: $path is outside the repository" >&2; exit 1 ;;
    esac
}

# List the .drawio files an argument covers (a file, or a directory searched
# recursively), one per line.
drawio_files() {
    local path="$1"
    if [ -d "$path" ]; then
        find "$path" -type f -name '*.drawio' | sort
    else
        case "$path" in
            *.drawio) echo "$path" ;;
            *) echo "error: $path is not a .drawio file" >&2; exit 1 ;;
        esac
    fi
}

# Fail unless the .drawio file holds exactly one page. A draw.io file is either
# an <mxfile> with one <diagram> element per page, or (as stored by the
# Confluence draw.io plugin) a bare <mxGraphModel>, which is a single page.
check_single_page() {
    local file="$1" pages
    pages="$({ grep -o '<diagram[ >]' "$file" || true; } | wc -l)"
    if [ "$pages" -gt 1 ]; then
        echo "error: $file has $pages pages; keep one diagram page per .drawio file" >&2
        exit 1
    fi
    if [ "$pages" -eq 0 ] && ! grep -q '<mxGraphModel' "$file"; then
        echo "error: $file does not look like a draw.io diagram" >&2
        exit 1
    fi
}

# Fail if an exported SVG references an image that is not embedded.
check_self_contained() {
    local svg="$1" external
    external="$(grep -o '<image[^>]*href="[^"]*"' "$svg" | grep -v 'href="data:' || true)"
    if [ -n "$external" ]; then
        echo "error: $svg references external images, which do not load in the doc site:" >&2
        echo "$external" | sed 's/^/    /' >&2
        echo "Embed the image in the diagram itself (in draw.io: select the shape, Edit > Edit Image..., choose the file) instead of linking a file path or URL." >&2
        exit 1
    fi
}

run_exporter() {
    local rel="$1" status=0
    # The exporter scans the given path recursively and writes <name>.svg next
    # to each <name>.drawio. The repository is mounted at /data so that the
    # relative paths in its output are readable. The headless draw.io
    # application logs harmless fontconfig and D-Bus complaints on every run;
    # they are filtered while the exporter's own exit status is kept.
    docker run --rm \
        --volume "$REPO_ROOT:/data" \
        --user "$(id -u):$(id -g)" \
        --env HOME=/tmp \
        "$IMAGE" \
        --format svg \
        --output . \
        --output-mode relative \
        --remove-page-suffix \
        --embed-svg-fonts false \
        --embed-svg-images \
        --border 10 \
        "$rel" \
        2>&1 | { grep -v -e 'Fontconfig error' -e 'dbus/bus.cc' -e '^[[:space:]]*/' -e '^[[:space:]]*$' || true; } \
        || status=$?
    if [ "$status" -ne 0 ]; then
        echo "error: draw.io export of $rel failed with exit code $status" >&2
        exit "$status"
    fi
}

for path in "$@"; do
    rel="$(relative_path "$path")"
    files="$(drawio_files "$REPO_ROOT/$rel")"
    if [ -z "$files" ]; then
        echo "No .drawio files under $rel"
        continue
    fi
    while IFS= read -r file; do
        check_single_page "$file"
    done <<< "$files"

    echo "Exporting draw.io diagrams under $rel"
    run_exporter "$rel"

    while IFS= read -r file; do
        svg="${file%.drawio}.svg"
        if [ ! -f "$svg" ]; then
            echo "error: expected $svg was not produced" >&2
            exit 1
        fi
        check_self_contained "$svg"
    done <<< "$files"
done
