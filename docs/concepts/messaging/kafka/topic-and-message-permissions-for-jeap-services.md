# Topic & Message Permissions for jEAP Services

## Introduction

Some [jEAP Reusable Microservices](../../../using-jeap.md)
and jEAP libraries — such as the
System Behaviour Documentation (TODO Link) or
[Error Handling](../error-handling/index.md) — produce or consume Kafka messages that are technical in
nature, or that are used in most jEAP services via a library, so no messaging contract is available for
these events.

It is **important to take these topics into account when provisioning topic access permissions** for a jEAP microservice.

Also, if you want to configure a list of allowed publishers for a message (see the [Jeap Messaging
Library](../jeap-messaging-library/index.md) configuration), consider these internal events.

> Topics with messaging contracts are NOT documented on this page, since these are considered well-known to
> the DevOps team operating a system. For these topics, a messaging contract annotation will have been added
> in the producer/consumer service.
>
> These topics are also documented in the generated documentation if you use the
> Arch Repo (TODO Link) service.

## jEAP service topics without messaging contracts

Note: `<system>` below denotes the prefix used for a given business application ("Fachapplikation"), based
on the [Naming Conventions](../../naming-conventions.md) for topics.

| # | Producer (write permission) | Consumer (read permission) | Topics | Allow publisher for message | Documentation link |
| --- | --- | --- | --- | --- | --- |
| 1 | **All** jEAP-based microservices integrating the jEAP Reaction Observer Library | jEAP **Reaction Observer Service** for a program/department | `applicationplatform-reaction-identified`<br/>`applicationplatform-reactions-observed` | No configuration required for DevOps teams. The Reaction Observer Service will not check the allowed publisher for these messages. | System Behaviour Documentation (TODO Link) |
| 2 | **All** jEAP-based microservices in a system using jEAP messaging to consume Kafka messages | jEAP **Error Handling Service** instance for a system | `<system>-messageprocessing-failed`<br/>(your topic might be named differently, please check!) | **Do not add the MessageProcessingFailedEvent to the list of allowed publishers.** This allows all publishers for this event, which is fine because the MPFE wraps a message that will be checked for authenticity/authorization by the consumer. | [Error Handling](../error-handling/index.md) |
| 3 | jEAP **Error Handling Service** instance for a system | **All** jEAP-based microservices in a system using jEAP messaging to consume Kafka messages | All topics consumed by #2, typically `<system>-*`, but also topics consumed from other systems (`<other-system>-<context>-<messagename>`)<br/>`<system>-messageprocessing-deadletter`<br/>`<system>-messageprocessing-failed`<br/>(your topic might be named differently, please check!) | n/a. The Error Handling Service re-produces the original event 1:1, including the original signature header and publisher name in the payload. The EHS is never the "publisher" of an event. | [Error Handling](../error-handling/index.md) |
| 4 | jEAP **Process Context Service** instance for a system | `<system>-process-outdated-internal`: jEAP **Process Context Service** instance for a system. Other topics: services consuming the events — they will need a messaging contract and should be visible in the generated documentation. | `<system>-process-processoutdated-internal`<br/>`<system>-process-snapshotcreated`<br/>(your topics might be named differently, please check!) | In the PCS config: all events consumed in the template must have an allowed-publisher entry for their producer; the PCS requires to be allowed to publish its own events (ProcessContextOutdatedEvent, ProcessContextStateChangedEvent). For services consuming events from the PCS: they will have a contract for these events (e.g. ProcessSnapshotCreatedEvent) and need to allow the PCS to publish them. | [Process Context Service](../process-context-service/index.md) |
