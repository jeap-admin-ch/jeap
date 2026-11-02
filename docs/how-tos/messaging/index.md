# How-Tos: Messaging

Kafka, message types, contracts and registries, the transactional outbox, error handling, and process
archiving/context tracking.

## Kafka

- [Integrate Kafka into a service](integrate-kafka-into-a-service.md) — an end-to-end checklist from message type to deployed consumer/producer.
- [Connect a service to multiple Kafka clusters](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/configuration#clusters) — hybrid-cloud setups, e.g. on-prem + AWS MSK.
- [Declare message contracts](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/message-contracts) — the annotations a producer/consumer must declare.
- [Use the idempotent message handler](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/idempotent-message-handler) — `@IdempotentMessageHandler`, for consumers that must tolerate at-least-once delivery.
- [Install all message types of a program locally](../../concepts/messaging/message-type-registry/installing-message-types-locally.md) — resolve a Message Type Registry's generated classes into your local Maven repository.
- Set up a Message/Archive Type Registry for a program — [Message Type Registry getting started](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-message-type-registry/getting-started), [Archive Type Registry getting started](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-archive-type-registry/getting-started).

## Message evolution

- [Apply EMC Message Evolution to a Kafka message type](apply-emc-message-evolution.md) — evolve an incompatible change through compatible steps instead of a new major version.
- [Evolve a message type consumed by its own producer](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/message-evolution#self-messages) — the extra steps needed when a service produces and consumes the same message type (jEAP Messaging 7.5.0+).

## Outbox, error handling & process services

- [Send a Kafka message within a database transaction](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging-outbox/getting-started) via the transactional outbox pattern.
- Set up an Error Handling Service instance ([jeap-error-handling](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-error-handling/getting-started)) — topics, consumer config, authorization, Agir/Jira hookup.
  - [Implement a custom resending strategy / task factory / Kafka back-off](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-error-handling/customization).
  - [Build, run and test the Error Handling Service library locally](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-error-handling/development).
- [Set up a Process Context Service instance](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-process-context-service/getting-started) for a business application.
- Set up a Process Archive Service instance ([jeap-process-archive-service](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-process-archive-service/getting-started)).
  - [Local development and testing of the Process Archive Service library](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-process-archive-service/local-development).
- Read an archived artifact back ([jeap-process-archive-reader](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-process-archive-reader/getting-started)) into a typed Avro object.
  - [Read an encrypted archived artifact](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-process-archive-reader/reading-encrypted-artifacts).
- [Set up a Message Exchange Service instance](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-message-exchange-service/getting-started).
