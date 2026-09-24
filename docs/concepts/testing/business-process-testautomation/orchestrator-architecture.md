# jEAP BusinessTest Orchestrator - Architecture

## Context

### External View

```plantuml
@startuml
title System Overview

skinparam componentStyle rectangle
skinparam shadowing false
left to right direction

actor "Jenkins" as Jenkins
actor "Browser (Swagger)" as Browser

component "<<your_own_orchestrator_impl>>" as OrchestratorImpl
component "YOUR_OWN_ORCHESTRATOR" as Orchestrator
component "jeap-test-orchestrator-service" as OrchestratorService
component "Jira Zephyr" as JiraZephyr

component "TestAgent A" as TestAgentA
component "TestAgent B" as TestAgentB

package "Business Application A" {
  component "Microservice A" as AppAMicroservice1
  component "Microservice A" as AppAMicroservice2
  component "Microservice A" as AppAMicroservice3
}

package "Business Application B" {
  component "Microservice B" as AppBMicroservice1
  component "Microservice B" as AppBMicroservice2
  component "Microservice B" as AppBMicroservice3
}

Jenkins --> OrchestratorImpl : startTest (orchestrator API)
Browser --> OrchestratorImpl : startTest (orchestrator API)

OrchestratorImpl --> OrchestratorService : <<uses>>
OrchestratorImpl --> JiraZephyr : zephyr API

OrchestratorImpl --> TestAgentA : testAgent API
OrchestratorImpl --> TestAgentB : testAgent API

TestAgentA --> AppAMicroservice1 : testAgent API
TestAgentA --> AppAMicroservice2 : testAgent API
TestAgentA --> AppAMicroservice3 : testAgent API

TestAgentB --> AppBMicroservice1 : testAgent API
TestAgentB --> AppBMicroservice2 : testAgent API
TestAgentB --> AppBMicroservice3 : testAgent API

TestAgentA --> OrchestratorImpl : notify and log (orchestrator API)
TestAgentB --> OrchestratorImpl : notify and log (orchestrator API)

note right of OrchestratorImpl
  orchestrator API
end note

@enduml
```

### Interfaces

#### Orchestrator REST API

| Operation | Method | Path | Description |
| --- | --- | --- | --- |
| `startTest` | POST | `/api/tests/{testCaseName}` | Starts a test run for the test case `testCaseName`.<br/>A `testId` is generated and returned. |
| `notifyEvent` | POST | `/api/tests/{testId}/notifications`<br/>Body:<br/>`{`<br/>`testId: <testId>,`<br/>`notification: <the Notification>`<br/>`producer: <which TestAgent>`<br/>`data: Map<Key, Value>`<br/>`}`<br/>[`NotificationDto.java`](https://github.com/jeap-admin-ch/jeap-bptestagent-api/blob/main/src/main/java/ch/admin/bit/jeap/testagent/api/notification/NotificationDto.java) | The test agent/simulator reports an event/state/progress of the business application.<br/>These events allow the orchestrator to:<br/>- trigger actions so the process can continue (e.g. simulate an arrival)<br/>- detect the progress of the test<br/><br/>This avoids the orchestrator having to poll the test agent to detect whether a given state has been reached. |
| `log` | POST | `/api/tests/<testId>/logs`<br/>Body:<br/>`{`<br/>`logMessage: <logMessage>,`<br/>`logLevel: <logLevel>,`<br/>`source: <testAgentName>`<br/>`}`<br/>[`LogDto.java`](https://github.com/jeap-admin-ch/jeap-bptestagent-api/blob/main/src/main/java/ch/admin/bit/jeap/testagent/api/notification/LogDto.java) | Test agents can report events and intermediate steps to the orchestrator.<br/>The orchestrator passes these messages 1:1 to the logger.<br/>Logs from the test agents are persisted in the orchestrator DB. |

## Building Block View

## Class Diagram

The class diagram only shows a partial excerpt, meant to illustrate how the framework and the test case implementation relate to each other.

Not shown in the diagram: all helper classes and domain classes (see the domain model for those).

```plantuml
@startuml
title Class Diagram

skinparam classAttributeIconSize 0
hide circle

package "your_own_orchestrator" {

  class TestCaseController {
    + startTestRun()
    + notifyEvent()
    + logEvent()
  }

  class YourTestCaseImplementation {
    - testRun
    + getTestCaseName()
    + prepare()
    + execute()
    + verify()
    + cleanUp()
    + onApplicationEvent(notificationEvent: NotificationEvent)
  }

  class SomeOtherTestCase {
    - testRun
  }
}

package "jeap-bptest-orchestrator" {

  interface TestCaseBaseInterface {
    + getTestCaseName()
    + getJiraProjectKey()
    + getZephyrTestCaseKey()
    + prepare()
    + execute()
    + verify()
    + cleanUp()
  }

  class TestCaseService {
    + startTestRun()
    + onApplicationEvent(executeDoneEvent: ExecuteDoneEvent)
    + logTestRun()
  }

  class TestAgentWebClient {
    - prepare()
    - act()
    - update()
    - verify()
    - cleanUp()
  }

  class ZephyrWebClient {
    + testRun
  }

  class TestReportService {
    + persistTestResult()
    + reportToJira()
  }

  class NotificationEvent
  class ExecuteDoneEvent

  interface "ApplicationListener<NotificationEvent>" as NotificationEventListener
  interface "ApplicationListener<ExecuteDoneEvent>" as ExecuteDoneEventListener
}

YourTestCaseImplementation ..|> TestCaseBaseInterface
SomeOtherTestCase ..|> TestCaseBaseInterface

YourTestCaseImplementation ..|> NotificationEventListener
TestCaseService ..|> ExecuteDoneEventListener

TestCaseController --> TestCaseService : starts

TestCaseService --> TestAgentWebClient : uses
TestCaseService --> TestReportService : uses
TestReportService --> ZephyrWebClient : uses

TestCaseService --> TestCaseBaseInterface : manages
TestAgentWebClient --> TestCaseBaseInterface : invokes

YourTestCaseImplementation --> NotificationEvent : receives
TestCaseService --> ExecuteDoneEvent : receives

note right of TestCaseController
  orchestrator:
    testAgents:
      TestAgentA: https://www.ssss.ch
      TestAgentB: www.ssss.ss
end note

@enduml
```

## Domain Model

```plantuml
@startuml
title Domain Model

skinparam classAttributeIconSize 0
hide circle

class TestCase {
  + name: String
  + jiraProjectKey: String
  + zephyrTestCase: String
  + testAgents: List<TestAgent>
}

class TestRun {
  + id: String
  + state: String
  + startedAt: DateTime
  + endedAt: DateTime
  + environment: String
  + testData: Map<String, String>
}

class Report {
  + id: String
  + detailText: String
}

enum Conclusion {
  FAIL
  PASS
}

class Result {
  + name: String
  + detail: String
}

class Logs {
  + level: String
  + msg: String
}

class TestStep {
  + index: Integer
  + status: String
  + comment: String
}

class TestCaseRecord {
  + name: String
  + status: String
  + actualResult: String
  + environment: String
  + actualStartDate: DateTime
  + actualEndDate: DateTime
  + comment: String
}

TestCase "1" --> "0..*" TestRun : testRuns
TestRun "0..1" --> "1" Report : report
Report "1" --> "1..*" Result : results
Report "1" --> "1" Conclusion : conclusion
TestRun "1" --> "0..*" Logs : logs
TestCase "1" --> "1..*" TestStep : testSteps

note "Zephyr report data model" as ZephyrNote
ZephyrNote ..> TestCaseRecord
ZephyrNote ..> TestStep

@enduml
```

## Sequence Diagram

```plantuml
@startuml
title TestCase Execution Flow

actor JenkinsOrManual as "Jenkins or manual"
participant Controller as "TestCaseController"
participant Service as "TestCaseService"
participant TestCase as "TestCaseXY"
participant AgentClient as "TestAgentWebClient"
participant ReportClient as "ZephyrReportWebClient"
actor TestAgent as "TestAgentXY"

autonumber

JenkinsOrManual -> Controller: POST /api/tests/testCaseXY
activate Controller

Controller -> Service: startTestRun(TestCaseXY, testId)
activate Service

Service -> TestCase: prepare
activate TestCase

TestCase -> AgentClient: /prepare("TestAgentA", "DEV")
AgentClient --> TestCase: prepared

Service -> TestCase: execute
TestCase -> AgentClient: act("TestAgentA", ...)
AgentClient --> TestCase: execution started

TestAgent -> Controller: POST /api/tests/{testId}/notifications
Controller -> TestCase: notify
TestCase -> Service: event: executeDone

Service -> TestCase: verify
Service -> ReportClient: report
Service -> TestCase: cleanUp

TestCase --> Service: completed
Service --> Controller: completed

deactivate TestCase
deactivate Service
deactivate Controller

@enduml
```
