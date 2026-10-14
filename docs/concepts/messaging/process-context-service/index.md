# Process Context Service

<a id="context-overview"></a>

## Purpose

The Process Context Service (PCS) makes distributed business processes observable.

## How it works

It collects messages from participating microservices and shows the state of each process and its tasks. A process template
defines how the messages are interpreted. The business services decide and execute their own work;
the PCS observes the process without orchestrating it.

```mermaid
flowchart LR
    Services[Business microservices] -->|Events and commands| PCS[Process Context Service]
    PCS -->|Process state| Users[Business users]
    PCS -->|Snapshots and notifications| PAS[Process Archive Service]
```

The live process view helps users understand what has happened and investigate incomplete processes.
Snapshots capture a process state for long-term archiving by the PAS.

<a id="detailed-documentation"></a><a id="overview"></a><a id="published-event"></a><a id="consumed-messages-task-events--commands"></a><a id="process-definition-process-template"></a><a id="process"></a><a id="tasks"></a><a id="state-transitions-of-a-task"></a><a id="tasks-planned-by-messages"></a><a id="task-instantiation-conditions-from-version-720"></a><a id="task-completion-via-message-domain-event"></a><a id="observation-tasks"></a><a id="instantiation-condition-from-v720"></a><a id="task-data-from-pcs-version-930"></a><a id="user-data-from-pcs-version-930"></a><a id="messages"></a><a id="correlation-provider"></a><a id="correlation-by-process-id-vs-correlation-by-process-data"></a><a id="payloadextractor"></a><a id="referenceextractor"></a><a id="processdata"></a><a id="relation-patterns"></a><a id="relation-patterns-with-multiple-processdatakeys"></a><a id="determining-relations-via-jointype-from-version-7110"></a><a id="relationpatterns-with-feature-flag-from-pcs-v1312"></a><a id="process-completion-from-pcs-v519"></a><a id="process-completion-via-a-message"></a><a id="process-completion-via-a-custom-condition"></a><a id="process-completion-when-all-tasks-are-completed"></a><a id="default-process-completion"></a><a id="process-snapshots"></a><a id="process-snapshot-creation-upon-process-completion"></a><a id="process-archive-rest-interface-for-process-snapshots"></a><a id="receiving-encrypted-kafka-records-with-jeap-messaging"></a><a id="messagefilter"></a><a id="configuration-of-the-s3-storage-for-process-snapshots"></a><a id="notification-of-process-snapshot-creation"></a><a id="ui"></a><a id="deep-links"></a><a id="traceid-information-and-link-to-the-logging-system-splunkaws-cloudwatch"></a><a id="changes-to-existing-templates-migration"></a><a id="metrics"></a><a id="counters"></a><a id="timers"></a>

## Documentation

- [Service documentation](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-process-context-service/)
- [Getting started](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-process-context-service/getting-started)
