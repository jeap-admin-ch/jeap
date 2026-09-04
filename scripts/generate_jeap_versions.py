#!/usr/bin/env python3
"""Generate the jEAP version overview markdown document.

This script clones the latest release tags of the jEAP parent POM and the
configured product repositories, resolves their Maven versions/properties,
and writes a Markdown summary to ``generated-jeap-versions.md`` in the
workspace directory.

It is invoked by the "Fetch versions and generate markdown" step of the
``update_jeap_versions.yml`` GitHub Actions workflow, which provides the
required configuration via environment variables (see ``load_config``
below). Functions in this module can be imported and unit tested without
triggering any network or git operations, since those only happen when
``main()`` is executed.
"""

import json
import os
import re
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


def run(*args, cwd=None):
    subprocess.run(
        args,
        check=True,
        cwd=cwd,
    )


def run_capture(*args, cwd=None):
    completed = subprocess.run(
        args,
        check=True,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def parse_pom_root(root):
    if root.tag.startswith("{"):
        namespace = root.tag[1 : root.tag.find("}")]
        ns = {"m": namespace}
        pref = "m:"
    else:
        ns = {}
        pref = ""

    def find_text(xpath):
        node = root.find(xpath, ns) if ns else root.find(xpath)
        return (node.text or "").strip() if node is not None else ""

    group_id = find_text(f"{pref}groupId")
    if not group_id:
        group_id = find_text(f"{pref}parent/{pref}groupId")

    artifact_id = find_text(f"{pref}artifactId")
    project_version = find_text(f"{pref}version")

    if not project_version:
        project_version = find_text(f"{pref}parent/{pref}version")

    parent_version = find_text(f"{pref}parent/{pref}version")

    parent_group_id = find_text(f"{pref}parent/{pref}groupId")
    parent_artifact_id = find_text(f"{pref}parent/{pref}artifactId")

    properties = {}

    properties_node = (
        root.find(f"{pref}properties", ns) if ns else root.find("properties")
    )

    if properties_node is not None:
        for child in list(properties_node):
            key = child.tag.split("}")[-1]
            properties[key] = (child.text or "").strip()

    return {
        "group_id": group_id,
        "artifact_id": artifact_id,
        "project_version": project_version,
        "parent_group_id": parent_group_id,
        "parent_artifact_id": parent_artifact_id,
        "parent_version": parent_version,
        "properties": properties,
    }


def parse_pom_file(path):
    if not path.is_file():
        raise RuntimeError(f"Missing POM: {path}")

    return parse_pom_root(ET.parse(path).getroot())


def parse_pom_versions(repo_name, tmp_repos):
    pom_path = tmp_repos / repo_name / "pom.xml"
    parsed = parse_pom_file(pom_path)

    return (
        parsed["project_version"],
        parsed["parent_version"],
        parsed["properties"],
    )


def fetch_published_pom(group_id, artifact_id, version):
    group_path = group_id.replace(".", "/")
    url = (
        "https://repo.maven.apache.org/maven2/"
        f"{group_path}/{artifact_id}/{version}/"
        f"{artifact_id}-{version}.pom"
    )

    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")


def resolve_properties(value, properties, source):
    if not value:
        return value

    pattern = re.compile(r"\$\{([^}]+)\}")

    for _ in range(10):
        resolved = pattern.sub(
            lambda match: properties.get(
                match.group(1),
                match.group(0),
            ),
            value,
        )

        if resolved == value:
            break

        value = resolved

    if pattern.search(value):
        raise RuntimeError(f"Unresolved Maven property in {source}: {value}")

    return value


def collect_parent_properties(parent_descriptor, seen=None):
    if seen is None:
        seen = set()

    if not all(parent_descriptor.values()):
        return {}

    parent_key = (
        parent_descriptor["group_id"],
        parent_descriptor["artifact_id"],
        parent_descriptor["version"],
    )
    if parent_key in seen:
        raise RuntimeError("Detected cyclic parent POM reference: " f"{parent_key}")

    seen.add(parent_key)
    pom_xml = fetch_published_pom(*parent_key)
    parent_data = parse_pom_root(ET.fromstring(pom_xml))

    parent_context = dict(parent_data["properties"])
    parent_context.update(
        {
            "project.version": parent_key[2],
            "pom.version": parent_key[2],
        }
    )
    inherited_parent = {
        key: resolve_properties(
            parent_data[f"parent_{key}"],
            parent_context,
            f"{parent_key[1]} parent {key}",
        )
        for key in ("group_id", "artifact_id", "version")
    }

    properties = collect_parent_properties(
        inherited_parent,
        seen,
    )
    properties.update(parent_data["properties"])
    return properties


def collect_dependency_properties(repo_name, project_version, tmp_repos):
    parsed = parse_pom_file(tmp_repos / repo_name / "pom.xml")
    local_properties = dict(parsed["properties"])
    local_properties.update(
        {
            "project.version": project_version,
            "pom.version": project_version,
        }
    )

    parent_descriptor = {
        key: resolve_properties(
            parsed[f"parent_{key}"],
            local_properties,
            f"{repo_name}/pom.xml parent {key}",
        )
        for key in ("group_id", "artifact_id", "version")
    }

    parent_properties = collect_parent_properties(parent_descriptor)
    parent_properties.update(parsed["properties"])
    parent_properties.update(
        {
            "project.version": project_version,
            "pom.version": project_version,
            "project.parent.version": parent_descriptor["version"],
            "parent.version": parent_descriptor["version"],
        }
    )
    return parent_properties


def repository_name_for_component(component_name, repositories_by_component):
    return repositories_by_component.get(
        component_name,
        component_name,
    )


def pom_release_version(version):
    suffix = "-SNAPSHOT"
    return version[: -len(suffix)] if version.endswith(suffix) else version


def changelog_link(repository, version, org, repositories_by_component):
    repo_name = repository_name_for_component(repository, repositories_by_component)

    return (
        f"[Changelog]"
        f"(https://github.com/{org}/{repo_name}"
        f"/blob/v{version}/CHANGELOG.md)"
    )


def latest_release(org, repo):
    remote = f"https://github.com/{org}/{repo}.git"
    tags = run_capture(
        "git",
        "ls-remote",
        "--refs",
        "--tags",
        remote,
    )
    tag_pattern = re.compile(
        r"^v(\d+)\.(\d+)\.(\d+)" r"(?:-([0-9A-Za-z][0-9A-Za-z.-]*))?$"
    )
    releases = []

    for line in tags.splitlines():
        tag = line.rsplit("/", 1)[-1]
        match = tag_pattern.fullmatch(tag)

        if not match:
            continue

        prerelease = match.group(4)
        prerelease_key = ()

        if prerelease:
            prerelease_key = tuple(
                (0, int(part)) if part.isdigit() else (1, part.lower())
                for part in re.split(r"[.-]", prerelease)
            )

        releases.append(
            (
                (
                    int(match.group(1)),
                    int(match.group(2)),
                    int(match.group(3)),
                    1 if prerelease is None else 0,
                    prerelease_key,
                ),
                tag,
                tag[1:],
            )
        )

    if not releases:
        raise RuntimeError(
            f"No v<major>.<minor>.<patch> release tag found " f"for {org}/{repo}"
        )

    _, tag, version = max(releases)
    return tag, version


def clone_latest_release(org, repo, tmp_repos):
    destination = tmp_repos / repo

    if destination.exists():
        raise RuntimeError(f"Repository destination already exists: {destination}")

    tag, version = latest_release(org, repo)
    print(f"Cloning {org}/{repo} release {tag}...")

    run(
        "git",
        "clone",
        "--depth",
        "1",
        "--branch",
        tag,
        f"https://github.com/{org}/{repo}.git",
        str(destination),
    )

    return version


def create_version_rows(included_dependencies, dependency_properties):
    rows = []

    for key, value in dependency_properties.items():
        for dep in included_dependencies:
            if key == f"{dep}.version":
                resolved_value = resolve_properties(
                    value,
                    dependency_properties,
                    f"managed dependency property {key}",
                )

                rows.append(f"| {dep} | `{resolved_value}` |")
                break

    rows.sort()
    return rows


def load_config():
    """Read the workflow-provided environment variables into a config dict."""
    return {
        "workspace": Path(os.environ["GITHUB_WORKSPACE"]),
        "org": os.environ["JEAP_ORG"],
        "product_repositories": json.loads(os.environ["PRODUCT_REPOSITORIES_JSON"]),
        "spring_dependencies": set(json.loads(os.environ["SPRING_DEPENDENCIES_JSON"])),
        "third_party_dependencies": set(
            json.loads(os.environ["THIRD_PARTY_DEPENDENCIES_JSON"])
        ),
        "repositories_by_component": json.loads(
            os.environ["REPOSITORIES_BY_COMPONENT_JSON"]
        ),
    }


def main():
    config = load_config()
    workspace = config["workspace"]
    org = config["org"]
    product_repositories = config["product_repositories"]
    spring_dependencies = config["spring_dependencies"]
    third_party_dependencies = config["third_party_dependencies"]
    repositories_by_component = config["repositories_by_component"]

    tmp_repos = workspace / "_tmp_repos"
    tmp_repos.mkdir(exist_ok=True)

    # ------------------------------------------------------------------
    # jEAP parent
    # ------------------------------------------------------------------

    parent_version = clone_latest_release(org, "jeap-spring-boot-parent", tmp_repos)

    dependency_properties = collect_dependency_properties(
        "jeap-spring-boot-parent",
        parent_version,
        tmp_repos,
    )

    print(f"jEAP parent version: {parent_version}")

    # ------------------------------------------------------------------
    # Product repositories
    # ------------------------------------------------------------------

    versions_by_repo = {}

    for repo in product_repositories:
        project_version = clone_latest_release(org, repo, tmp_repos)

        pom_project_version, product_parent_version, _ = parse_pom_versions(
            repo, tmp_repos
        )

        properties = collect_dependency_properties(
            repo,
            project_version,
            tmp_repos,
        )

        pom_project_version = resolve_properties(
            pom_project_version,
            properties,
            f"{repo}/pom.xml project version",
        )
        product_parent_version = resolve_properties(
            product_parent_version,
            properties,
            f"{repo}/pom.xml parent version",
        )

        if not product_parent_version:
            raise RuntimeError(f"Missing parent version in {repo}/pom.xml")

        if pom_release_version(pom_project_version) != project_version:
            raise RuntimeError(
                f"Latest release tag v{project_version} does not match "
                f"the project version {pom_project_version!r} in "
                f"{repo}/pom.xml"
            )

        versions_by_repo[repo] = {
            "version": project_version,
            "parentVersion": product_parent_version,
        }

    # ------------------------------------------------------------------
    # Generate Markdown
    # ------------------------------------------------------------------

    library_rows = []

    for key, value in dependency_properties.items():
        if (
            key.startswith("jeap-")
            and key.endswith(".version")
            and "maven-plugin" not in key
        ):
            component = key[: -len(".version")]
            repo_name = repository_name_for_component(
                component, repositories_by_component
            )

            resolved_value = resolve_properties(
                value,
                dependency_properties,
                f"jEAP library property {key}",
            )

            library_rows.append(
                f"| {repo_name} | `{resolved_value}` | "
                f"{changelog_link(repo_name, resolved_value, org, repositories_by_component)} |"
            )

    library_rows.sort()

    spring_rows = create_version_rows(spring_dependencies, dependency_properties)

    third_party_rows = create_version_rows(
        third_party_dependencies, dependency_properties
    )

    product_rows = []

    for repo_name in sorted(versions_by_repo):
        data = versions_by_repo[repo_name]

        product_rows.append(
            f"| {repo_name} | "
            f"`{data['version']}` | "
            f"`{data['parentVersion']}` | "
            f"{changelog_link(repo_name, data['version'], org, repositories_by_component)} |"
        )

    parent_changelog = changelog_link(
        "jeap-spring-boot-parent",
        parent_version,
        org,
        repositories_by_component,
    )

    lines = [
        "# jEAP Version Overview",
        "",
        "## jEAP Parent",
        "",
        f"Current Version: `{parent_version}` ({parent_changelog})",
        "",
        "## jEAP Library Versions",
        "",
        "| Component | Current Version | Changelog |",
        "| --- | --- | --- |",
        *library_rows,
        "",
        "## Spring Versions",
        "",
        "Managed Versions of Spring dependencies:",
        "",
        "| Component | Version |",
        "| --- | --- |",
        *spring_rows,
        "",
        "## jEAP Products",
        "",
        "| Component | Current Version | Required jEAP Parent Version | Changelog |",
        "| --- | --- | --- | --- |",
        *product_rows,
        "",
        "## Managed 3rd Party Versions",
        "",
        "Managed Versions of selected 3rd party dependencies:",
        "",
        "| Component | Version |",
        "| --- | --- |",
        *third_party_rows,
    ]

    generated_file = workspace / "generated-jeap-versions.md"

    generated_file.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print(f"Generated markdown: {generated_file}")
    print(
        f"Products: {len(product_rows)}, "
        f"jEAP libraries: {len(library_rows)}, "
        f"Spring dependencies: {len(spring_rows)}, "
        f"third-party dependencies: {len(third_party_rows)}"
    )


if __name__ == "__main__":
    main()
