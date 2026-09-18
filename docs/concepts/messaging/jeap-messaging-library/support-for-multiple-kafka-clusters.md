# Support for Multiple Kafka Clusters

## Introduction

jEAP Messaging supports connecting to more than one Kafka cluster since version 6. This feature is primarily
intended to support hybrid cloud use cases. See [jEAP Messaging Library — Configuration](index.md#configuration)
for a reference of all available configuration properties and more code examples.

Also, the jme-messaging-examples repository contains a multi-cluster example,
`jme-messaging-multicluster-service` — the module path referenced in the original documentation could not be
verified against the current [jme-messaging-example](https://github.com/jme-admin-ch/jme-messaging-example)
repository on GitHub (see migration notes in the summary).

## Example

For example, a Spring Boot service might connect to two different Kafka clusters and schema registries:

```plantuml
@startuml
title Multi-Cluster Overview

left to right direction

skinparam shadowing false
skinparam componentStyle rectangle
skinparam packageStyle rectangle
skinparam defaultTextAlignment center

package "jEAP-based Spring Boot Service" as springBootService #E2E2E2 {
  component "Spring Kafka Beans\nCluster 1\n@Primary\n@Qualifier(\"bit\")" as springKafkaBeansBit #C9DAF8
  component "Spring Kafka Beans\nCluster 2\n@Qualifier(\"aws\")" as springKafkaBeansAws #D9EAD3
}

package "Kafka Cluster 1\nExample name: \"bit\"\nDefault cluster" as kafkaCluster1 #FFFFFF {
  component "Kafka Cluster 1" as kafka1 #C9DAF8
  database "Schema\nRegistry" as schemaRegistry1 #C9DAF8
}

package "Kafka Cluster 2\nExample name: \"aws\"" as kafkaCluster2 #FFFFFF {
  component "Kafka Cluster 2" as kafka2 #D9EAD3
  database "Schema\nRegistry" as schemaRegistry2 #D9EAD3
}

springKafkaBeansBit --> kafkaCluster1 : Produce / Consume
springKafkaBeansAws --> kafkaCluster2 : Produce / Consume

kafka1 ..> schemaRegistry1
kafka2 ..> schemaRegistry2

@enduml
```

### Configuration

This shows a complete configuration example for two clusters. See
[jEAP Messaging Library — Configuration](index.md#configuration) for a reference of all available configuration
properties.

```yaml
jeap:
  messaging:
    kafka:
      error-topic-name: example-messageprocessing-failed
      system-name: example
      cluster:
        # Cluster configuration 1
        bit:
          bootstrap-servers: "https://example-kafka:1234"
          schema-registry-url: "https://example-registry:1234"
          username: example-user
          password: ${example-secret}
          security-protocol: SASL_SSL
        # Cluster configuration 2
        cloud:
          aws:
            glue:
              registry-name: example-registry-aws
              region: eu-central-2
              assume-iam-role-arn: arn:...
            msk:
              iam-auth-enbled: true
              bootstrap-servers: "https://example-kafka-aws:1234"
```

### Code

The beans for the default cluster are marked as `@Primary` beans. This means that you can inject Spring Kafka
beans (`KafkaTemplate` mainly) without any special qualifiers.

For non-default clusters, the bean names are prefixed with the cluster name, and annotated with
`@Qualifier(clusterName)`. These beans can be injected using the cluster name as a qualifier (see example).

| Use Case | Default Cluster | Other Clusters (for example, a cluster named "aws") |
| --- | --- | --- |
| Consumer | `@KafkaListener(topics=...)` | `@KafkaListener(topics=..., containerFactory = "awsKafkaListenerContainerFactory")` |
| Producer | `KafkaTemplate<AvroMessageKey, AvroMessage> defaultClusterTemplate` | `@Qualifier("aws") KafkaTemplate<AvroMessageKey, AvroMessage> awsClusterTemplate` |

The jme-messaging-example application contains an example of a Spring Boot service that injects Spring Kafka beans
and defines Spring Kafka listeners that produce/consume from different clusters (see the
`jme-messaging-multicluster-service` module in
[jme-messaging-example](https://github.com/jme-admin-ch/jme-messaging-example) — see the note above on this
module path).

#### Caveat When Using Lombok

Be careful when using Lombok to generate constructors (`@AllArgsConstructor`, `@RequiredArgsConstructor`) for
Spring beans. Lombok does by default not copy annotations from fields to generated constructors.

This means that `@Qualifier` annotations on fields will not be taken into account, leading to the Kafka template
for the default cluster being injected regardless of qualifier annotations on the field.

There are two options to deal with that:

1. Avoid Lombok, at least in this case.
2. Configure Lombok to copy the annotation to the generated constructor (see `lombok.copyableAnnotations` in
   [https://projectlombok.org/features/constructor](https://projectlombok.org/features/constructor)).

## Spring Kafka Bean Autoconfiguration in jeap-messaging

When the dependency jeap-messaging-infrastructure is on the classpath, it will activate the Spring autoconfiguration
support for jEAP Messaging.

1. The autoconfiguration class [KafkaConfiguration](https://github.com/jeap-admin-ch/jeap-messaging/blob/main/jeap-messaging-infrastructure-kafka/src/main/java/ch/admin/bit/jeap/messaging/kafka/KafkaConfiguration.java)
   in jeap-messaging will activate the import bean registrar
   [JeapKafkaBeanRegistrar](https://github.com/jeap-admin-ch/jeap-messaging/blob/main/jeap-messaging-infrastructure-kafka/src/main/java/ch/admin/bit/jeap/messaging/kafka/bean/JeapKafkaBeanRegistrar.java).
2. [JeapKafkaBeanRegistrar](https://github.com/jeap-admin-ch/jeap-messaging/blob/main/jeap-messaging-infrastructure-kafka/src/main/java/ch/admin/bit/jeap/messaging/kafka/bean/JeapKafkaBeanRegistrar.java)
   iterates over each cluster configured under `jeap.messaging.kafka.cluster.<clustername>`.
3. If a cluster is marked with `default-cluster=true`, this will be the default cluster. Otherwise, the first
   cluster in the YAML configuration will be the designated default cluster.
4. For each configured cluster, beans will be registered:
   1. Default cluster: bean names will not be prefixed (for example, `kafkaTemplate`). The registered beans will
      be marked as `@Primary`. Spring will prefer primary beans at injection points without a qualifier.
      - The following beans are marked `@Primary` for a cluster other than the default cluster if
        `default-producer-cluster-override=true` (supported from jEAP Messaging 7.10.0) is set for a specific
        cluster:
        1. `KafkaTemplate`
        2. `KafkaProducerFactory`
        3. `SenderOptions`
        4. `ReactiveKafkaProducerTemplate`
        5. `TransactionalOutbox` (+ internal outbox beans)
   2. Other clusters: bean names will be prefixed with the cluster name (for example, `awsKafkaTemplate`). The
      registered beans will be marked as `@Qualifier("clusterName")`. Spring will inject these beans at injection
      points when a matching qualifier is annotated (see "Code" above).

This graph shows the most relevant Spring beans that are relevant for cluster-specific producers and consumers:

```plantuml
@startuml
title Spring Kafka Beans per Cluster

left to right direction

skinparam shadowing false
skinparam componentStyle rectangle
skinparam packageStyle rectangle
skinparam defaultTextAlignment center

package "jEAP-based Spring Boot Service" as springBootService #E2E2E2 {
  package "Spring Kafka Beans Cluster 1\nName: \"bit\" – Default Cluster\n@Primary @Qualifier(\"bit\")" as cluster1 #C9DAF8 {
    component "TransactionalOutbox" as transactionalOutbox1
    component "KafkaTemplate" as kafkaTemplate1
    component "KafkaConsumerFactory" as kafkaConsumerFactory1
    component "KafkaProducerFactory" as kafkaProducerFactory1
    component "KafkaAvroSerdeProvider" as kafkaAvroSerdeProvider1
    component "KafkaAdmin" as kafkaAdmin1
    component "KafkaListenerContainerFactory" as kafkaListenerContainerFactory1
    component "KafkaTransactionManager" as kafkaTransactionManager1
    component "KafkaSaslAuthProperties" as kafkaSaslAuthProperties1
  }

  package "Spring Kafka Beans Cluster 2\nName: \"aws\"\n@Qualifier(\"aws\")" as cluster2 #D9EAD3 {
    component "TransactionalOutbox" as transactionalOutbox2
    component "KafkaTemplate" as kafkaTemplate2
    component "KafkaConsumerFactory" as kafkaConsumerFactory2
    component "KafkaProducerFactory" as kafkaProducerFactory2
    component "KafkaAvroSerdeProvider" as kafkaAvroSerdeProvider2
    component "KafkaAdmin" as kafkaAdmin2
    component "KafkaListenerContainerFactory" as kafkaListenerContainerFactory2
    component "KafkaTransactionManager" as kafkaTransactionManager2
    component "AwsMskKafkaAuthProperties" as awsMskKafkaAuthProperties2
  }

  component "KafkaConfiguration" as kafkaConfiguration #E2E2E2
  component "KafkaProperties" as kafkaProperties #E2E2E2
  component "CommonErrorHandler" as commonErrorHandler #E2E2E2
}

' Cluster 1 bean relationships
transactionalOutbox1 --> kafkaTemplate1
kafkaTemplate1 --> kafkaProducerFactory1
kafkaConsumerFactory1 --> kafkaAvroSerdeProvider1
kafkaConsumerFactory1 --> kafkaConfiguration
kafkaConsumerFactory1 --> kafkaAdmin1
kafkaConsumerFactory1 --> kafkaTransactionManager1
kafkaConsumerFactory1 --> kafkaSaslAuthProperties1
kafkaProducerFactory1 --> kafkaAvroSerdeProvider1
kafkaProducerFactory1 --> kafkaConfiguration
kafkaProducerFactory1 --> kafkaProperties
kafkaTemplate1 --> commonErrorHandler
commonErrorHandler --> kafkaTemplate1
kafkaListenerContainerFactory1 --> kafkaConsumerFactory1
kafkaListenerContainerFactory1 --> kafkaAdmin1
kafkaListenerContainerFactory1 --> kafkaTransactionManager1

' Cluster 2 bean relationships
transactionalOutbox2 --> kafkaTemplate2
kafkaTemplate2 --> kafkaProducerFactory2
kafkaConsumerFactory2 --> kafkaAvroSerdeProvider2
kafkaConsumerFactory2 --> kafkaConfiguration
kafkaConsumerFactory2 --> kafkaAdmin2
kafkaConsumerFactory2 --> kafkaTransactionManager2
kafkaConsumerFactory2 --> awsMskKafkaAuthProperties2
kafkaProducerFactory2 --> kafkaAvroSerdeProvider2
kafkaProducerFactory2 --> kafkaConfiguration
kafkaProducerFactory2 --> kafkaProperties
kafkaTemplate2 --> commonErrorHandler
commonErrorHandler --> kafkaTemplate2
kafkaListenerContainerFactory2 --> kafkaConsumerFactory2
kafkaListenerContainerFactory2 --> kafkaAdmin2
kafkaListenerContainerFactory2 --> kafkaTransactionManager2

note bottom of springBootService
  Beans marked @Primary for a specific cluster when
  default-producer-cluster-override=true is configured
  for that cluster:

  - KafkaTemplate
  - KafkaProducerFactory
  - SenderOptions
  - ReactiveKafkaProducerTemplate
  - TransactionalOutbox and internal outbox beans
end note

@enduml
```

## See also

- [jEAP Messaging Library](index.md) — the parent topic, including the full configuration reference.
- [Signing Messages and Checking Signatures Without jEAP](signing-messages-and-checking-signatures-without-jeap.md)
