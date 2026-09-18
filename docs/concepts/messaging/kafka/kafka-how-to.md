# Kafka How-To

## Step-by-step integration of Kafka into a service / business application

1. Define [Message Types](../message-types.md) according to the business requirements.
2. Order Kafka topics from the
   party responsible for the cluster (usually one topic per event, though several events per topic are
   possible), following the [Naming Conventions](index.md#topic-names).
3. Define the [Type Descriptor](../message-type-registry/index.md) and
   [Avro Schema](../message-type-registry/index.md), and publish them on a feature branch in the
   [Message Type Registry](../message-type-registry/index.md).
4. Set up an [Error Handling Service](../error-handling/error-handling-service.md).
   - Don't forget to request the roles needed to authorize the service.
5. Add the [Jeap Messaging Library](../jeap-messaging-library/index.md) as a dependency to the service, and
   add the generated message types as a dependency as described in "Usage of Message Types in Java" (see
   [Jeap Messaging Library](../jeap-messaging-library/index.md)).
6. Import the Kafka cluster certificates and the schema registry's root certificate into the truststore (see
   the instructions below).
7. Declare the consumer/producer message contract for the microservice using annotations, as described under
   [Message Contracts](../message-contracts/index.md).
8. Implement the
   [producer](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/jme-messaging-common-lib/src/main/java/ch/admin/bit/jeap/jme/messaging/common/infrastructure/KafkaEventPublisher.java)
   /
   [consumer](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/jme-messaging-common-lib/src/main/java/ch/admin/bit/jeap/jme/messaging/common/infrastructure/KafkaEventConsumer.java)
   following the [example](https://github.com/jme-admin-ch/jme-messaging-example), applying the Idempotent
   Receiver pattern on the consumer side (see the instructions below).
9. Define the Kafka configuration in the service, following the example in
   `jme-messaging-receiver-service/src/main/resources/application-ref.yml` in the
   [jme-messaging-example](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/jme-messaging-receiverpublisher-service/src/main/resources/application.yml)
   repository.
10. Develop and test the event-driven service, both locally and on dev.
    - Follow the guidelines & examples for implementing idempotent behavior (TODO Link).
11. Once the event schema is stable, merge the branch in the
    [Message Type Registry](../message-type-registry/index.md) into master via a pull request.

## Topics, events & keys

### Topics

When creating topics, please follow the [Naming Conventions](index.md#topic-names).

### Settings

| Value | Meaning | Default |
| --- | --- | --- |
| Replicas | The number of brokers a [topic is replicated](https://kafka.apache.org/documentation/#replication) to, in order to increase data safety and availability. A value of 1 means the topic would become unavailable if a broker fails or is upgraded. | Depends on the cluster size |
| Retention | How long records are kept on a topic before being deleted. Consumers must consume records within this time span. The optimal value balances the amount of data on a topic against the maximum time consumers may be down. It also depends on the [architecture pattern](https://martinfowler.com/articles/201701-event-driven.html) used — e.g. with Event Sourcing it may be desirable to keep records on topics for a very long time, whereas with Event Notification the retention period can be much shorter. | dev/ref: 7d, abn/prd: 28d |
| User | Which users have access to a topic. Depends on the protection needs of the business application and the data exchanged on the topic. For topics without particularly sensitive data, it is recommended to use one user per business application. | Depends on the application's protection needs |
| Partitions | The number of partitions (see the next section) a topic is split into. Since a partition is always assigned to exactly one consumer within a consumer group, this also controls the maximum number of parallel consumers. | Depends on the desired consumer scaling |

### Partitioning & use of Kafka keys

Kafka records are key/value pairs, where the key is optional. The key controls how records are distributed
across a topic's partitions; if no key is set, records are distributed evenly across partitions using
hashing.

A topic's partition is always assigned to exactly one consumer within a consumer group; a topic must be
partitioned in order to use several consumer instances. Records with the same key are guaranteed to be
consumed in the order they were produced. Ordering is therefore one of the main use cases for setting
explicit keys.

![Consumer groups](https://sookocheff.com/post/kafka/kafka-in-a-nutshell/consumer-groups.png)

#### Why partition data in Kafka via an explicit key?

Using an explicit key for records makes sense when

- Consumers need an ordering guarantee for messages with a particular key (**main use case**)
- Sharding of events is needed with respect to a scarce external resource, to avoid overloading it
- Consumers use technologies such as KSQL to work directly on the topics and run queries on keys
- Log compaction is used, in which case Kafka guarantees that the last record for a key is kept

Keys are, for example, business IDs, with distribution based on the key's hash value. To avoid an unfavorable
balance across partitions, keys should be fine-grained enough to produce different hash values. A customer
segment with only 3 possible values would be a poor choice of key; a business ID newly assigned for every
order would be a good one.

> Generally, it is recommended to only use keys when explicit ordering guarantees are required. The most even
> distribution across partitions is achieved when no explicit key is set.

### Message types per topic

It is recommended to use one topic per message type. This keeps consumers and producers maximally decoupled,
and the producer makes no assumptions about the granularity needed by consumers. Consumers can subscribe to
exactly the topics whose events they are interested in.

If there are specific requirements on the sequence across different event types, it can be helpful to produce
several events on the same topic. Using the same key then guarantees the sequence as long as processing
succeeds in the consumer. When retrying failed events, the application must be able to handle retries
happening out of the original sequence.

See [https://www.confluent.io/blog/put-several-event-types-kafka-topic/](https://www.confluent.io/blog/put-several-event-types-kafka-topic/)
for details.

## Examples

The [jme-messaging-example](https://github.com/jme-admin-ch/jme-messaging-example) repository shows
consumer/producer configuration and implementation using the
[Jeap Messaging Library](../jeap-messaging-library/index.md).

### Local development with Kafka

Kafka can be started locally — see the Docker Compose file in
[jme-messaging-example](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/docker/docker-compose.yml),
also reproduced under [Kafka – Starting Kafka locally](index.md#starting-kafka-locally).

## Acknowledge / commit

When using the jEAP Messaging Library, two configuration options are set that affect how consumed records
are committed:

- `enable.auto.commit = false` (Kafka client, [https://kafka.apache.org/documentation/#enable.auto.commit](https://kafka.apache.org/documentation/#enable.auto.commit))
- `AckMode = MANUAL` (Spring Kafka, [https://docs.spring.io/spring-kafka/reference/html/#committing-offsets](https://docs.spring.io/spring-kafka/reference/html/#committing-offsets))

In addition, an error handler is installed which ensures that events are never lost: on processing failures
in the consumer, the record is published to the error topic and handled by the Error Handling Service.

Records must therefore **always** be committed (via `Acknowledgment.acknowledge()` in Spring Kafka), whether
processed successfully or handled by the error handler. The acknowledge call must happen at the very end of
event processing, otherwise there is a risk that events get acknowledged even though they were not processed
successfully!

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

Given the way we use Kafka, there is an at-least-once guarantee that produced records are consumed. This
means it is entirely possible for a consumer to receive a record (and hence a domain event) more than once.
Consumers must therefore be implemented idempotently — duplicate events must not cause errors or unexpected
state changes.

For this, the identity part of the [Message Types](../message-types.md) provides an `idempotenceId`. This
can, for example, be persisted as an attribute of an entity created as a result of the event, so that it can
be determined whether an event has already been processed:

```java
    @KafkaListener(topics = {TopicConfiguration.NAME})
    public void consume(final JmeDeclarationCreatedEvent event, Acknowledgment ack) {
        log.debug("Received event {}", event.getIdentity().getEventId());
        if (repository.containsOrderWithIdempotenceId(event.getIdentity().getIdempotenceId()) {
            log.debug("Received duplicate event with idempotenceId {}, ignoring", event.getIdentity().getIdempotenceId());
            ack.acknowledge();
            return;
        }
        ...
        ack.acknowledge();
    }
```

## Relationship between Message Type Registry and Kafka Schema Registry

### Message Type Registry

A [Message Type Registry](../message-type-registry/index.md) provides an overview of the message types in
an application group. Besides the message descriptors — which define metadata for a message type — the
Message Type Registry also contains the Avro schema files. It is therefore the storage location for schemas
at development time.

### Kafka Schema Registry

The Kafka Schema Registry is the storage location for schemas at runtime, i.e. the schemas of all messages
sent within a microservice environment must be stored in the Schema Registry. The
[jEAP Messaging Library](../jeap-messaging-library/index.md) automatically registers the schemas of sent
messages in the Kafka Schema Registry. Using the Kafka Schema Registry is therefore largely transparent to
developers.

### Schema evolution

See [Evolution of Messages](../evolution-of-messages/index.md).

## Further reading

- [https://kafka.apache.org/documentation/#replication](https://kafka.apache.org/documentation/#replication)
- [https://sookocheff.com/post/kafka/kafka-in-a-nutshell/](https://sookocheff.com/post/kafka/kafka-in-a-nutshell/)
- [https://blog.newrelic.com/engineering/effective-strategies-kafka-topic-partitioning/](https://blog.newrelic.com/engineering/effective-strategies-kafka-topic-partitioning/)
- [https://docs.confluent.io/current/schema-registry/index.html](https://docs.confluent.io/current/schema-registry/index.html)
