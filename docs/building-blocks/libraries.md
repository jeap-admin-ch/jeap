# Libraries

General-purpose jEAP libraries you add as dependencies to solve a specific concern inside
your own Spring Boot application. For the Maven parents and auto-configuring starters see
[Spring Boot Starters](spring-boot-starters.md); for deployable service templates see
[Reusable Microservices](reusable-microservices.md).

| Library | Purpose | Source |
|---|---|---|
| jeap-audit | Fluent builder API for creating and dispatching audit records (`CreateAuditRecordCommand`), with reliable delivery via the messaging-outbox pattern. | [GitHub](https://github.com/jeap-admin-ch/jeap-audit) |
| jeap-crypto | Utilities for client-side encryption of data-at-rest, with key configuration handled in a secrets-management tool. | [GitHub](https://github.com/jeap-admin-ch/jeap-crypto) |
| jeap-db-schema-publisher | Publishes database schemas to the Architecture Repository at application startup — useful for DB schema documentation and data catalogs. | [GitHub](https://github.com/jeap-admin-ch/jeap-db-schema-publisher) |
| jeap-initializer | Generate ready-to-use codebases for bootstrapping projects, based on existing tested project templates hosted in Git. | [GitHub](https://github.com/jeap-admin-ch/jeap-initializer) |
| jeap-messaging | Messaging based on Avro and Spring Kafka. Eases integration of different Kafka authentication mechanisms and implements the Transactional Outbox pattern as a reusable library. | [GitHub](https://github.com/jeap-admin-ch/jeap-messaging) |
| jeap-messaging-outbox | Implementation of the [Transactional Outbox pattern](https://microservices.io/patterns/data/transactional-outbox.html). | [GitHub](https://github.com/jeap-admin-ch/jeap-messaging-outbox) |
| jeap-messaging-sequential-inbox | Configure the order in which messages are processed in a microservice, independently of the order in which they were received. | [GitHub](https://github.com/jeap-admin-ch/jeap-messaging-sequential-inbox) |
| jeap-opensearch-index-type | Core domain model defining the `IndexType` and `SearchItem` contracts shared by the jEAP OpenSearch building blocks. Pure domain model, zero infrastructure dependencies. | [GitHub](https://github.com/jeap-admin-ch/jeap-opensearch-index-type) |
| jeap-opensearch-searchitem-api | Spring MVC REST API and model exposing indexed search items from OpenSearch (`SearchItemContainer`, `SearchItemsController`, `SearchItemsProvider`). | [GitHub](https://github.com/jeap-admin-ch/jeap-opensearch-searchitem-api) |
| jeap-process-archive-reader | Retrieve an object from the process archive (S3) and convert it directly into the target object. | [GitHub](https://github.com/jeap-admin-ch/jeap-process-archive-reader) |
| jeap-server-sent-events | Send real-time events from server to client using Server-Sent Events (SSE). | [GitHub](https://github.com/jeap-admin-ch/jeap-server-sent-events) |

## Related

- The OpenSearch building blocks span categories: the read-access
  [jeap-opensearch-client-starter](spring-boot-starters.md), the event-driven
  [jeap-opensearch-index-writer-service](reusable-microservices.md), and the
  [index-type-registry Maven plugin](tooling.md).
- [App Building Blocks](index.md) — overview of all categories.
