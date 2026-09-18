# Error Handler of the jEAP Messaging Library

## Overview

> **Warning:** The error handler also works when several messages are polled together. It does not work, however, when several messages are processed together (Spring for Kafka "batch processing"). This is not supported by the [Jeap Messaging Library](../jeap-messaging-library/index.md).

As part of the [Jeap Messaging Library](../jeap-messaging-library/index.md), an error handler is configured. If an error occurs while processing a message, this error handler is called automatically. The error handler then:

- wraps the message that caused the error into a [MessageProcessingFailed Event](message-processing-failed-event.md) and sends it to the [Error Handling Service](error-handling-service.md)
- acknowledges the message on the original topic, so that event processing can continue
- if several messages were polled together across different partitions and topics, sets the offset for the other topics/partitions to the last message that was already successfully consumed

Technically, this is implemented using the [SeekToCurrentErrorHandler](https://docs.spring.io/spring-kafka/api/org/springframework/kafka/listener/SeekToCurrentErrorHandler.html) with a specific handler. No backoff or retry is supported here, since this is handled by the Error Handling Service. If the error handler is not able to send an EventProcessingFailed event, propagation is aborted and the event is not acknowledged. Since event processing is then no longer possible, the application instance is terminated so that it can be restarted by the container platform.

## Integration

### Message Listener

The error handler is used automatically.

```java
@KafkaListener(topics = {TopicConfiguration.NAME})
public void consume(final JmeDeclarationCreatedEvent event, Acknowledgment ack) {
        log.debug("Received event {}", event.getIdentity().getEventId());
        jmeDeclarationCreatedEventListeners.forEach(l -> l.receive(event));
        // Acknowledge event. In case of error, the error handler will take care of acknowledging the event
        ack.acknowledge();
        log.debug("Acknowledged event {}", event.getIdentity().getEventId());
}
```

Note that the acknowledgment must only be performed on successful processing. In particular, no acknowledgment should be done in a `finally` block. If an error occurs while processing the message, the acknowledgment is performed by the error handler once the EventProcessingFailed event has been published successfully. An additional acknowledgment in a `finally` block could lead to the message being lost if an error occurs in the Error Handling Service.

```java
@KafkaListener(topics = {TopicConfiguration.NAME})
public void consume(final JmeDeclarationCreatedEvent event, Acknowledgment ack) {
        log.debug("Received event {}", event.getIdentity().getEventId());
        try {
                jmeDeclarationCreatedEventListeners.forEach(l -> l.receive(event));
        } finally {
            //DO NOT DO THIS!!!! This acknowledge will also be executed when event processing fails!
            ack.acknowledge();
            //DO NOT DO THIS!!!! This acknowledge will also be executed when event processing fails!
        }
        log.debug("Acknowledged event {}", event.getIdentity().getEventId());
}
```

To use the message handler, the receiver must be configured as described under [Jeap Messaging Library](../jeap-messaging-library/index.md).

### Defining custom exceptions and temporary errors for retries

If an exception implements the `MessageHandlerExceptionInformation` interface, the information in the [MessageProcessingFailed Event](message-processing-failed-event.md) is assembled from this information. This allows, for example, temporary errors to be produced. This interface can be implemented by an application's own error classes; alternatively, [MessageHandlerException](https://github.com/jeap-admin-ch/jeap-messaging/blob/main/jeap-messaging-avro-errorevent/src/main/java/ch/admin/bit/jeap/messaging/avro/errorevent/MessageHandlerException.java) provides a ready-made implementation.

By default, the error handler never triggers a retry on its own. It is up to the business applications to decide which kinds of errors are classified as temporary and are therefore candidates for a retry. See the `temporality` attribute in [MessageHandlerException](https://github.com/jeap-admin-ch/jeap-messaging/blob/main/jeap-messaging-avro-errorevent/src/main/java/ch/admin/bit/jeap/messaging/avro/errorevent/MessageHandlerException.java) and [MessageHandlerExceptionInformation](https://github.com/jeap-admin-ch/jeap-messaging/blob/main/jeap-messaging-avro-errorevent/src/main/java/ch/admin/bit/jeap/messaging/avro/errorevent/MessageHandlerExceptionInformation.java#L27).

## Error Stack Trace Hashing (from jEAP Messaging version 8.7.0)

The error handler can compute a hash from the stack trace of the exception that caused the error and embed it in the MessageProcessingFailedEvent. If two errors have the same hash, it can be assumed that the exceptions occurred at the same place in the code and describe the same problem. Such exceptions can then be shown grouped together in the [Error Handling Service](error-handling-service.md).

For this to work correctly, "variable" parts of the stack traces must be excludable from the hash computation. Exclusion patterns can be defined for this purpose, allowing certain stack trace lines to be ignored. An exclusion pattern is a regular expression (per the Java `Pattern` class) over a fully-qualified class name with an appended method name, i.e. the input for the pattern matching can look like this: `ch.admin.bit.mypackage.MyClass.myMethod`

Stack trace hashing can be configured with the following properties under the prefix `jeap.messaging.kafka.`:

| Property Name | Description | Default | Example |
| --- | --- | --- | --- |
| `errorStackTraceHashEnabled` | Should a stack trace hash be computed, or not? | true | false |
| `errorStackTraceHashDefaultExclusionPatterns` | The list of predefined default exclusion pattern strings (can be replaced if needed) | `^java.base/.*`, `^org.springframework.aop..*`, `.*\$\$FastClassByCGLIB\$\$.*`, `.*\$\$EnhancerBySpringCGLIB\$\$.*`, `.*\$\$EnhancerByCGLIB\$\$.*`, `.*\$\$SpringCGLIB\$\$.*` | |
| `errorStackTraceHashAdditionalExclusionPatterns` | A list of additional exclusion pattern strings (user-defined extension of the default exclusion patterns) | | `^org.springframework..*`, `^ch.admin.bit.mypackage..*` |

## Example

The [jme-messaging-example](https://github.com/jme-admin-ch/jme-messaging-example) integrates error handling. Depending on the content of the message, the jme-messaging-subscriber throws different exceptions (see [ExampleController.java](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/jme-messaging-subscriber-service/src/main/java/ch/admin/bit/jeap/jme/messaging/receiver/ExampleController.java)). [jme-messaging-error-scs](https://github.com/jme-admin-ch/jme-messaging-example/tree/main/jme-messaging-error-scs) is the instance of the Error Handling Service in this example.

## Further reading

- [Spring for Apache Kafka Documentation](https://docs.spring.io/autorepo/docs/spring-kafka-dist/2.6.x/reference/html/)
