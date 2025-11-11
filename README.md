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

- **[jeap-archrepo-service](https://github.com/jeap-admin-ch/jeap-archrepo-service)**
  The `jeap-archrepo-service` is a service template library designed to be integrated into applications through simple 
  dependency configuration. This library provides a centralized system for automatically managing and documenting the 
  application architecture inventory.

- **[jeap-audit](https://github.com/jeap-admin-ch/jeap-audit)**
  This library simplifies the process of creating and dispatching audit records by offering a fluent builder API
  for the CreateAuditRecordCommand, ensuring consistent audit record structure across all jEAP-based services.
  The library supports reliable audit record delivery through integration with the messaging-outbox pattern,
  guaranteeing that audit commands are persistently stored and eventually delivered even in the face of system failures.

- **[jeap-bptest-orchestrator](https://github.com/jeap-admin-ch/jeap-bptest-orchestrator)**
  Service providing an orchestrator for business process tests

- **[jeap-bptestagent-api](https://github.com/jeap-admin-ch/jeap-bptestagent-api)**
  TestAgent API for Business Process Tests

- **[jeap-cli](https://github.com/jeap-admin-ch/jeap-cli)**
  A command-line interface (CLI) tool for interacting with source code repositories using jEAP. Automates tasks such 
  as updating dependencies and migrating to new Java or Spring Boot versions.

- **[jeap-crypto](https://github.com/jeap-admin-ch/jeap-crypto)**
  Provides utilities for client-side encryption of data-at-rest.

- **[jeap-db-schema-publisher](https://github.com/jeap-admin-ch/jeap-db-schema-publisher)**  
  Publishes database schemas to the Architecture Repository at startup of a Spring Boot application. This is useful for
  documenting DB schema definitions and creating data catalogs.

- **[jeap-deploymentlog-service](https://github.com/jeap-admin-ch/jeap-deploymentlog-service)**
  Service to trace the deployments of microservice on stages

- **[jeap-error-handling](https://github.com/jeap-admin-ch/jeap-error-handling)**
  Error Handling Service supports error handling patterns for errors, i.e. retry for temporary issues,
  persistence and retry/handling for permanent errors.

- **[jeap-initializer](https://github.com/jeap-admin-ch/jeap-initializer)**
  This library enables generating ready-to-use codebases for bootstrapping projects. It creates code based on existing,
  working and tested project templates hosted in Git repositories.

- **[jeap-internal-spring-boot-parent](https://github.com/jeap-admin-ch/jeap-internal-spring-boot-parent)**
  Internal Spring Boot parent project for jEAP. Manages the Spring Boot version and inherits dependency management for
  common dependencies from Spring Boot. Also provides common Maven Plugin pre-configuration to streamline project setup.
  This parent is mostly used jEAP-internally by jEAP libraries.

- **[jeap-license-template](https://github.com/jeap-admin-ch/jeap-license-template)**
  Provides a template for the [Maven License Plugin](https://www.mojohaus.org/license-maven-plugin/aggregate-add-third-party-mojo.html) to
  generate a markdown file listing third-party dependency licenses.

- **[jeap-message-contract-service](https://github.com/jeap-admin-ch/jeap-message-contract-service)**
  Service to manage messaging contracts used in compatibility checks upon deployment of a service,
  similar to consumer-driven contract testing.

- **[jeap-message-exchange-service](https://github.com/jeap-admin-ch/jeap-message-exchange-service)**
  Service for exchanging incoming and outgoing messages with external parties, using an HTTP-based messagebox API.

- **[jeap-message-type-registry](https://github.com/jeap-admin-ch/jeap-message-type-registry)**
  Defines standardized message types used by jEAP libraries and products.

- **[jeap-messaging](https://github.com/jeap-admin-ch/jeap-messaging)**
  Supports applications by providing messaging functionality based on Avro and Spring Kafka. Also eases integration of
  different Kafka authenthication mechanism, and implements the Transactional Outbox pattern in a re-usable library.

- **[jeap-messaging-outbox](https://github.com/jeap-admin-ch/jeap-messaging-outbox)**
  jEAP Messaging outbox is an implementation of the [Transactional outbox pattern](https://microservices.io/patterns/data/transactional-outbox.html)

- **[jeap-messaging-sequential-inbox](https://github.com/jeap-admin-ch/jeap-messaging-sequential-inbox)**
  The jEAP Sequential Inbox Library allows to configure the order in which messages will be processed in a microservice, which may be different from the order in which the messages were received.

- **[jeap-oauth-mock-server](https://github.com/jeap-admin-ch/jeap-oauth-mock-server)**
  The jEAP OAuth Mock Server provides a configurable OAuth2/OpenID-Connect server for local development and testing.

- **[jeap-process-archive-reader](https://github.com/jeap-admin-ch/jeap-process-archive-reader)**
  This library can be used to retrieve an object from the process archive (S3) and convert it directly into the target object.

- **[jeap-process-archive-service](https://github.com/jeap-admin-ch/jeap-process-archive-service)**
  The jEAP Process Archive Service (PAS) is a service template library that provides a way to archive artifacts pertaining
  to a process. Such artifacts might be required to be archived for audit purposes or due to business requirements.

- **[jeap-archive-type-registry](https://github.com/jeap-admin-ch/jeap-archive-type-registry)**
  Archive type registry used internally by jEAP libraries and products. Contains for example the definition of the
  Process Snapshot archive type.

- **[jeap-process-context-service](https://github.com/jeap-admin-ch/jeap-process-context-service)**
  The jEAP Process Context Service (PCS) is a service template library that provides a way to store and retrieve context 
  information pertaining to a process. This context information might be required to be stored for audit purposes or due
  to business requirements.

- **[jeap-server-sent-events](https://github.com/jeap-admin-ch/jeap-server-sent-events)**
  jEAP server sent events is a library that provides a way to send real-time events from the server to the client using
  Server-Sent Events (SSE). It allows for efficient and scalable communication between the server and the client, enabling    
  real-time updates and notifications.

- **[jeap-spring-boot-config-aws-starter](https://github.com/jeap-admin-ch/jeap-spring-boot-config-aws-starter)**
  Integrates with AWS AppConfig and AWS Secrets Manager.

- **[jeap-spring-boot-db-migration-starter](https://github.com/jeap-admin-ch/jeap-spring-boot-db-migration-starter)**
  Spring Boot starter for running DB migrations as separate jobs (i.e. on k8s).

- **[jeap-spring-boot-parent](https://github.com/jeap-admin-ch/jeap-spring-boot-parent)**
  A Maven parent inheriting from `jeap-internal-spring-boot-parent`. Its main purpose is managing the versions of jEAP
  dependencies such as jEAP Starters, jEAP Messaging and jEAP Crypto. This is the Maven parent applications based on jEAP
  should use.

- **[jeap-spring-boot-starters](https://github.com/jeap-admin-ch/jeap-spring-boot-starters)**
  Contains various Spring Boot starters to simplify application setup and configuration.
  See [jeap-spring-boot-starters/README.md](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/README.md)
  for a full list of the provided starters.

- **[jeap-spring-boot-tls-starter](https://github.com/jeap-admin-ch/jeap-spring-boot-tls-starter)**
  Activates TLS on the Spring Boot webserver, and provides the option to generate a certificate at startup (suitable for 
  encrytion beetn AWS ALB and the Spring Boot app).

- **[jeap-spring-boot-roles-anywhere-starter](https://github.com/jeap-admin-ch/jeap-spring-boot-roles-anywhere-starter)**
  Java library for seamless integration with AWS IAM Roles Anywhere in Spring Boot. 
  Enables secure, certificate-based credentials without external helper tools.

- **[jeap-test-message-type-registry](https://github.com/jeap-admin-ch/jeap-test-message-type-registry)**
  Message type registry used internally by jEAP for testing purposes.

- **[jeap-truststore-maven-plugin](https://github.com/jeap-admin-ch/jeap-truststore-maven-plugin)**
  A Maven plugin for generating Java trust stores, making it easy to handle certificate management.

## Building jEAP

To build jEAP libraries from source, you will usually be able to start a build using the provided Apache Maven Wrapper
script in the repository. The following command will build the project, run all tests and install the library
in your local Apache Maven repository:

```shell
./mvnw install
```
Note that jEAP libraries may have additional build requirements, such as specific Java versions. Please refer to the
individual repository's README.md or pom.xml for more information.

### Confluent Maven Repository

jeap-messaging libraries that serialize/deserialize Kafka records using a Confluent Avro Schema Registry require 
dependencies from the Confluent Maven Repository. To build these libraries, you need to configure the Confluent 
repository either in your Maven settings.xml or locally in the repository's pom.xml. For more information, please refer 
to the [Maven documentation](https://maven.apache.org/guides/mini/guide-multiple-repositories.html) and the
[Confluent Java Client documentation](https://docs.confluent.io/kafka-clients/java/current/overview.html#java-installation).

```xml
<repositories>
        <repository>
            <id>confluent</id>
            <url>https://packages.confluent.io/maven/</url>
        </repository>
</repositories>
```

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
