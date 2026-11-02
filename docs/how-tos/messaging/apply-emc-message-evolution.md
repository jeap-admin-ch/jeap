# How to: apply EMC Message Evolution to a Kafka message type

Use this when a message-type change would otherwise be incompatible (e.g. adding and removing mandatory
fields at once), but you control or can coordinate with all producers and consumers — the preferred
[Expand-Migrate-Contract](../../concepts/continuous-delivery/expand-migrate-contract.md) strategy, since it
needs no new major version and no parallel publication of two message types. If you don't control the
participants, use
[EMC Message Replacement](../../concepts/continuous-delivery/expand-migrate-contract.md#strategy-emc-message-replacement)
instead.

## Procedure

1. **Expand** — make a compatible change to the Avro schema (e.g. add a new optional attribute) and publish
   a new minor/patch version of the message type.
2. **Migrate** — all consumers/producers migrate to this first new version by updating the Maven dependency
   version for the message type.
3. **Migrate/Contract** — make a further compatible change (e.g. remove an old, no-longer-needed attribute)
   and publish a second new minor/patch version.
4. **Contract** — all consumers/producers migrate to the second new version.

> Both changes are Avro-schema-compatible between reader and writer — one change in `BACKWARD` mode, the
> other in `FORWARD` mode. Because the two steps use different compatibility modes, the **Kafka Schema
> Registry subject** must use compatibility mode `NONE` (this is not the same as the compatibility mode
> declared for a message type version in the Message Type Registry, which should almost never be `NONE`).
> Since jEAP Messaging 7.3.0 the library sets this automatically on the Kafka Schema Registry subject.

For the underlying forward/backward compatibility rules and the special case of a service that consumes a
message type it also produces, see [Evolution of Messages](../../concepts/messaging/evolution-of-messages/index.md)
and [jeap-messaging — Message evolution: self-messages](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/message-evolution#self-messages).

## Related

- [Expand-Migrate-Contract](../../concepts/continuous-delivery/expand-migrate-contract.md) — the general pattern, and the EMC Message Replacement alternative.
- [Evolution of Messages](../../concepts/messaging/evolution-of-messages/index.md) — forward/backward compatibility rules.
- [Message Type Registry](../../concepts/messaging/message-type-registry/index.md)
