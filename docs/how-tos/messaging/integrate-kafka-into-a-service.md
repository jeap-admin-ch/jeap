# How to: Integrate Kafka into a service

An end-to-end checklist for wiring Apache Kafka into a jEAP-based microservice using the
[jEAP Messaging Library](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/getting-started),
spanning the Message Type Registry, the Error Handling Service and the library itself. For settings
reference (topics, consumers, producers, partitioning), see
[Kafka](../../concepts/messaging/kafka/index.md) and
[Kafka topics & client configuration](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/kafka-topics-and-configuration).

## Checklist

1. Define [Message Types](../../concepts/messaging/message-types.md) according to the business requirements.
2. Order Kafka topics from the party responsible for the cluster (usually one topic per event, though several
   events per topic are possible), following the
   [Naming Conventions](../../concepts/messaging/kafka/index.md#topic-names).
3. Define the type descriptor and Avro schema, and publish them on a feature branch in the
   [Message Type Registry](../../concepts/messaging/message-type-registry/index.md).
4. Set up an
   [Error Handling Service](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-error-handling/getting-started)
   — don't forget to request the roles needed to authorize the service.
5. Add
   [`jeap-messaging-infrastructure-kafka`](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/getting-started)
   and the generated message-type dependencies.
6. Import the Kafka cluster certificates and the schema registry's root certificate into the truststore.
7. Declare the consumer/producer message contracts for the microservice using annotations, as described under
   [jeap-messaging — Message contracts](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/message-contracts).
8. Implement the
   [producer](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/jme-messaging-common-lib/src/main/java/ch/admin/bit/jeap/jme/messaging/common/infrastructure/KafkaEventPublisher.java)
   /
   [consumer](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/jme-messaging-common-lib/src/main/java/ch/admin/bit/jeap/jme/messaging/common/infrastructure/KafkaEventConsumer.java),
   following the [jme-messaging-example](https://github.com/jme-admin-ch/jme-messaging-example) and applying the
   idempotent-receiver pattern on the consumer side (see [below](#idempotent-consumer)).
9. Define the Kafka configuration in the service, following the example in
   [`application.yml`](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/jme-messaging-receiverpublisher-service/src/main/resources/application.yml)
   in the jme-messaging-example repository.
10. Develop and test the event-driven service, both locally (see [below](#local-development-with-kafka)) and on
    dev.
11. Once the event schema is stable, merge the feature branch in the Message Type Registry into master via a
    pull request.

## Local development with Kafka

A trimmed `docker-compose.yml` with a KRaft-mode broker, a schema registry and a Postgres database for the
error-handling service:

```yaml
services:
  broker:
    image: confluentinc/cp-kafka:latest
    hostname: broker
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@broker:9093
      KAFKA_LISTENERS: SASL_PLAINTEXT://broker:9092,CONTROLLER://broker:9093
      KAFKA_ADVERTISED_LISTENERS: SASL_PLAINTEXT://localhost:9092
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: SASL_PLAINTEXT:SASL_PLAINTEXT,CONTROLLER:PLAINTEXT
      KAFKA_SASL_ENABLED_MECHANISMS: SCRAM-SHA-512
      KAFKA_SASL_MECHANISM_INTER_BROKER_PROTOCOL: SCRAM-SHA-512
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  schema-registry:
    image: confluentinc/cp-schema-registry:latest
    depends_on:
      - broker
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: SASL_PLAINTEXT://broker:9092
      SCHEMA_REGISTRY_LISTENERS: http://0.0.0.0:8081

  errorhandling-db:
    image: postgres:latest
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: errorhandling
      POSTGRES_USER: errorhandling
      POSTGRES_PASSWORD: errorhandling
```

See also [Kafka — Starting Kafka locally](../../concepts/messaging/kafka/index.md#starting-kafka-locally) for
notes on schema-registry port clashes and the Confluent Control Center license.

## Acknowledge / commit

jEAP Messaging sets `enable.auto.commit=false` (Kafka client) and `AckMode=MANUAL` (Spring Kafka). A listener
must therefore always call `Acknowledgment.acknowledge()` itself, at the very end of event processing — never
before processing or in a `finally` block, or an early acknowledgment can lose the message on failure. The jEAP
error handler acknowledges a failed record itself, after publishing its failure event:

```java
@KafkaListener(topics = {TopicConfiguration.NAME})
public void consume(final JmeDeclarationCreatedEvent event, Acknowledgment ack) {
    log.debug("Received event {}", event.getIdentity().getEventId());
    // ... processing ...

    ack.acknowledge();
    log.debug("Acknowledged event {}", event.getIdentity().getEventId());
}
```

## Idempotent consumer

At-least-once delivery means a consumer may receive the same record (and hence the same domain event) more
than once — also via an error-handler resubmit. Consumers must therefore be implemented idempotently. The
message identity's `idempotenceId` is the basis for deduplication; see
[jeap-messaging — Idempotent message handler](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/idempotent-message-handler)
for the automatic approach, or deduplicate manually:

```java
@KafkaListener(topics = {TopicConfiguration.NAME})
public void consume(final JmeDeclarationCreatedEvent event, Acknowledgment ack) {
    log.debug("Received event {}", event.getIdentity().getEventId());
    if (repository.containsOrderWithIdempotenceId(event.getIdentity().getIdempotenceId())) {
        log.debug("Received duplicate event with idempotenceId {}, ignoring", event.getIdentity().getIdempotenceId());
        ack.acknowledge();
        return;
    }
    // ... processing ...
    ack.acknowledge();
}
```

## Related

- [Kafka](../../concepts/messaging/kafka/index.md) — topic naming conventions, cluster provisioning, settings reference.
- [jeap-messaging — Message contracts](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/message-contracts)
- [jeap-messaging — Idempotent message handler](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/idempotent-message-handler)
- [Message Type Registry](../../concepts/messaging/message-type-registry/index.md)
- [jeap-messaging getting started](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/getting-started)
- [jeap-messaging — Kafka topics & client configuration](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/kafka-topics-and-configuration)
