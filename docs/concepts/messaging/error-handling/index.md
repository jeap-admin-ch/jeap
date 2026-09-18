# Error Handling

## Overview

### Motivation

In a system landscape with an event-driven architecture, many **event-driven** business processes run (e.g. events on crossing a border, ...). These business events are often processed **automatically** and without user interaction as an [event](../index.md). An event often triggers further business events, so that a chain of events results. A problem that every application has to solve: what happens on **processing errors**? Events must **not be lost**, since an event that is lost is never processed and the process it belongs to then stalls.

### How it Works

```plantuml
@startuml
skinparam linetype ortho
skinparam nodesep 40
skinparam ranksep 30
skinparam rectangle {
  BorderColor Black
}
skinparam component {
  BorderColor Black
}
rectangle "Agir\nTask-Management\nUI" as n9 #cfe2f3
rectangle "Agir\nTask-Management\nService" as n5 #cfe2f3
() "Get Task Details /\nUpdate Task" as n10c
actor "User" as n10
rectangle "Error Handling UI" as n8 #cfe2f3
() "Create / Close\nManual Task" as n7c
rectangle "Topics mit\nfachlichen Events" as n0 #D9A741
rectangle "Error Handling Topic" as n2 #D9A741
rectangle "Business Microservice" as n1 #cfe2f3
rectangle "Error Handling Service" as n3 #cfe2f3
database "Database" as n6

n0 -[dashed,bold]-> n1
n1 -[dashed,bold]-> n2
n2 -[dashed,bold]-> n3
n10c -- n5
n6 -- n3
n3 -[dashed]-> n0 : "[Retry after Temporary or Permanent Error]\nResend Event to Originating Topic"
n7c -- n3
n3 -[dashed,bold]-> n10c
n8 -[dashed,bold]-> n7c
n9 -[dashed,bold]-> n10c
n10 -[dashed,bold]-> n9
n10 -[dashed,bold]-> n8

n9 -[hidden]-> n5
n5 -[hidden]-> n10
n10 -[hidden]-> n10c
n10c -[hidden]-> n8
n8 -[hidden]-> n7c
n7c -[hidden]-> n0
n0 -[hidden]-> n2
n2 -[hidden]-> n1
n1 -[hidden]-> n3
n3 -[hidden]-> n6
@enduml
```

As part of the [Jeap Messaging Library](../jeap-messaging-library/index.md), an error handler is automatically configured (see [Error Handler of the jEAP Messaging Library](error-handler-of-the-jeap-messaging-library.md)). If an application throws an exception while processing an event, the exception is caught by the error handler. The error handler then sends a [MessageProcessingFailed Event](message-processing-failed-event.md) to a configurable error topic and acknowledges receipt of the original event. This lets the application's event processing continue for further events without blocking.

A separate [Error Handling Service](error-handling-service.md) then reads the MessageProcessingFailed events from the topic and stores them in its own database. The Error Handling Service can then:

- On temporary errors, write the original event back into the original topic after a certain time, so that the event is processed again.
- Convert temporary errors that have occurred repeatedly into permanent errors.
- On permanent errors, create a task so that an employee can take care of the problem.

## Integration

To integrate error handling into your own business applications, the following steps must be carried out:

- An error topic must be ordered.
- A user with write access to all topics that the Error Handling Service needs to be able to resend events to must be provided for the Error Handling Service.
- Roles must be configured in PAMS for the Error Handling Service (see [Error Handling Service > OAuth](error-handling-service.md#oauth)).
- The [Jeap Messaging Library](../jeap-messaging-library/index.md) must be configured in every service that processes events.
- A dedicated instance of the Error Handling Service must be instantiated (see [Error Handling Service > Integration](error-handling-service.md#integration)).

## Example

Error handling is integrated in [jme-messaging-example](https://github.com/jme-admin-ch/jme-messaging-example). Depending on the content of the event, the jme-event-receiver throws different exceptions (see [ExampleController.java](https://github.com/jme-admin-ch/jme-messaging-example/blob/main/jme-messaging-subscriber-service/src/main/java/ch/admin/bit/jeap/jme/messaging/receiver/ExampleController.java). [jme-messaging-error-scs](https://github.com/jme-admin-ch/jme-messaging-example/tree/main/jme-messaging-error-scs) is the instance of the Error Handling Service in this example.
