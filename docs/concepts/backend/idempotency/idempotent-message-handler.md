# Idempotent Message Handler

To simplify the implementation of idempotent message processing, jEAP provides the Java annotation
`@IdempotentMessageHandler`. Within the configured retention period, it ensures that a message handler
method executes successfully at most once for a given idempotence ID and message type, by recording
successfully processed messages in a database — so a microservice doesn't need to extend its own
persistent business data with the idempotence IDs of processed messages.

**See [jeap-messaging — Idempotent message handler](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/idempotent-message-handler)**
for the dependency, the required database schema, annotating a handler method, the `@Transactional` advice-order
caveat, and the full configuration reference.

## Related

- [At-least-once delivery](at-least-once-delivery.md) — why idempotent processing is necessary.
- [How to: integrate Kafka into a service](../../../how-tos/messaging/integrate-kafka-into-a-service.md)
- [Expand-Migrate-Contract](../../continuous-delivery/expand-migrate-contract.md) — why idempotency context ignores the major version.
