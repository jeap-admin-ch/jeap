# jEAP Glossary

> **Draft for maintainer review.** This glossary explains recurring terms used across the jEAP documentation, especially terms that may be unfamiliar to readers new to jEAP.

## Categories

- **jEAP-specific** — a jEAP component or concept.
- **industry standard** — an established software or framework term.
- **Swiss Confederation** — terminology or services from the Swiss federal context.
- **infrastructure** — a deployment platform or supporting service.

## Glossary

### Agir

**Category:** Swiss Confederation

A Swiss federal task-management service referenced in the Error Handling Service documentation.

### Apache Avro

**Category:** industry standard

A data serialization system used by jEAP messaging to define message structures.

### Application

**Category:** industry standard

A software system that provides functionality to users or other systems. In jEAP documentation, an application is typically built with Spring Boot and may use jEAP building blocks.

### Architecture Repository (ArchRepo)

**Category:** jEAP-specific

A jEAP service that collects and presents information about application architecture, such as interfaces, message contracts, schemas, and deployments.

### BIT / FOITT

**Category:** Swiss Confederation

Bundesamt für Informatik und Telekommunikation (Federal Office of Information Technology, Systems and Telecommunication), the Swiss federal office that publishes and maintains jEAP.

### Building Block

**Category:** jEAP-specific

A reusable part of jEAP, such as a library, Spring Boot starter, reusable microservice, or developer tool.

### Business Process Test (BPT)

**Category:** jEAP-specific

A test that checks the execution of a business process, often across multiple applications.

### Business System

**Category:** jEAP-specific

A business solution that may consist of multiple applications and supporting services.

### Command

**Category:** industry standard

A message that asks a receiver to perform an action.

### Dead Letter Topic (DLT)

**Category:** industry standard

A Kafka topic to which messages may be sent when normal processing fails.

### eIAM

**Category:** Swiss Confederation

The Swiss federal electronic identity and access management system.

### ePortal

**Category:** Swiss Confederation

A Swiss federal web portal that provides access to e-government services and applications.

### Event

**Category:** industry standard

A message that states that something has happened.

### Event-Driven Architecture (EDA)

**Category:** industry standard

An architectural style in which software components communicate by publishing and consuming events.

### jEAP

**Category:** jEAP-specific

The Java Enterprise Application Platform: a collection of open-source libraries, Spring Boot starters, reusable microservices, and tools for building Java enterprise applications.

**See also:** [What is jEAP?](https://jeap-admin-ch.github.io/docs/what-is-jeap)

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

### Kafka

**Category:** industry standard

An event-streaming platform used by jEAP messaging to publish and consume messages.

### Key Management System (KMS)

**Category:** infrastructure

A service for creating and managing cryptographic keys.

**See also:** [jEAP Crypto](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-crypto/)

### Message Broker

**Category:** industry standard

Infrastructure that receives messages from producers and makes them available to consumers.

### Message Contract

**Category:** jEAP-specific

A description of how an application produces or consumes a message type.

**See also:** [jEAP Messaging](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/)

### Message Schema

**Category:** industry standard

A definition of a message's data structure and field types.

### Message Type

**Category:** jEAP-specific

A named kind of message, such as a command or event, with a defined purpose and structure.

### Message Type Registry

**Category:** jEAP-specific

A registry of standardised jEAP message-type definitions.

### Microservice

**Category:** industry standard

A small, independently deployable application focused on a particular capability.

### OAuth 2.0

**Category:** industry standard

A framework that allows applications to obtain limited access to protected resources.

### Oblique

**Category:** Swiss Confederation

The Swiss Confederation's frontend ecosystem, including design foundations, libraries, and tools.

### OpenID Connect (OIDC)

**Category:** industry standard

An identity protocol built on OAuth 2.0 that allows applications to verify a user's identity.

### Quadrel

**Category:** Swiss Confederation

A frontend framework and set of Angular libraries developed by the Federal Office for Customs and Border Security (BAZG).

### Red Hat OpenShift

**Category:** infrastructure

A Kubernetes-based platform for deploying and managing applications.

### Reusable Microservice

**Category:** jEAP-specific

A ready-made jEAP service template that can be configured and deployed as a separate application.

**See also:** [Reusable Microservices](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/)

### Self-Contained System (SCS)

**Category:** industry standard

An independently deployable system that includes the user interface and backend for a business capability.

### Spring Boot

**Category:** industry standard

A Java framework for building Spring-based applications, used as the application framework for jEAP.

### Spring Boot Starter

**Category:** industry standard

A dependency that simplifies adding a capability to a Spring Boot application by bringing in related dependencies and configuration.
