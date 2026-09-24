# Interaction Tests

Interaction tests verify that a microservice interacts correctly with other microservices. In particular, they check whether the microservice triggers follow-up events or requests to other APIs.

Important:

- The microservice is tested in isolation — no chained scenarios with other microservices.
- The test should ideally run locally, and therefore quickly — the goal is not to test integration with the infrastructure, but whether the interactions with other microservices actually take place.
- An interaction test is a JUnit test, more precisely an integration test (suffix `IT`).

Motivation: many small, simple tests instead of a few large, complex end-to-end tests.

## Test Scope

![Compatibility vs Interaction](interaction-tests-compatibility-vs-interaction.png)

## Use Cases

### Handling Requests

```plantuml
@startuml
left to right direction
skinparam linetype ortho
skinparam nodesep 40
skinparam ranksep 30
skinparam rectangle {
  BorderColor Black
}
skinparam component {
  BorderColor Black
}
component "Test" as n1 #ffe599
component "RestController" as n0
component "Service" as n2
component "Repository" as n4
rectangle "Microservice under Test" as n5 #9fc5e8
component "KafkaTemplate" as n6
rectangle "Expected\nMessage" as n7 #b6d7a8
rectangle "EmbeddedKafka" as n8
component "Consumer\nMock" as n10 #f4cccc
component "WebClient" as n3
component "Provider Mock\n(e.g. WireMock)" as n9 #f4cccc

n1 -[bold]-> n0
n0 --> n2
n2 --> n3
n2 --> n4
n4 --> n5
n2 --> n6
n6 -[bold]-> n7
n7 -[bold]-> n8
n3 -[bold]-> n9
n8 -[bold]-> n10

n1 -[hidden]-> n0
n0 -[hidden]-> n2
n2 -[hidden]-> n4
n4 -[hidden]-> n5
n5 -[hidden]-> n6
n6 -[hidden]-> n7
n7 -[hidden]-> n8
n8 -[hidden]-> n10
n10 -[hidden]-> n3
n3 -[hidden]-> n9
@enduml
```

**Verify**

- Correct response?
- Were the expected requests to other APIs triggered?
  - Request parameters filled in correctly (1)
- Were the expected commands triggered?
  - Command payload filled in correctly (1)
- Were the expected events triggered?
  - Event payload filled in correctly (1)
- Is the status of the service correct? (1)

(1) Interaction tests should primarily verify that the interactions take place and that the required data is passed on. The concrete values should only be verified as far as necessary in the interaction test, so that the interaction tests remain robust against changes to the domain logic.

### Handling Commands/Events

```plantuml
@startuml
left to right direction
skinparam linetype ortho
skinparam nodesep 40
skinparam ranksep 30
skinparam rectangle {
  BorderColor Black
}
skinparam component {
  BorderColor Black
}
component "Test" as n11 #ffe599
component "Repository" as n3
rectangle "Tested\nMessage" as n10 #ffe599
rectangle "EmbeddedKafka" as n12
rectangle "Microservice under Test" as n4 #9fc5e8
component "KafkaListener" as n0
component "MessageHandler" as n1
component "WebClient" as n2
component "Provider Mock\n(e.g. WireMock)" as n8 #f4cccc
component "KafkaTemplate" as n5
rectangle "Expected\nMessage" as n6 #b6d7a8
rectangle "EmbeddedKafka" as n7
component "Consumer\nMock" as n9 #f4cccc

n0 --> n1
n1 --> n2
n1 --> n3
n3 --> n4
n1 --> n5
n5 -[bold]-> n6
n6 -[bold]-> n7
n2 -[bold]-> n8
n7 -[bold]-> n9
n11 -[bold]-> n10
n10 -[bold]-> n12
n12 -[bold]-> n0
@enduml
```

**Verify**

- Message is processed
- Were the expected requests to other APIs triggered?
  - Request parameters filled in correctly (1)
- Were the expected commands triggered?
  - Command payload filled in correctly (1)
- Were the expected events triggered?
  - Event payload filled in correctly (1)
- Is the status of the service correct? (1)

(1) Interaction tests should primarily verify that the interactions take place and that the required data is passed on. The concrete values should only be verified as far as necessary in the interaction test, so that the interaction tests remain robust against changes to the domain logic.

### Interaction Test Example

```plantuml
@startuml
left to right direction
skinparam linetype ortho
skinparam nodesep 40
skinparam ranksep 30
skinparam rectangle {
  BorderColor Black
}
skinparam component {
  BorderColor Black
}
component "Test" as n7 #ffe599
rectangle "Tested\nCommand" as n6 #ffe599
rectangle "EmbeddedKafka" as n8
component "WebClient" as n1
component "Provider Mock\n(e.g. WireMock)" as n4 #ffe599
component "ExampleService" as n0
rectangle "Expected\nEvent" as n2 #b6d7a8
rectangle "EmbeddedKafka" as n3
component "Test Consumer\nMock" as n5 #ffe599

n0 --> n1
n0 -[bold]-> n2
n2 -[bold]-> n3
n1 -[bold]-> n4
n3 -[bold]-> n5
n7 -[bold]-> n6
n6 -[bold]-> n8
n8 -[bold]-> n0
@enduml
```
