# jEAP Messaging Library

## Overview

The **[jEAP Messaging Library](https://github.com/jeap-admin-ch/jeap-messaging)** is a library for working with
[message types](../message-types.md) and other messages in Spring Boot. It allows microservices to send and
receive [messages](../index.md) via [Kafka](../kafka/index.md) quickly and easily. It is based on
[Spring for Apache Kafka](https://docs.spring.io/spring-kafka/reference/html/).

```plantuml
@startuml
skinparam linetype ortho
skinparam nodesep 30
skinparam ranksep 30
skinparam rectangle {
  BorderColor Black
}
skinparam frame {
  BorderColor Black
  BackgroundColor #dbe9f6
}

frame "jeap" as jeap {
  rectangle "messaging-model" as n7
  rectangle "messaging-infrastructure" as n8
  rectangle "messaging-avro-maven-plugin" as n6
  rectangle "messaging-avro" as n1
  rectangle "messaging-infrastructure-kafka" as n2
}

frame "system" as system {
  rectangle "event-definition /\ncommand-definition" as n0
  rectangle "kafka-configuration" as n3
}

rectangle "microservice" as n9
rectangle "microservice" as n4
rectangle "microservice" as n5

n8 -[dashed]-> n7
n1 -[dashed]-> n7
n6 -[dashed]-> n1
n2 -[dashed]-> n1
n0 -[dashed]-> n1 : only compile
n3 -[dashed]-> n2
n9 -[dashed]-> n0
n4 -[dashed]-> n0
n5 -[dashed]-> n0
n9 -[dashed]-> n3 : only runtime
n4 -[dashed]-> n3
n5 -[dashed]-> n3
@enduml
```

To use the jEAP Messaging Library, three layers of code are required:

- **Service layer:** the individual microservice can implement message processors and generators as needed. Since
  these do not depend on the infrastructure, they can be implemented directly as business logic, so that little to
  no overhead / boilerplate code is required in the service itself.
- **System layer:** the actual messages must be defined across multiple microservices. A message must be defined as
  an [Avro](https://de.wikipedia.org/wiki/Apache_Avro) schema. It is also advisable to create a builder and a
  listener interface for each message. The Kafka configuration (topics, acknowledgment strategy, etc.) can also be
  defined here. Depending on requirements, these definitions can be split into several packages and shared with
  other projects, so that messages can be sent across system boundaries.
- **jEAP layer:** across all systems, the **jeap-messaging** library is available, providing the base types as well
  as simple publishers and consumers.

## jEAP Layer

The jEAP layer of the Messaging Library consists of, among others, the following components:

- The **jeap-messaging-model** package defines general, infrastructure-independent interfaces for domain events and
  commands. These could later be used to run parts of the library on other technologies (JSON, RabbitMQ) as well.
- The **jeap-messaging-avro** package contains an implementation of jeap-messaging-model for Avro.
- The **jeap-messaging-api** package defines general, infrastructure-independent interfaces for message listeners
  and publishers. These could later be used to run parts of the library on other technologies (JSON, RabbitMQ) as
  well.
- The **jeap-messaging-infrastructure-kafka** package contains an implementation of jeap-messaging-api for Kafka.
  Published and consumed messages and keys must be Avro objects. All Kafka message keys and values must extend the
  corresponding base types from jeap-messaging-avro.
- The **jeap-messaging-avro-maven-plugin** package provides a plugin for building Java classes from Avro schemas. It
  is based on the pre-configured Avro Maven plugin from Apache and adds additional, specific details. In
  particular, it ensures that the generated classes implement the matching interfaces from jeap-messaging-model
  resp. jeap-messaging-avro. For this to work correctly, the names of the Avro types must follow the naming
  convention.
- The **jeap-messaging-avro-integration-test** package tests the integration of the jeap-messaging-avro-maven-plugin
  with the other components of the Messaging library.

The following classes are particularly relevant for systems that use the Messaging library:

- The class `ch.admin.bit.jeap.domainevent.avro.AvroDomainEventBuilder` can be used as a basis for a builder class
  for your own Avro events.
- The class `ch.admin.bit.jeap.messaging.avro.AvroCommandBuilder` can be used as a basis for a builder class for
  your own Avro commands.
- The class `ch.admin.bit.jeap.messaging.avro.AvroSerializationHelper` can be used to (de)serialize events to/from
  Avro without sending them over Kafka. This is particularly useful for testing a builder, to make sure the events
  it generates conform to the Avro schema and can be (de)serialized.
- The interface `ch.admin.bit.jeap.messaging.infrastructure.MessageListener` can be used as a basis for your own
  listener interfaces.
- The interface `ch.admin.bit.jeap.messaging.infrastructure.MessagePublisher` should be implemented by your own
  publisher class. An object implementing this interface can then be injected into the message generators.

## System Layer

For different microservices to use the same message types, the types must be defined in a central place. This can,
for example, happen in a common-messages library. Depending on the project setup, these can look quite different.
For instance, it can make sense to define several type libraries, since they also need to be shared with other
systems. To create a message type with the Messaging library, the following steps must be taken:

- The message type must be defined as an Avro schema or in Avro IDL (see [Message Types](../message-types.md)). The
  jeap-messaging-avro-maven-plugin can be used for this (see below).
- A builder must be defined. The AvroDomainEventBuilder or AvroCommandBuilder can be extended for this.
- A listener interface must be defined. The MessageListener interface must be extended for this.

Besides the message types, the infrastructure must also be configured. This should also happen across services:

- A publisher class must be implemented, defining where sent messages are published to.
- A message-type-specific consumer class must be implemented, defining where messages are read from.

## Service Layer

Within an individual microservice, the message processors must implement the message-specific listener interface
and then automatically receive the relevant messages. The message generators can have an instance of the
MessagePublisher injected and can then publish any messages. For the microservices to connect to the
infrastructure, they must also be configured correctly.

## Using Message Types in Java

To use a message with the jEAP Messaging Library, it must be defined in the
[Message Type Registry](../message-type-registry/index.md). As part of jEAP Messaging, a Maven plugin is provided
that generates Java classes from the schemas and uploads them to a Maven repository as part of the registry's
build.

:::note
A service can only produce or consume messages for which a [message contract](../message-contracts/index.md)
exists.
:::

The generated classes can be imported from the Maven repository as a dependency:

```xml
<dependencies>
    <dependency>
        <groupId>ch.admin.bit.jme.messagetype.jme</groupId>
        <artifactId>jme-declaration-created-event</artifactId>
        <version>1.4.0</version>
    </dependency>
    <dependency>
        <groupId>ch.admin.bit.jme.messagetype.jme</groupId>
        <artifactId>jme-create-declaration-command</artifactId>
        <version>1.0.0</version>
    </dependency>
</dependencies>
```

The group ID is defined in the `pom.xml` of the respective Message Type Registry, the artifact ID is composed of
the business application and the message name (see example above).

If a message type uses common types of the business application, a dependency on the latest version of that
business application's common types is pulled in transitively. Since common types cannot be changed or deleted
after being published to master, it is usually not a problem to use the latest version.

```xml
<dependencies>
    <dependency>
        <groupId>ch.admin.bit.jme.messagetype.jme</groupId>
        <artifactId>jme-messaging-common</artifactId>
        <version>...</version>
    </dependency>
</dependencies>
```

## Integration

### Dependency

To use the Messaging library for Kafka, the following dependency must be included.

```xml title="Integration of the domain event library for Kafka"
<dependency>
    <groupId>ch.admin.bit.jeap</groupId>
    <artifactId>jeap-messaging-infrastructure-kafka</artifactId>
</dependency>
```

### Configuration

**Multi-cluster configuration vs. single-cluster configuration:** since **version 6**, jEAP Messaging supports
connecting to more than one Kafka cluster. This feature is primarily intended to support hybrid cloud use cases —
see [Support for Multiple Kafka Clusters](support-for-multiple-kafka-clusters.md) for details.

Cluster-specific configuration options can be defined in the configuration under
`jeap.messaging.cluster.<name>.*`.

```yaml
jeap:
  messaging:
    cluster:
      bit:
        bootstrapServers: ...
        # additional configuration options
        default-cluster: true # Optional - if not set explicitly, the first defined cluster becomes the default cluster
      aws:
        bootstrapServers: ...
        # additional configuration options
```

The cluster used for a consumer or producer with Spring Kafka is selected via a `@Qualifier` on the injected
`KafkaTemplate` for producers, resp. via the choice of `ContainerFactory` for consumers. For the default cluster,
neither is necessary.

The qualifier's name corresponds to the cluster name, as does the prefix of the container factory bean, for
example:

```java
// Producer - Specific Cluster

// !!! Be careful with lombok - lombok does by default NOT copy annotations from fields to generated constructors !!!
// See https://projectlombok.org/features/constructor (lombok.copyableAnnotations)

// Qualifier required if the default cluster should not be used
public MyService(@Qualifier("aws") KafkaTemplate awsKafkaTemplate) {
   ...
}

// Consumer - Specific Cluster
@KafkaListener(topics = Message.TypeDef.DEFAULT_TOPIC, containerFactory = "awsKafkaListenerContainerFactory")
void onMessage(Message message, Acknowledgement ack) {
  ...
}

// Producer - Default Cluster. No qualifier required.
@Autowired
private KafkaTemplate kafkaTemplate;

// Consumer - Default Cluster. No containerFactory needs to be specified.
@KafkaListener(topics = Message.TypeDef.DEFAULT_TOPIC)
void onMessage(Message message, Acknowledgement ack) {
  ...
}
```

**Overriding the class used for deserialization**

From version 7.2.0 (Confluent only, not reactive), the deserialized type for the key or value can be specified.
This is needed when a "self-message" (published and received by the same microservice) needs to be changed (see
[EMC message evolution](../evolution-of-messages/index.md)). Thanks to this override, the microservice can use two
different (but compatible) schema versions for sending and receiving messages.

The class can be set with the following properties:

- `specific.avro.key.type`: for deserializing the message key
- `specific.avro.value.type`: for deserializing the message value

An example:

```java
// Messages received of type JmeSimpleTestEvent will be deserialized
// as JmeSimpleTestV2Event (schemas are compatible)
@KafkaListener(topics = TOPIC_NAME, properties = {"specific.avro.value.type=ch.admin.bit.jme.test.JmeSimpleTestV2Event"})
public void consumeWithCustomValueDeserializer(JmeSimpleTestV2Event event, Acknowledgment ack) {
    ...
}

@KafkaListener(topics = OTHER_TOPIC_NAME, properties = {"specific.avro.key.type=ch.admin.bit.jme.test.BeanReferenceMessageKeyV2"})
public void consumeWithCustomKeyDeserializer(ConsumerRecord consumerRecord, Acknowledgment ack) {
   // The key was sent as BeanReferenceMessageKey but has been deserialized as BeanReferenceMessageKeyV2
   lastMessageKey = (BeanReferenceMessageKeyV2) consumerRecord.key();
}
```

Source: [ConsumerCustomDeserializationIT.java](https://github.com/jeap-admin-ch/jeap-messaging/blob/main/jeap-messaging-infrastructure-kafka-test/src/test/java/ch/admin/bit/jeap/messaging/kafka/test/integration/ConsumerCustomDeserializationIT.java)
and [JmeDeclarationCreatedEventCustomDeserializerPropertiesConsumer.java](https://github.com/jeap-admin-ch/jeap-messaging/blob/main/jeap-messaging-infrastructure-kafka-test/src/test/java/ch/admin/bit/jeap/messaging/kafka/test/integration/common/JmeDeclarationCreatedEventCustomDeserializerPropertiesConsumer.java#L22)

**Configuration parameters**

:::note
For backward-compatibility reasons, all cluster-specific properties under `jeap.messaging.kafka.cluster.<name>.*`
can also be configured directly under `jeap.messaging.kafka.*`. This does not apply to the new, AWS-specific
properties.

From a technical point of view, clusters under `jeap.messaging.kafka.cluster.<name>` can be named arbitrarily. The
name is used in the configuration and, in some cases, in logs, but has no technical meaning. Since the name is used
for Spring beans, we recommend avoiding special characters. We also recommend a consistent naming scheme within a
system group.
:::

The following configuration parameters can be set:

| Name | Default | Description |
| --- | --- | --- |
| `jeap.messaging.kafka.cluster.<name>.bootstrapServers` | `localhost:9092` | Address (hostname and port) of the Kafka bootstrap servers. |
| `jeap.messaging.kafka.cluster.<name>.consumerBootstrapServers` | - | Address (hostname and port) of the Kafka bootstrap servers for Kafka message consumers. If not defined, Kafka message consumers use the bootstrap servers from `jeap.messaging.kafka.bootstrapServers`. Available from jEAP Messaging 4.2.0. |
| `jeap.messaging.kafka.cluster.<name>.producerBootstrapServers` | - | Address (hostname and port) of the Kafka bootstrap servers for Kafka message producers. If not defined, Kafka message producers use the bootstrap servers from `jeap.messaging.kafka.bootstrapServers`. Available from jEAP Messaging 4.2.0. |
| `jeap.messaging.kafka.cluster.<name>.adminClientBootstrapServers` | - | Address (hostname and port) of the Kafka bootstrap servers for Kafka admin clients. If not defined, Kafka admin clients use the bootstrap servers from `jeap.messaging.kafka.bootstrapServers`. Available from jEAP Messaging 4.2.0. |
| `jeap.messaging.kafka.cluster.<name>.default-producer-cluster-override` | `false` | Controls whether this cluster is used by default for producing records via one of the beans listed below. This option is intended for cross-cluster migration scenarios, so that consumption happens from the default cluster (target cluster) while production still happens on the source cluster while mirroring from source to target takes place. Once all consumers have migrated to the target cluster, the producer-cluster-override flag can be removed again and mirroring disabled. Affects whether the following beans are annotated as `@Primary` and thus injected as the default without specifying a cluster: `KafkaTemplate`, `KafkaProducerFactory`, `SenderOptions`, `ReactiveKafkaProducerTemplate`, `TransactionalOutbox` (+ internal outbox beans). |
| `jeap.messaging.kafka.useSchemaRegistry` | `true` | Whether a schema registry should be used. If `false`, an internal mock Confluent schema registry is used. |
| `jeap.messaging.kafka.autoRegisterSchema` | `true` | Whether new schemas should be automatically registered in the Kafka schema registry. Avro (de)serialization is configured to use the [TopicRecordNameStrategy](https://docs.confluent.io/current/schema-registry/serializer-formatter.html#subject-name-strategy) to determine the schema's name. |
| `jeap.messaging.kafka.expose-message-key-to-consumer` | `false` | Whether the message keys are made available to the consumer (`true`) or suppressed (`false`). |
| `jeap.messaging.kafka.errorTopicName` | - | Name of the error topic. If events cannot be processed, a [MessageProcessingFailed event](../error-handling/message-processing-failed-event.md) is written to this topic. Can also be configured per cluster under `jeap.messaging.kafka.cluster.<name>.errorTopicName`. |
| `jeap.messaging.kafka.systemName` | - | Name of the sending system. Required when generating a [MessageProcessingFailed event](../error-handling/message-processing-failed-event.md). |
| `jeap.messaging.kafka.serviceName` | - | Name of the sending service. Required when generating a [MessageProcessingFailed event](../error-handling/message-processing-failed-event.md). |
| `jeap.messaging.kafka.publishWithoutContractAllowed` | `false` | Can the service send events without contracts? Must be `false` in production; can be set to `true` in development environments to use events outside the event registry. |
| `jeap.messaging.kafka.consumeWithoutContractAllowed` | `false` | Can the service receive events without contracts? Must be `false` in production; can be set to `true` in development environments to use events outside the event registry. |
| `jeap.messaging.kafka.silentIgnoreWithoutContract` | `false` | If an event without a contract is received, an error message is emitted. This is also the case, for example, if a system listens on a topic with multiple events but only processes some of them. This flag can be used to suppress these error messages. |
| `jeap.messaging.kafka.messageTypeEncryptionDisabled` | `false` | Disables encryption of message types whose producer contract has configured an encryption key ID (and thus encryption) for the application. Allows, for example, writing tests without needing jEAP Crypto instantiation. Forbidden on the acceptance and production environments. |
| `jeap.messaging.kafka.errorServiceRetryIntervalMs` | `5000` | Defines the interval after which writing a [MessageProcessingFailed event](../error-handling/message-processing-failed-event.md) is retried (see also [Error Handler of the jEAP Messaging Library](../error-handling/error-handler-of-the-jeap-messaging-library.md)). |
| `jeap.messaging.kafka.errorServiceRetryAttempts` | `5` | Defines the number of attempts to send a [MessageProcessingFailed event](../error-handling/message-processing-failed-event.md). After that, the program is terminated (see also [Error Handler of the jEAP Messaging Library](../error-handling/error-handler-of-the-jeap-messaging-library.md)). |
| `jeap.messaging.kafka.embedded` | - | If explicitly set to `false`, disables jEAP Messaging's automatic configuration for tests with EmbeddedKafka. Specifically, in this case, the bootstrap server and the mock schema registry are not configured automatically. If explicitly set to `true`, forces the automatic configuration for EmbeddedKafka. |

### Confluent Schema Registry & Apache Kafka with SASL Authentication

The following configuration parameters can additionally be set:

| Name | Default | Description |
| --- | --- | --- |
| `jeap.messaging.kafka.cluster.<name>.schemaRegistryUrl` | [http://localhost:8081](http://localhost:8081) | URL of the schema registry. |
| `jeap.messaging.kafka.cluster.<name>.schemaRegistryUsername` | - | Username for accessing the schema registry, if authenticated access is required, otherwise not to be configured. |
| `jeap.messaging.kafka.cluster.<name>.schemaRegistryPassword` | - | Password for accessing the schema registry, if authenticated access is required, otherwise not to be configured. |
| `jeap.messaging.kafka.cluster.<name>.securityProtocol` | `PLAINTEXT` | Protocol used to connect to Kafka. For SASL-authenticated access, either `SASL_SSL` or `SASL_PLAINTEXT`. For unauthenticated access, `SSL` or `PLAINTEXT`. |
| `jeap.messaging.kafka.cluster.<name>.username` | - | Username for accessing Kafka, if authenticated access is required, otherwise not to be configured. |
| `jeap.messaging.kafka.cluster.<name>.password` | - | Password for accessing Kafka, if authenticated access is required, otherwise not to be configured. |

### AWS Glue Schema Registry & AWS Managed Streaming for Apache Kafka (MSK)

If the corresponding AWS products should be used instead of a Confluent Schema Registry and on-premises Kafka, this
can be configured. The Glue Schema Registry and IAM authorization for MSK can be used independently of one another,
but it typically makes sense to configure both.

For credentials for the AWS APIs, either a bean of type
[AwsCredentialsProvider](https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/auth/credentials/AwsCredentialsProvider.html)
is expected, or — if none is present in the Spring context — a
[DefaultCredentialsProvider](https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/auth/credentials/DefaultCredentialsProvider.html)
is instantiated. This uses, for example on ECS, the task's IAM role, which is usually a sensible default.

The following configuration parameters can additionally be set:

**Glue Schema Registry**

| Name | Mandatory | Default | Description |
| --- | --- | --- | --- |
| `jeap.messaging.kafka.cluster.<name>.aws.glue.registryName` | Y | - | Name of the Glue Schema Registry (e.g. `my-registry`). **This property activates the AWS Glue Schema Registry integration in jeap-messaging.** This disables the Confluent Schema Registry. |
| `jeap.messaging.kafka.cluster.<name>.aws.glue.region` | Y | - | Region in which the Glue Schema Registry is provisioned. |
| `jeap.messaging.kafka.cluster.<name>.aws.glue.endpoint` | N | `<regional endpoint>` | API endpoint for the Glue Schema Registry. Derived from the region by the AWS SDK; only useful to override for tests. |
| `jeap.messaging.kafka.cluster.<name>.aws.glue.assumeIamRoleArn` | N | - | For cross-account access to a Glue Schema Registry, [AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) can be used to obtain a token for a role in the account where Glue is provisioned. This property contains the [ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) of the role. |
| `jeap.messaging.kafka.cluster.<name>.aws.glue.assumeIamRoleSessionName` | N | `${spring.application.name}` | Identifies the client in logs etc. when a role from another account is used to access Glue via AssumeRole. |
| `jeap.messaging.kafka.cluster.<name>.aws.glue.stsEndpoint` | N | `<global STS endpoint>` | API endpoint for the Security Token Service. AWS recommends using the regional endpoint, see the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html). Can also be controlled via an environment variable, see the AWS docs. |
| `jeap.messaging.kafka.cluster.<name>.aws.glue.stsClientTimeoutSeconds` | N | `30s` | Timeout of the Security Token Service client used to obtain a token for accessing Glue via [AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html). |

**MSK Kafka (IAM Authorization)**

| Name | Mandatory | Default | Description |
| --- | --- | --- | --- |
| `jeap.messaging.kafka.cluster.<name>.aws.msk.iamAuthEnabled` | Y | `false` | **This property activates the AWS MSK authentication integration in jeap-messaging.** |
| `jeap.messaging.kafka.cluster.<name>.aws.msk.region` | N | - | Region of the AWS Security Token Service (STS) when AssumeRole is used to authenticate against MSK. |
| `jeap.messaging.kafka.cluster.<name>.aws.msk.assumeIamRoleArn` | N | - | For cross-account access to MSK, [AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) can be used to obtain a token for a role in the account where MSK is provisioned. This property contains the [ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) of the role. |
| `jeap.messaging.kafka.cluster.<name>.aws.msk.assumeIamRoleSessionName` | N | `${spring.application.name}` | Identifies the client in logs etc. when a role from another account is used to access MSK via AssumeRole. |

### Registering Message-Type Schemas in the Kafka Schema Registry

For messages to be successfully sent and received over Kafka with the jEAP Messaging Library, the schemas of the
transmitted messages must be present in the Kafka schema registry. By default, new schemas are automatically
registered in the Kafka schema registry by the message sender before the first time a corresponding message is
sent (see configuration property `jeap.messaging.kafka.autoRegisterSchema`).

For the Confluent Schema Registry: since jEAP Messaging already checks compatibility between schema versions during
build and deployment in the [Message Type Registry](../message-type-registry/index.md) and on the
[Message Contract Service](../message-contracts/message-contract-service.md), the compatibility mode `NONE` is
generally set on the Confluent Schema Registry (since jeap-messaging 7.3.0). No further compatibility check then
takes place on the Confluent registry.

For AWS Glue, `NONE` is likewise used, resp. no compatibility check is activated.

### Encrypting Messages

Since version 4.9.0, the jEAP Messaging Library supports encrypting messages, based on the
jEAP Crypto library (TODO Link). For this, the application must
configure a `KeyIdCryptoService` instance from jEAP Crypto in the jEAP Kafka message serializer and deserializer
implementations. The `jeap-messaging-infrastructure-kafka` library does this automatically if such an instance is
available as a Spring bean. Such a bean can, for example, be provided via the `jeap-crypto-vault-starter` (together
with the `jeap-spring-boot-vault-starter`). This makes the wrapping keys declared in the jEAP Vault crypto
configuration available to messaging for encrypting and decrypting messages.

The following example shows the configuration of such a wrapping key under the key ID `messagingKey` with Vault.
For other key management systems supported by jeap-crypto, see the jEAP Crypto library's documentation. For
jeap-messaging, the KMS used is not relevant — everything supported by jeap-crypto is supported.

```yaml
jeap:
  crypto:
    vault:
      default-secret-engine-path: "transit/jme"
      keys:
        messagingKey: # key id, any name can be chosen
          key-name: "jme-crypto-example-messaging-key" # key name in vault
```

If a message should be sent encrypted, the wrapping key (vault key) to be used for it must be referenced by its key
ID in the message's producer contract. This happens via the `encryptionKeyId` field in the annotation used to
define producer contracts (see [Message Contracts](../message-contracts/index.md)). In the following example, a
producer contract for the message type `SomeEvent` is declared, and it declares that the producer encrypts
messages of this type with the wrapping key referenced by the key ID `messagingKey`.

```java
@JeapMessageProducerContract(value=SomeEvent.TypeRef.class, encryptionKeyId = "messagingKey")
```

The jEAP example project [jme-crypto-example](https://github.com/jme-admin-ch/jme-crypto-example) shows an example
of sending and receiving encrypted messages.

### Signing Messages and Verifying Signatures

Since version 8.21.0, the jEAP Messaging Library supports signing messages when sending and verifying their
signature on receipt.

#### Overview

The process looks as follows:

```plantuml
@startuml
title jEAP Messaging Signature

left to right direction

skinparam shadowing false
skinparam componentStyle rectangle
skinparam defaultTextAlignment center

component "Publisher" as publisher #E2E2E2
component "Subscriber" as subscriber #E2E2E2

component "jEAP Messaging" as publisherMessaging #F9CB9C
component "jEAP Messaging" as subscriberMessaging #F9CB9C

component "Message\nwith Signature" as signedMessage #F9CB9C

component "Secrets Management" as secretsManagement #E2E2E2
component "Config Provider" as configProvider #E2E2E2

component "Private Key" as privateKey #9FC5E8
component "Certificate\npublicKey\npublisher" as certificate #9FC5E8

component "Messaging Trust Config\n(Optional)" as messagingTrustConfig #9FC5E8
component "TrustedPublisher\npublisher\nmessageType" as trustedPublisher #9FC5E8
component "UnsignedMessageType\nmessageType" as unsignedMessageType #9FC5E8

component "KafkaRecordHeader\nSignature" as signatureHeader #9FC5E8
component "jeap-sign\njeap-sign-key\njeap-cert" as signatureHeaders #9FC5E8

component "Automated Secrets Management Process" as secretsProcess #FFFFFF

publisher --> publisherMessaging : uses
publisherMessaging --> signedMessage : publishes
signedMessage --> subscriberMessaging : delivered
subscriberMessaging --> subscriber : consumes

publisher --> secretsManagement : getPrivateKey()
secretsManagement --> privateKey

subscriber --> configProvider : getCertificate(certReference)
configProvider --> certificate : provides certificate
secretsManagement --> certificate : manages certificate

publisherMessaging --> signatureHeader : adds header
signatureHeader --> signatureHeaders : contains

subscriberMessaging ..> messagingTrustConfig : optional trust configuration
messagingTrustConfig --> trustedPublisher
messagingTrustConfig --> unsignedMessageType

secretsManagement --> secretsProcess : createSecret()
configProvider --> secretsProcess : publish Certificate

note right of messagingTrustConfig
  TrustedPublisher and
  UnsignedMessageType define
  the subscriber trust rules.
end note

@enduml
```

| Step | Description |
| --- | --- |
| 1a and b | At startup: the jEAP Messaging Library retrieves the private key and the certificate from the platform's secrets management. |
| 2a | The jEAP Messaging Library signs the value and, if present, the key of the message. It ensures that the publisher declared in the message exactly matches the publisher in the certificate (fail fast). |
| 2b | The signature(s) and the reference to the certificate, specifically its serial number, are transported with the message as Kafka record headers. |
| 3 | At startup: the jEAP Messaging Library retrieves the required certificates from the platform's config provider. |
| 4a | The jEAP Messaging Library verifies the signature of the message, determines the effective publisher via the certificate, and verifies that the publisher declared in the message matches the one in the certificate. |
| 4b | The subscriber can (optionally) configure that certain message types are only accepted from explicitly declared publishers (several are possible), and that certain message types are accepted even without a signature. |

#### Configuration

**Publisher**

| Name | Mandatory | Default | Description | Example |
| --- | --- | --- | --- | --- |
| `jeap.messaging.authentication.publisher.signature-key` | N (Y if signature-certificate is set) | - | The private key used for signing. | `-----BEGIN PRIVATE KEY-----`<br/>`MIIEcDCCAlgCFFx88xf15M8AEghQtgqUwFlNyWTjMA0GCSqGSIb3DQEBCwUAMG8x`<br/>`....`<br/>`-----END PRIVATE KEY-----` |
| `jeap.messaging.authentication.publisher.signature-certificate` | N (Y if signature-key is set) | - | The service's certificate (contains, among other things, the serial number). | `-----BEGIN CERTIFICATE-----`<br/>`MIIEcDCCAlgCFFx88xf15M8AEghQtgqUwFlNyWTjMA0GCSqGSIb3DQEBCwUAMG8x`<br/>`....`<br/>`-----END CERTIFICATE-----` |

**Subscriber**

| Name | Mandatory | Default | Description | Example |
| --- | --- | --- | --- | --- |
| `jeap.messaging.authentication.subscriber.require-signature` | N | `false` | Strict mode on or off: if `true`, every message except whitelisted ones must have a signature. If `false`, unsigned messages are allowed, but signatures are still verified when the signature headers are present. | `false` |
| `jeap.messaging.authentication.subscriber.accept-unsigned-messagetype-whitelist` | N | - | A list of message types that do not necessarily need a signature. | `accept-unsigned-messagetype-whitelist: [DummyEvent1, DummyEvent2]` |
| `jeap.messaging.authentication.subscriber.allowed-publishers` | N | - | A map of message types and their corresponding services (list). If an entry is present for a message type, only messages of that type from the configured services are accepted. | `allowed-publishers: {JmeDeclarationCreatedEvent: [jme-messaging-receiverpublisher-service, jme-messaging-receiverpublisher-outbox-service], JmeOtherEvent: [jme-messaging-receiverpublisher-service]}` |
| `jeap.messaging.authentication.subscriber.certificate-chains` | N (Y if signature verification is enabled and signed messages are consumed) | - | A map of services and their corresponding certificate chains. A certificate chain consists of a leaf certificate (certificate of the sending service), any intermediate certificates, and the root certificate. The service certificates are used to verify the signature of the values and keys. | see example below |
| `jeap.messaging.authentication.subscriber.privileged-producer-common-names` | N | - | A list of producer certificate common names (CNs) for which the signature is checked, but not whether the CN matches the producer name in the message's identity part. Primarily intended for migration scenarios (mirroring topics between clusters with changes to record format + signature, e.g. on-premises → AWS MSK). | `privileged-producer-common-names: [mirrormaker]` |
| `jeap.messaging.authentication.subscriber.allow-non-jeap-messages` | N | `false` | If set to `true`, non-jEAP messages are also possible; these are not subject to signature verification. | `true` |

Example `certificate-chains` configuration:

```yaml
certificate-chains:
  jme-messaging-receiverpublisher-service:
    - chain:
      - |-
        -----BEGIN CERTIFICATE-----
        MIIEcDCCAlgCFFx88xf15M8AEghQtgqUwFlNyWTjMA0GCSqGSIb3DQEBCwUAMG8x
        ....
        -----END CERTIFICATE-----
      - ${intermediate-certificate}
      - ${root-certificate}
```

#### Metrics

The following metrics are published by the signature functionality:

| Metric | Type | Remarks |
| --- | --- | --- |
| `jeap_messaging_signature_certificate_days_remaining` | Gauge | Shows the number of days the certificate configured for the publisher is still valid. Per application. |
| `jeap_messaging_signature_required_state` | Gauge | Shows whether the subscriber has `require-signature` set (`1`) or not (`0`). Per application. |
| `jeap_messaging_signature_validation_outcome` | Counter | Shows how many signature validations succeeded (`status=OK`) or failed (`status=NOK`). Per application and message type. |

The metric `jeap_messaging_total` was extended with information on whether the message was signed (`signed=1`) or
not (`signed=0`).

#### Error Cases

The following error cases can occur:

| Error case | Consequence |
| --- | --- |
| **Publisher**, if signing is active, i.e. signature-key is configured. | |
| Private key and certificate do not match. | Publisher service cannot start (checked at startup). |
| **Subscriber**, if signature verification is active, i.e. require-signature is configured. | |
| Arrival of an unsigned message when a signature is required. Strict mode and no whitelist entry for the message. | Message is not consumed and is sent to the error handling service. Permanent error. |
| Arrival of a signed message whose corresponding certificate cannot be found (not configured). | Message is not consumed and is sent to the error handling service. Temporary error, can be fixed by adjusting the configuration. |
| Arrival of a signed message whose corresponding certificate is no longer valid. | Message is not consumed and is sent to the error handling service. Permanent error. |
| Arrival of a signed message whose certificate chain is not valid. | Message is not consumed and is sent to the error handling service. Temporary error, may be fixable by adjusting the configuration. |
| Arrival of a signed message where the common name in the certificate does not match the sending service. | Message is not consumed and is sent to the error handling service. Permanent error. |
| Arrival of a signed message whose signature is not valid. | Message is not consumed and is sent to the error handling service. Permanent error. |

#### Examples

The jEAP example project [jme-messaging-example](https://github.com/jme-admin-ch/jme-messaging-example) shows an
example of sending and receiving signed messages on AWS — see the
[README.md](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/README.md) under "*Message signing*".


## Filtering Messages

From jeap-messaging version 11.14.0 (jeap-spring-boot-parent 30.14.0), messages resent by the Error Handling
Service (EHS) are automatically filtered out if they are not intended for the consuming service. The EHS sets the
header `jeap_eh_target_service` for this purpose. jeap-messaging discards messages where the service specified in
the header does not match the consuming service.

## Example Application

The example application [jme-messaging-example](https://github.com/jme-admin-ch/jme-messaging-example)
uses the jEAP Messaging Library. The application consists of several parts (see also
[README.md](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/README.md)):

- [jme-messaging-common-lib](https://github.com/jme-admin-ch/jme-messaging-example/tree/main/jme-messaging-common-lib)
  defines the system layer (see above). These classes can be shared across several microservices. The file
  `src/main/avro/events.json` references the event descriptor with the
  [event schema in Avro IDL](https://github.com/jme-admin-ch/jme-message-type-registry/blob/main/descriptor/jme/event/jmedeclarationcreatedevent/JmeDeclarationCreatedEvent_v2.avdl)
  (the `JmeDeclarationCreatedEventBuilder`, `JmeDeclarationCreatedEventListener` and `infrastructure` package
  referenced from the same source page point at an older, now-renamed repository, `jme-event-example`, that could
  not be found on GitHub — see the migration notes below); the Maven plugin is used to generate Java classes from
  this event (see `pom.xml`).
- `jme-messaging-sender-service` is a microservice that creates events and sends them via Kafka. On a request to
  `/send/?message=XXX`, an event with the message "XXX" is sent.
- `jme-messaging-receiver-service` receives the events and stores them in a buffer. On a request to `/receive`, the
  buffered events are returned.

## Health Indicators

For the health indicators exposed by the library, see
[docs/health-indicators.md](https://github.com/jeap-admin-ch/jeap-messaging/blob/main/docs/health-indicators.md) in
the jeap-messaging repository.

## See also

- [Messaging](../index.md) — the general messaging concept overview.
- [Message Types](../message-types.md) — how message types are defined and versioned.
- [Kafka](../kafka/index.md) — the Kafka concepts jEAP Messaging builds on.
- [Message Type Registry](../message-type-registry/index.md) — where message types are defined and published.
- [Message Contracts](../message-contracts/index.md) — the producer/subscriber contracts required to send or
  receive a message.
- [Support for Multiple Kafka Clusters](support-for-multiple-kafka-clusters.md) — connecting a service to more than
  one Kafka cluster.
- [Signing Messages and Checking Signatures Without jEAP](signing-messages-and-checking-signatures-without-jeap.md) —
  implementing message signing without the jEAP Messaging Library.
- [Spring for Apache Kafka documentation](https://docs.spring.io/spring-kafka/reference/html/)
- [Spring AMQP documentation](https://docs.spring.io/spring-amqp/docs/current/reference/html/)
- [Avro IDL documentation](https://avro.apache.org/docs/current/idl.html)
- [Avro schema documentation](http://avro.apache.org/docs/1.9.1/)
- [Avro protocol documentation](https://avro.apache.org/docs/1.8.1/spec.html#Protocol+Declaration)
