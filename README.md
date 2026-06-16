# jEAP - Java Enterprise Application Platform

Welcome to the **Java Enterprise Application Platform (jEAP)** umbrella repository. jEAP provides a suite of
libraries and tools designed to assist in developing Java-based software applications based on Spring Boot.
Each jEAP repository addresses specific cross-functional needs, including but not limited to logging, monitoring,
messaging, security and encryption.

## Purpose

The jEAP suite provides developers with a set of ready-to-use solutions for common challenges when developing enterprise
applications using Spring Boot. Building on the blueprint provided by jEAP allows you to focus on business logic and
functionality, with jEAP providing solutions for the reusable cross-functional aspects.

## Documentation

Start here to understand and use jEAP:

- [What is jEAP?](docs/what-is-jeap.md) — definition, core principles, value, and the problems jEAP solves.
- [Using jEAP](docs/using-jeap.md) — the Maven parents and dependency management.
- [App Building Blocks](docs/building-blocks/index.md) — the libraries, starters and microservices you compose from:
  - [Libraries](docs/building-blocks/libraries.md)
  - [Spring Boot Starters](docs/building-blocks/spring-boot-starters.md)
  - [Reusable Microservices](docs/building-blocks/reusable-microservices.md)
  - [Tooling & Registries](docs/building-blocks/tooling.md)

The building-block pages list every jEAP repository with a short description and a link to its source on GitHub.

## License

This repository is Open Source Software licensed under the [Apache License 2.0](./LICENSE).

## Building jEAP

jEAP libraries build from source with the provided Apache Maven Wrapper (`./mvnw install`). Some libraries have
additional requirements such as a specific Java version.
See [Using jEAP — Building from source](docs/using-jeap.md#building-from-source) for details.

## Reporting Security Vulnerabilities

If you would like to report a potential security issue in a jEAP repository, please follow the procedure described in
[SECURITY.md](./SECURITY.md).

## External contributions cannot be accepted currently

At this point in time, jEAP is released as open source software based on the
[EMBAG](https://www.fedlex.admin.ch/eli/cc/2023/682/de) law.

We do not currently accept external contributions. Please refrain from providing code changes or pull requests as we are
unable to accept them.

## Contact

For questions, please contact the maintainers at `jeap-community@bit.admin.ch`.
