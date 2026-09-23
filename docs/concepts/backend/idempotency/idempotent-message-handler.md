# Idempotent Message Handler

## Overview

To simplify the implementation of idempotent message processing, jEAP provides the Java annotation `@IdempotentMessageHandler`. Within the configured retention period, it can ensure that a message handler method executes successfully at most once for a given idempotence ID and message type. This is achieved by recording successfully processed messages in a database, so that a message is not processed again if it has already been recorded in the database. Recurring messages are recognized based on their idempotence IDs and message types.

The `@IdempotentMessageHandler` annotation can relieve a microservice from having to extend its persistent business data with the idempotence IDs of processed messages.

## Integration

The current implementation of the `@IdempotentMessageHandler` annotation requires an SQL database accessed via JPA/JDBC.

### Maven Dependency

The `@IdempotentMessageHandler` annotation is part of a module of the jEAP Messaging Library and can be added to a project in Maven as follows:

```xml
<dependency>
    <groupId>ch.admin.bit.jeap</groupId>
    <artifactId>jeap-messaging-idempotence</artifactId>
</dependency>
```

### Database

To provide its functionality, the `@IdempotentMessageHandler` annotation requires its own tables in the database. For this, the following DDL script must be run against the database (see [`V1_0_0__create-idempotent-processing-schema.sql`](https://github.com/jeap-admin-ch/jeap-messaging/blob/main/jeap-messaging-idempotence/src/test/resources/db/migration/common/V1_0_0__create-idempotent-processing-schema.sql) in the jeap-messaging repository):

```sql
-- The size restrictions on the composite primary key fields of the idempotent_processing table
-- are due to requirements of the AWS Database Migration Service (DMS). For more information, see:
-- https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Validating.html
-- Select sizes that suit your specific needs while ensuring compliance with DMS requirements
-- if you plan to use AWS DMS for database migration or validation.
CREATE TABLE  idempotent_processing
(
    idempotence_id         text           NOT NULL,
    idempotence_id_context text           NOT NULL,
    created_at             timestamp with time zone NOT NULL,
    CONSTRAINT pk_idempotent_processing PRIMARY KEY (idempotence_id, idempotence_id_context)
);

CREATE TABLE shedlock (
    name                VARCHAR(64)                 NOT NULL,
    lock_until          TIMESTAMP                   NOT NULL,
    locked_at           TIMESTAMP                   NOT NULL,
    locked_by           VARCHAR(255)                NOT NULL,
    PRIMARY KEY (name)
);
```

If the `shedlock` table already exists, e.g. because the Transactional Outbox is also used, it doesn't need to be added a second time.

The idempotent message handler implementation uses JPA and declares the entities it needs via `@EntityScan`. If the application in which `@IdempotentMessageHandler` is to be used also uses JPA but doesn't declare a specific `@EntityScan` itself, the application's `SpringBootApplication` class must additionally be annotated with `@EntityScan`, to replicate Spring Boot's default behavior when no explicit entity declaration is present.

In the database, the message type without the major version (e.g. **JmeDeclarationCreatedEvent** without **V2**) is stored as the idempotence context. This ensures idempotency across all major versions of a message, since all major versions of a message type share one idempotence context. This creates the prerequisite for expanding the publisher first before subscribers migrate individually, as part of Expand-Migrate-Contract (TODO Link).

Examples:

| Message Type | idempotence_id_context |
| --- | --- |
| JmeDeclarationCreatedEvent | JmeDeclarationCreatedEvent |
| JmeDeclarationCreatedV2Event | JmeDeclarationCreatedEvent |
| JmeCreateDeclarationCommand | JmeCreateDeclarationCommand |
| JmeCreateDeclarationV2Command | JmeCreateDeclarationCommand |
| JmeCreateDeclarationV3Command | JmeCreateDeclarationCommand |

### Usage

The `@IdempotentMessageHandler` annotation can be used in an application as follows:

```java
...
class SomeMessageTypeListener implements MessageListener<SomeMessageType> {

	@Transactional
	@IdempotentMessageHandler
	public void receive(SomeMessageType message) {

		// process the message and change some persistent state

	}
	...
}
```

:::warning
The processing of the message must happen within a transaction. This can either be started directly by the message handler method annotated with `@IdempotentMessageHandler`, or it can already be active before the method is called.
:::

:::warning
The message handler method annotated with `@IdempotentMessageHandler` must have the return type `void`, and the method's signature must list the message to be processed as the first parameter. Any additional parameters are allowed.
:::

:::warning
The `@IdempotentMessageHandler` annotation is not inherited, i.e. it has no effect when placed on an interface method or an abstract method, for example. As an alternative, the annotation can be declared, for example, on a non-abstract method of an abstract class, which then delegates to an abstract method.
:::

### Advice Order

In Spring AOP, the order in which advices of different aspects are executed on a join point is undefined unless explicitly specified. This can, in principle, be a problem when a message handler method is annotated simultaneously with `@IdempotentMessageHandler` and `@Transactional`, since both annotations are associated with advices that are, by default, declared with the same precedence (`Ordered.LOWEST_PRECEDENCE`). However, the transaction management advice must run before the idempotence advice. Accordingly, the precedence of the `@Transactional` annotation must be increased if `@IdempotentMessageHandler` and `@Transactional` are used simultaneously on a message handler method in a microservice. This can be achieved with the following configuration:

```java
...
@EnableTransactionManagement(order = Ordered.LOWEST_PRECEDENCE - 1)
@SpringBootApplication
public class Application {
	public static void main(String[] args) {
		...
	}
}
```

If necessary, the precedence of `@IdempotentMessageHandler` can also be configured (see the `advice-order` configuration property).

### Housekeeping

It doesn't make sense for the mechanism behind the `@IdempotentMessageHandler` annotation to remember indefinitely which messages have already been processed. This would only unnecessarily fill up the database. Usually there's a certain time window during which a message could be received again for processing. In many cases, repeated processing of a message is likely driven by the jEAP Error Handling Service. Accordingly, this time window can often be derived from the retry strategy configuration of the affected error handling service.

The time window can be set via the `idempotent-processing-retention-duration` configuration. A cleanup job regularly (see the `house-keeping-schedule` configuration) deletes records for messages that have exceeded their retention period.

### Configuration

Configuration for cleaning up records of successfully processed messages is relative to the property path: `jeap.messaging.idempotent-processing`

| Property | Description | Default | Type |
| --- | --- | --- | --- |
| house-keeping-schedule | Cron expression that determines when the cleanup jobs should run. | 0 0 4 * * * | Cron expression |
| idempotent-processing-retention-duration | Time period during which messages remain recorded as successfully processed before they may be deleted by a cleanup job. | P30D | Duration |

Configuration of the `@IdempotentMessageHandler` annotation is relative to the property path: `jeap.messaging.idempotent-message-handler`

| Property | Description | Default | Type |
| --- | --- | --- | --- |
| advice-order | Defines the precedence of applying the `@IdempotentMessageHandler` annotation compared to another annotation, when a message handler method is decorated with both annotations at the same time. LOWEST_PRECEDENCE means that the `@IdempotentMessageHandler` annotation runs after annotations with higher precedence, which is desired, for example, in the case of the `@Transactional` annotation. | Ordered.LOWEST_PRECEDENCE | int |

## Usage Notes

- A processed message is only recorded as successfully processed if its surrounding transaction completed successfully. This is typically the case when no error occurred while processing the message.
- If the message handler method is called again with a message already recorded as processed, the message handler method is not executed.
- The `@IdempotentMessageHandler` annotation results in a database query for every message handler method call, in which an attempt is made, before the method executes, to create an IdempotentProcessing record derived from the message, if such a record doesn't already exist. Using the annotation therefore leads to additional latency and additional database load.
- If the IdempotentProcessing record cannot be created, because one already exists or because a lock prevents it, the `@IdempotentMessageHandler` annotation throws an `IdempotentMessageHandlerExecutionSkippedException` and does not execute the annotated message handler. This case generally occurs when a second microservice instance is already processing the same message (type, idempotence ID) at the same time.
- If the processing of a message fails and the surrounding transaction is therefore rolled back, the same message will be processed again by the message handler method on a subsequent call. This is a typical scenario when using the jEAP Error Handling Service.

:::warning
The `@IdempotentMessageHandler` annotation does not relieve message processing from having to compensate for certain side effects that have already occurred in case of an error, such as REST calls or sent messages (when not using the Transactional Outbox).
:::

- If messages are sent via the [Transactional Outbox](../../../building-blocks/index.md), sending the message effectively becomes part of the surrounding transaction, and compensation in case of an error (transaction rollback) becomes unnecessary.

## Example

The microservice `jme-messaging-receiverpublisher-outbox-service` in the example project [jme-messaging-example](https://github.com/jme-admin-ch/jme-messaging-example) shows an example of using the `@IdempotentMessageHandler` annotation together with the Transactional Outbox. This microservice duplicates the functionality of `jme-messaging-receiverpublisher-service`, but additionally persists the declarations, uses the Transactional Outbox to send events, and processes incoming commands in a message handler method annotated with `@IdempotentMessageHandler`. The [README](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/README.md) and the comments in [`CommandListener`](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/jme-messaging-receiverpublisher-outbox-service/src/main/java/ch/admin/bit/jeap/jme/messaging/receiverpublisheroutbox/CommandListener.java) explain the details.
