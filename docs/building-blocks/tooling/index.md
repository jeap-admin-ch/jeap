# Tooling & Registries

Supporting building blocks that are not composed into an application at runtime: the jEAP
CLI, DevOps and pipeline tooling, Maven plugins, migration recipes, and the message/archive
type registries.

## Tooling

| Tool | Purpose | Source |
|---|---|---|
| [jeap-cli](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-cli/) | Command-line tool for interacting with jEAP source-code repositories. Automates tasks such as updating dependencies and migrating to new Java or Spring Boot versions. | [GitHub](https://github.com/jeap-admin-ch/jeap-cli) |
| [jeap-devops-tools](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-devops-tools/) | Supporting tools and documentation for developing, maintaining and operating jEAP-based applications (e.g. OAuth2 login from the command line). | [GitHub](https://github.com/jeap-admin-ch/jeap-devops-tools) |
| [jeap-renovate-presets](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-renovate-presets/) | Composable [Renovate](https://docs.renovatebot.com/) presets for jEAP-based projects, standardizing grouping, approval, versioning, changelog and automerge behaviour for Maven, Docker, npm and GitHub Actions dependencies. | [GitHub](https://github.com/jeap-admin-ch/jeap-renovate-presets) |
| jeap-python-pipeline-lib | Reusable Python modules for CI/CD pipeline operations in a jEAP context. | [GitHub](https://github.com/jeap-admin-ch/jeap-python-pipeline-lib) |

## Maven plugins

| Plugin | Purpose | Source |
|---|---|---|
| [jeap-truststore-maven-plugin](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-truststore-maven-plugin/) | Generates Java trust stores, simplifying certificate management. | [GitHub](https://github.com/jeap-admin-ch/jeap-truststore-maven-plugin) |
| [jeap-central-publishing-maven-plugin](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-central-publishing-maven-plugin/) | Fork of Sonatype's `central-publishing-maven-plugin` that patches HTTP client creation to respect HTTP proxy system properties. Used to publish jEAP artifacts to Maven Central from behind a proxy. | [GitHub](https://github.com/jeap-admin-ch/jeap-central-publishing-maven-plugin) |
| [jeap-opensearch-index-type-registry-maven-plugin](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-opensearch-index-type-registry-maven-plugin/) | Manages an OpenSearch Index Type Registry: validates registry structure and mapping schemas, enforces immutability of existing mappings, and generates per-index-type artifacts (typed Java records, `IndexType` singletons, mapping files). | [GitHub](https://github.com/jeap-admin-ch/jeap-opensearch-index-type-registry-maven-plugin) |

## Auxiliary

| Building block | Purpose | Source |
|---|---|---|
| [jeap-rewrite-recipes](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-rewrite-recipes/) | OpenRewrite recipes for migrating apps based on the jEAP Blueprint Microservices. Used by the [jEAP CLI](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-cli/) to automate Spring Boot / Spring Framework version migrations and other refactorings. | [GitHub](https://github.com/jeap-admin-ch/jeap-rewrite-recipes) |
| [jeap-license-template](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-license-template/) | Template for the Maven License Plugin to generate a Markdown file listing third-party dependency licenses. | [GitHub](https://github.com/jeap-admin-ch/jeap-license-template) |

## Message & archive type registries

Registries holding standardized type definitions used internally by jEAP libraries and
products.

| Registry | Purpose | Source |
|---|---|---|
| [jeap-message-type-registry](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-message-type-registry/) | Defines standardized message types used by jEAP libraries and products. | [GitHub](https://github.com/jeap-admin-ch/jeap-message-type-registry) |
| [jeap-archive-type-registry](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-archive-type-registry/) | Archive type registry used internally (e.g. the Process Snapshot archive type definition). | [GitHub](https://github.com/jeap-admin-ch/jeap-archive-type-registry) |
| [jeap-test-message-type-registry](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-test-message-type-registry/) | Message type registry used internally by jEAP for testing purposes. | [GitHub](https://github.com/jeap-admin-ch/jeap-test-message-type-registry) |

## Related

- [App Building Blocks](../index.md) — overview of all categories.
- [Using jEAP](../../using-jeap.md) — the [CLI](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-cli/) and recipes support dependency and version migrations.
