# How-Tos: Messaging

Kafka, message types, contracts and registries, the transactional outbox, error handling, and process
archiving/context tracking.

- Add jEAP Messaging to a service ([jeap-messaging](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/getting-started)) — dependency, cluster config, message contracts, produce and consume a first message.
  - [Publish a message](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/publishing-messages).
  - [Consume a message](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/consuming-messages) idempotently.
  - [Encrypt a message type](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/encrypting-messages).
- [Install all message types of a program locally](../../concepts/messaging/message-type-registry/installing-message-types-locally.md) — resolve a Message Type Registry's generated classes into your local Maven repository.
- Set up a Message/Archive Type Registry for a program — [Message Type Registry getting started](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-message-type-registry/getting-started), [Archive Type Registry getting started](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-archive-type-registry/getting-started).
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

## Known gaps — no how-to exists yet

See [`doc-refactoring-plan.md`](https://github.com/jeap-admin-ch/jeap/blob/main/doc-refactoring-plan.md)
for the full list and status. Notably missing: a clean, steps-only Kafka integration how-to (the
existing `kafka-how-to.md` is duplicated and drifted between this repo and jeap-messaging, and is mixed
with reference/explanation in both places), a Confluent→AWS Glue/MSK-IAM migration guide, a how-to for
testing against the outbox/archive-reader locally, and an "onboard a new message type for archiving"
walkthrough.
