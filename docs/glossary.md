# jEAP Glossary

> **Draft for maintainer review.** This glossary explains recurring terms used across the jEAP documentation, especially terms that may be unfamiliar to readers new to jEAP.

## Categories

- **jEAP-specific** — a jEAP component or concept.
- **Industry standard** — an established software or framework term.
- **Swiss Confederation** — terminology from the Swiss federal organisational context.
- **Infrastructure** — a deployment platform or supporting service.

## Glossary

### Agir

**Category:** infrastructure

A task-management service integrated by the Error Handling Service to create manual tasks for permanent message-processing errors. The integration is optional and can be disabled.

### Application

**Category:** industry standard

A software system that provides functionality to its users or other systems. In jEAP documentation, an application is typically built with Spring Boot and may use one or more jEAP building blocks.

### Architecture Repository (ArchRepo)

**Category:** jEAP-specific

A jEAP service that collects and presents information about applications and their architecture, such as interfaces, message contracts, schemas, and deployments.

### BIT / FOITT

**Category:** Swiss Confederation

Bundesamt für Informatik und Telekommunikation (Federal Office of Information Technology, Systems and Telecommunication), the Swiss federal office responsible for IT and telecommunications.

### Building Block

**Category:** jEAP-specific

A reusable part of jEAP, such as a library, Spring Boot starter, reusable microservice, or developer tool.

### Business Process Test (BPT)

**Category:** jEAP-specific

A test that verifies the correct execution of a business process, often using a process engine and test data.

### Business System

**Category:** jEAP-specific

A business solution that may consist of several applications and supporting services.

### jEAP

**Category:** jEAP-specific

The Java Enterprise Application Platform: a collection of open-source libraries, Spring Boot starters, reusable microservices, and tools for building Java enterprise applications.

**See also:** [What is jEAP?](https://jeap-admin-ch.github.io/docs/what-is-jeap)

### Dead Letter Topic (DLT)

**Category:** industry standard

A Kafka topic where messages that cannot be processed successfully are sent for later inspection and handling.

### eIAM

**Category:** Swiss Confederation

The Swiss federal electronic identity and access management system, which provides authentication and authorization services for applications.

### ePortal

**Category:** Swiss Confederation

A Swiss federal web portal that provides access to various e-government services and applications.

### jEAP Library

**Category:** jEAP-specific

Reusable code added to an application's dependencies to provide a capability within that application.

**See also:** [jEAP Libraries](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/)

### jEAP Spring Boot Parent

**Category:** jEAP-specific

A Maven parent that provides dependency versions and build configuration for jEAP applications.

**See also:** [Using jEAP](https://jeap-admin-ch.github.io/docs/using-jeap/)

### jEAP Starter

**Category:** jEAP-specific

A jEAP Spring Boot starter that provides dependencies and configuration for a capability used by an application.

**See also:** [jEAP Spring Boot Starters](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/)

### Key Management System (KMS)

**Category:** infrastructure

A managed service for creating and controlling cryptographic keys. jEAP documentation commonly uses "KMS" when discussing encryption keys, including AWS KMS integrations. KMS is an infrastructure dependency only for configurations that select such a key provider.

**See also:** [jEAP Crypto](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-crypto/)

### Message Contract

**Category:** jEAP-specific

A description of how an application produces or consumes a message type.

**See also:** [jEAP Messaging](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/)

### Message Schema

**Category:** industry standard

A definition of the structure and data types of a message, often written in Avro for jEAP messaging.

### Message Type

**Category:** jEAP-specific

A named kind of message, such as a command or event, with a defined purpose and data structure.

### Oblique

**Category:** Swiss Confederation

The Swiss Confederation's frontend ecosystem for consistent, maintainable user interfaces, including design foundations, libraries, tooling, and a service navigation component. Oblique is a frontend dependency, not a jEAP backend service.

### OpenID Connect (OIDC)

**Category:** industry standard

An identity protocol built on OAuth 2.0 that allows applications to verify a user's identity.

### Quadrel

**Category:** Swiss Confederation

A frontend framework and collection of reusable Angular libraries developed in the BAZG (Bundesamt für Zoll und Grenzsicherheit) for Swiss federal applications. Quadrel is a frontend dependency, not a jEAP backend service.

### RedHat OpenShift (ROHS)

**Category:** infrastructure

A container application platform that provides a Kubernetes-based environment for deploying and managing applications.

### Reusable Microservice

**Category:** jEAP-specific

A ready-made service template that can be configured and deployed as a separate application.

**See also:** [Reusable Microservices](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/)

### Self-Contained System (SCS)

**Category:** industry standard

An independently deployable system that contains the user interface and backend needed for a business capability. In jEAP names and examples, the suffix -scs identifies this deployable type. A frontend and backend packaged as one SCS are one deployment unit.

### Spring Boot Starter

**Category:** industry standard

A dependency that simplifies adding a capability to a Spring Boot application by bringing in related dependencies and configuration.
