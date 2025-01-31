# jEAP - Java Enterprise Application Platform

Welcome to the **Java Enterprise Application Platform (jEAP)** umbrella repository. jEAP provides a suite of
libraries and tools designed to assist in developing Java-based software applications based on Spring Boot.
Each jEAP repository addresses specific cross-functional needs, including but not limited to logging, monitoring,
messaging, security and encryption.

## Purpose

The jEAP suite provides developers with a set of ready-to-use solutions for common challenges when developing enterprise
applications using Spring Boot. Building on the blueprint provided by jEAP allows you to focus on business logic and
functionality, with jEAP providing solutions for the reusable cross-functional aspects.

## Getting Started

This umbrella repository is a guide to the individual components of the jEAP suite. We recommend exploring each
repository to understand how it can be applied to your projects.

## License

This repository is Open Source Software licensed under the [Apache License 2.0](./LICENSE).

## Repository List

Here is a list of all the repositories in the jEAP umbrella, along with a brief description of their purpose:

- **[jeap-internal-spring-boot-parent](https://github.com/jeap-admin-ch/jeap-internal-spring-boot-parent)**  
  Internal Spring Boot parent project for jEAP. Manages the Spring Boot version and inherits dependency management for
  common dependencies from Spring Boot. Also provides common Maven Plugin pre-configuration to streamline project setup.
  This parent is mostly used jEAP-internally by jEAP libraries.

- **[jeap-spring-boot-parent](https://github.com/jeap-admin-ch/jeap-spring-boot-parent)**  
  A Maven parent inheriting from `jeap-internal-spring-boot-parent`. Its main purpose is managing the versions of jEAP
  dependencies such as jEAP Starters, jEAP Messaging and jEAP Crypto. This is the Maven parent applications based on jEAP
  should use.

- **[jeap-spring-boot-starters](https://github.com/jeap-admin-ch/jeap-spring-boot-starters)**  
  Contains various Spring Boot starters to simplify application setup and configuration.
  See [jeap-spring-boot-starters/README.md](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/README.md)
  for a full list of the provided starters.

- **[jeap-messaging](https://github.com/jeap-admin-ch/jeap-messaging)**  
  Supports applications by providing messaging functionality based on Avro and Spring Kafka. Also eases integration of
  different Kafka authenthication mechanism, and implements the Transactional Outbox pattern in a re-usable library.

- **[jeap-crypto](https://github.com/jeap-admin-ch/jeap-crypto)**  
  Provides utilities for client-side encryption of data-at-rest.

- **[jeap-truststore-maven-plugin](https://github.com/jeap-admin-ch/jeap-truststore-maven-plugin)**  
  A Maven plugin for generating Java trust stores, making it easy to handle certificate management.

- **[jeap-message-type-registry](https://github.com/jeap-admin-ch/jeap-message-type-registry)**  
  Defines standardized message types used by jEAP libraries and products.

- **[jeap-test-message-type-registry](https://github.com/jeap-admin-ch/jeap-test-message-type-registry)**  
  Message type registry used internally by jEAP for testing purposes.

- **[jeap-bptestagent-api](https://github.com/jeap-admin-ch/jeap-bptestagent-api)**  
  TestAgent API for Business Process Tests

- **[jeap-bptest-orchestrator](https://github.com/jeap-admin-ch/jeap-bptest-orchestrator)**  
  Basic Library for implementing a Business Process Test Orchestrator

- **[jeap-license-template](https://github.com/jeap-admin-ch/jeap-license-template)**  
  Provides a template for
  the [Maven License Plugin](https://www.mojohaus.org/license-maven-plugin/aggregate-add-third-party-mojo.html) to
  generate a markdown file listing third-party dependency licenses.

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
