# Kafka

## Overview

**Apache Kafka** is an open-source project of the Apache Software Foundation, used in particular for
processing data streams. Within the Blueprint Microservice, Kafka acts as the central message broker.

> In jEAP, messages (Domain Events, Commands, ...) are exchanged over Kafka using
> [Message Types](../message-types.md).

### Getting started

See [Kafka How-To](kafka-how-to.md).

### Kafka configuration

See [Kafka Consumer, Producer & Topic Configuration](kafka-consumer-producer-topic-configuration.md).

## Kafka cluster

Kafka clusters must be provisioned by the program/project before use; credentials can then be stored as
secrets.

## Topic names

Topic names must follow the schema `<system>-<context>-<MessageName without postfix>[-<version postfix from
the message name>]` (all lowercase). The variables have the following meaning:

| Variable | Description | Example |
| --- | --- | --- |
| `system` | Name of the business application publishing the events, in lowercase | `eets` |
| `context` | The name of the bounded context within a business application (in the DDD sense, often corresponding to a microservice) that publishes the events. In lowercase, dash-separated if it has multiple parts. | `billing` |
| `MessageName` without postfix | **DomainEvent**: the event name without the "Event" postfix, e.g. for the (Eets) *BillCreated*Event this is *billcreated*. This part of the name uses a short form of the event name, see [Naming Conventions – Domain events](../../naming-conventions.md#domain-events). **Command**: the command name without the "Command" postfix, e.g. for the (Eets) *CreateBillCommand* this is *createbill*. This part of the name uses a short form of the command name, see [Naming Conventions – Commands](../../naming-conventions.md#commands). | `billcreated` / `createbill` |
| Optional: version | If the event changes in a backward-incompatible way and a new topic is needed to separate the old and new version: version postfix from the event name (e.g. BillCreatedEventV2 → billcreated-v2) | `v2` |

Thus **eets-billing-createbill** (topic with commands) and **eets-billing-billcreated** (topic with domain
events) are both valid topic names.

### Mirrormaker and "internal" in topic names

> **Note:** The Mirrormaker tool is often used for migrations. It treats topics with "internal" at the
> start/end of their name specially: they are excluded from the migration
> ([see the Kafka source](https://github.com/apache/kafka/pull/11220/files#diff-20a9931da3de4b577145af409d7e704e90ed30b410e4d8236e297b033dea6d0aR87)).
>
> To avoid problems in the future, this naming pattern should be avoided.

## Starting Kafka locally

> **Note (ports):** The default port for the
> [Confluent Schema Registry](https://docs.confluent.io/current/schema-registry/index.html) is 8081. This is
> often not ideal, since the port may already be used by a microservice. To change it, the docker-compose
> file can be adjusted (e.g. `7081:8081` instead of `8081:8081`), and the new port configured in the
> application as follows:
>
> `jeap.event.kafka.schemaRegistryUrl: http://localhost:7081`

> **Note (licenses):** The Confluent Control Center may only be used under the Confluent Developer License,
> which is limited to a single broker. If more than one broker is used locally, the Control Center must not
> be used. See
> [https://docs.confluent.io/current/control-center/installation/licenses.html](https://docs.confluent.io/current/control-center/installation/licenses.html)
> for detailed license terms.

The following Docker Compose file can be used to start a local cluster including a local schema registry.
If the [Jeap Messaging Library](../jeap-messaging-library/index.md) is used, this cluster can be reached
with the default settings (from
[`docker/docker-compose.yml`](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/docker/docker-compose.yml)
in [jme-messaging-example](https://github.com/jme-admin-ch/jme-messaging-example)).

The Confluent Control Center can be reached at [localhost:9021](http://localhost:9021/).

## Kafka Schema Registry

All events used within a microservice environment must be defined in the Kafka Schema Registry. The
[Jeap Messaging Library](../jeap-messaging-library/index.md) can publish events directly to the schema
registry. For this, the `useSchemaRegistry` and `autoRegisterSchema` parameters must be set to `true`. This
is the default setting for jEAP Messaging.

## Example

The [Jeap Messaging Library](../jeap-messaging-library/index.md) documentation describes a sample
application that sends events over Kafka using the Jeap Messaging Library.

## Further reading

- [Apache Kafka project page](https://kafka.apache.org/)
