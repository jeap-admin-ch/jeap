# jEAP Test Support for Kafka

This page describes the test infrastructure jEAP provides for services that use Kafka: a way to mock Kafka
away entirely for tests that don't need it, and a base class plus helpers for integration tests that run
against an embedded Kafka broker.

For techniques on how to keep such tests fast and isolated once you're using this infrastructure, see
[Unit / Integration Testing with Kafka](unit-integration-testing-with-kafka.md).

## Integration Tests Without Kafka

Implementing a test (e.g. a Pact test) in a project that uses Kafka is relatively complicated, because an embedded Kafka needs to be available so that the Spring context can start up.

To mock Kafka, there is a test configuration in `jeap-messaging`:

[`jeap-messaging` / `jeap-messaging-infrastructure-kafka-test` / `KafkaMockTestConfig.java`](https://github.com/jeap-admin-ch/jeap-messaging/blob/main/jeap-messaging-infrastructure-kafka-test/src/main/java/ch/admin/bit/jeap/messaging/mockkafka/KafkaMockTestConfig.java)

```java
package ch.admin.bit.jeap.messaging.mockkafka;

import ch.admin.bit.jeap.messaging.avro.AvroMessage;
import ch.admin.bit.jeap.messaging.avro.AvroMessageKey;
import ch.admin.bit.jeap.messaging.kafka.KafkaConfiguration;
import ch.admin.bit.jeap.messaging.kafka.KafkaConsumerConfiguration;
import ch.admin.bit.jeap.messaging.kafka.serde.confluent.config.ConfluentSchemaRegistryAutoConfiguration;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.kafka.autoconfigure.KafkaAutoConfiguration;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.core.KafkaTemplate;
import org.mockito.Mockito;

@TestConfiguration
@EnableAutoConfiguration(exclude = {
        ConfluentSchemaRegistryAutoConfiguration.class,
        KafkaAutoConfiguration.class,
        KafkaConfiguration.class,
        KafkaConsumerConfiguration.class
})
public class KafkaMockTestConfig {

    @Bean
    KafkaTemplate<AvroMessageKey, AvroMessage> kafkaTemplate() {
        return Mockito.mock(KafkaTemplate.class);
    }

}
```

## Test Support in jEAP for Kafka Tests

### Base Class `KafkaIntegrationTestBase`

The base class `KafkaIntegrationTestBase` for tests with embedded Kafka, in the module `jeap-messaging-infrastructure-kafka-test`, provides the following features:

- An `EmbeddedKafka` annotation with a random port for the Kafka broker, for test isolation ([https://docs.spring.io/spring-kafka/reference/testing.html#embedded-kafka-junit5](https://docs.spring.io/spring-kafka/reference/testing.html#embedded-kafka-junit5))
- `EmbeddedKafka` configuration for integration tests. The broker address is automatically set to the embedded Kafka broker with a random port
  - For all configuration options preset in this case, see [`jeap-messaging-embedded-kafka-defaults.properties`](https://github.com/jeap-admin-ch/jeap-messaging/blob/main/jeap-messaging-infrastructure-kafka/src/main/resources/jeap-messaging-embedded-kafka-defaults.properties)
- Waits before the test until all consumer containers have been assigned a partition, to ensure that messages are actually received and processed

### Annotation `@TestKafkaListener`

The `@TestKafkaListener` annotation is an alias for `@KafkaListener`, with the difference that in this test listener the jEAP message-contract check is disabled by default. This means it is not necessary to globally disable the contract check or to create a consumer contract for the test. In addition, the test listener also listens on its own consumer group (specifically `${spring.application.name:testapp}-test`). This ensures that the test listener receives all messages sent on a topic.

```java
@TestKafkaListener(topics = JmeDeclarationCreatedEvent.TypeRef.DEFAULT_TOPIC)
public void consume(JmeDeclarationCreatedEvent event, Acknowledgment ack) {
    log.info("Consuming event in TestKafkaListener: {}", event);
    // ...
    ack.acknowledge();
}
```

### `sendSync()` in `KafkaIntegrationTestBase` Without Contract Check

The `sendSync()` method in `KafkaIntegrationTestBase` (from the module `jeap-messaging-infrastructure-kafka-test`) sets a test header on the message. This causes the contract check for producing the test message to be skipped. It is not necessary to globally disable the contract check, so it still runs — and is covered by the test — for the production code.

```java
class DeclarationServiceIT extends KafkaIntegrationTestBase {

    @Test
    void testCreateDeclaration() {
        AvroMessage event = ...
        // sendSync() sets a test header to skip the contract check for the test message
        sendSync(JmeDeclarationCreatedEvent.TypeRef.DEFAULT_TOPIC, event);

        // ...
    }
}
```

For tests that don't use the base class, the following helper can also be used, which shows the same behavior (it is used internally by `KafkaIntegrationTestBase.sendSync()`):

```java
TestMessageSender.sendSync(kafkaTemplate, topic, message);
```

## Related

- [Unit / Integration Testing with Kafka](unit-integration-testing-with-kafka.md) — recommendations and patterns for fast, isolated tests built on this infrastructure.
