# Business Process Testautomation

## Goal

The automated business process tests (Business Process Tests) are intended to test the interaction between different business applications, and they form the top of the test pyramid. Functional correctness should not be verified in the business process tests.

## Architecture Overview

![Architecture Overview](architecture-overview.svg)

### Component Responsibilities

| Component | Responsibilities |
| --- | --- |
| TestOrchestrator | - Orchestrates the test of the business process<br/>- Interacts with the TestAgents of the business applications via a simple, standardized REST API<br/>- Exposes a simple, standardized REST API so that TestAgents can report statuses and data from the business application back to the orchestrator |
| Business application A & B | The individual microservices of the business applications should not need to be adapted for the business process tests. There may be individual exceptions. |
| TestAgent A & B | - Enables the Test Orchestrator to interact with the business application.<br/>- Exposes a simple, standardized REST API that can be used by the Test Orchestrator<br/>- Notifies statuses and data to the REST API of the Test Orchestrator |
| JIRA | Jira (with the ZephyrScale plugin) acts as the reporting tool. The test results are transferred automatically by the TestOrchestrator via REST API after every test run. |

## Test Orchestrator

To implement a Test Orchestrator, the jEAP library [jeap-bptest-orchestrator](https://github.com/jeap-admin-ch/jeap-bptest-orchestrator) can be used. This in turn has a dependency on the jEAP library [jeap-bptestagent-api](https://github.com/jeap-admin-ch/jeap-bptestagent-api), which can also be used for the TestAgents.

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
component "jeap-bptestagent-api" as n1
component "jeap-bptest-orchestrator" as n0
component "your_own_orchestrator" as n2

n0 -[dashed]-> n1
n2 -[dashed]-> n0

n1 -[hidden]-> n0
n0 -[hidden]-> n2
@enduml
```

### Build your own Orchestrator

#### Organizational

Since an orchestrator operates across business applications, it must be decided where it should be hosted. Reporting is done via the Jira plugin ZephyrScale. This means a Jira project must also exist to which the orchestrator can deliver its report (to send the test report to Jira, a technical Jira user is required).

The following questions must be answered:

- Where are the test cases documented?
- In which project are the test runs reported?
- In which repository is the source code for the TestOrchestrator created?
- Where is the TestOrchestrator deployed?

#### Technical

**See [jeap-bptest-orchestrator — Getting started](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-bptest-orchestrator/getting-started)**
for the step-by-step setup and configuration reference.

### Test-Support

To make it easy to test test-case implementations, the `jeap-bptest-orchestrator` project provides three helper classes: [TestCaseRunner](https://github.com/jeap-admin-ch/jeap-bptest-orchestrator/blob/main/jeap-bptest-orchestrator/src/main/java/ch/admin/bit/jeap/testorchestrator/testsupport/TestCaseRunner.java), [TestCaseMockTool](https://github.com/jeap-admin-ch/jeap-bptest-orchestrator/blob/main/jeap-bptest-orchestrator/src/main/java/ch/admin/bit/jeap/testorchestrator/testsupport/TestCaseMockTool.java) and [TestCaseTestBase](https://github.com/jeap-admin-ch/jeap-bptest-orchestrator/blob/main/jeap-bptest-orchestrator/src/main/java/ch/admin/bit/jeap/testorchestrator/testsupport/TestCaseTestBase.java):

#### TestCaseRunner

With a `TestCaseRunner` instance, the flow of a test case can be simulated in a unit test for the test-case implementation under test. In doing so, the `prepare`, `execute`, `verify` and `cleanUp` phases are run through in a way comparable to `TestCaseService`.

The Test-Case-Runner also takes over the reception and distribution of events, so that no Spring context needs to be started up for the unit test. To do so, Spring application events must be published via the Test-Case-Runner's `ApplicationEventPublisher` (`getApplicationEventPublisher()`). For notifications from simulated Test Agents, the methods `notify(NotificationDto)` and `notifyAsync(NotificationDto, long, TimeUnit)` are available.

Test execution can be either synchronous (`run(TestCaseBaseInterface)`) or asynchronous (`runAsync(TestCaseBaseInterface)`). Asynchronous notifications are only allowed during asynchronous test execution. For most test cases, synchronous execution should be sufficient.

The Test-Case-Runner is stateful, and a single instance can only be used for one test execution.

The two examples [OrderBillingHappyPathTest](https://github.com/jme-admin-ch/jme-bptest-example/blob/main/jme-bptest-orchestrator/src/test/java/ch/admin/bit/jeap/jme/bptest/orchestrator/testcases/OrderBillingHappyPathTest.java) and [OrderBillingHappyPathAsyncTest](https://github.com/jme-admin-ch/jme-bptest-example/blob/main/jme-bptest-orchestrator/src/test/java/ch/admin/bit/jeap/jme/bptest/orchestrator/testcases/OrderBillingHappyPathAsyncTest.java) should show how to use the Test-Case-Runner.

#### TestCaseMockTool

Communication of a test case with the Test Agents is usually done exclusively via a Test-Agent-Web-Client. Accordingly, by mocking this client, the interaction between the test case and the Test Agents can be simulated and verified in a unit test in an almost arbitrary way, in a simple manner.

The test-support class `TestCaseMockTool` provides a collection of methods that can be used to simulate and verify the typical interactions between a test case and the Test Agents via a *Mockito* mock of the Test-Agent-Web-Client. The example [OrderBillingHappyPathTest](https://github.com/jme-admin-ch/jme-bptest-example/blob/main/jme-bptest-orchestrator/src/test/java/ch/admin/bit/jeap/jme/bptest/orchestrator/testcases/OrderBillingHappyPathTest.java) should make the use of the Test-Case-Mock-Tool clear. Of course, the Test-Agent-Web-Client mock used in a unit test does not need to be configured and verified exclusively with methods of the Test-Case-Mock-Tool; if needed, the mock can also be configured and verified directly via the *Mockito* API.

#### TestCaseTestBase

A simple abstract base class for test-case unit-test classes. For every test-method execution, it provides the following things pre-initialized:

- an instance of `TestCaseRunner`
- an instance of `TestCaseMockTool`
- the test ID under which the `TestCaseRunner` will execute the test case
- a Mockito mock of `TestAgentWebClient`
- a Mockito mock of `TestReportService`

## Test Agent / Test Simulator

:::info
A simulator is the same as a TestAgent, with the only difference being that it does not call any further services.
:::

As a rule, one Test Agent is built per business application. Every TestAgent is based on the jEAP library [jeap-bptestagent-api](https://github.com/jeap-admin-ch/jeap-bptestagent-api), which defines the API for the orchestrator.

- The TestAgent enables the Business Test Orchestrator to interact with the business application.
- The TestAgent exposes a simple, standardized REST API that is called by the Test Orchestrator.
- The TestAgent notifies statuses and data to the REST API of the Test Orchestrator.
- The TestAgent can deliver log messages to the orchestrator. These are persisted in the orchestrator.

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
component "jeap-bptestagent-api" as n1
component "your_own_testagent" as n0

n0 -[dashed]-> n1

n1 -[hidden]-> n0
@enduml
```

### TestAgent API

The REST API for the orchestrator is defined by the following interface (source: [TestAgentOperations.java](https://github.com/jeap-admin-ch/jeap-bptestagent-api/blob/main/src/main/java/ch/admin/bit/jeap/testagent/api/TestAgentOperations.java) in `jeap-bptestagent-api`, branch `main`):

```java
package ch.admin.bit.jeap.testagent.api;

import ch.admin.bit.jeap.testagent.api.act.ActionDto;
import ch.admin.bit.jeap.testagent.api.act.ActionResultDto;
import ch.admin.bit.jeap.testagent.api.prepare.PreparationDto;
import ch.admin.bit.jeap.testagent.api.prepare.PreparationResultDto;
import ch.admin.bit.jeap.testagent.api.update.DynamicDataDto;
import ch.admin.bit.jeap.testagent.api.verify.ReportDto;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Tag(name = "TestAgent API", description = """
        Every TestAgent/Simulator implements this API. \
        The Orchestrator uses this API to orchestrate the Business Process Tests\
        """)
@RequestMapping(value = "/api/tests")
public interface TestAgentOperations {

    @Operation(summary = "Prepare")
    @PutMapping("/{testId}")
    ResponseEntity<PreparationResultDto> prepare(@PathVariable String testId, @RequestBody PreparationDto preparationDto);

    @Operation(summary = "Update")
    @PutMapping("/{testId}/dynamicdata")
    void update(@PathVariable String testId, @RequestBody DynamicDataDto dynamicDataDto);

    @Operation(summary = "Act")
    @PostMapping("/{testId}/actions")
    ResponseEntity<ActionResultDto> act(@PathVariable String testId, @RequestBody ActionDto actionDto);

    @Operation(summary = "Verify")
    @GetMapping("/{testId}/report")
    ResponseEntity<ReportDto> verify(@PathVariable String testId);

    @Operation(summary = "Clean up")
    @DeleteMapping("/{testId}")
    void cleanUp(@PathVariable String testId);

}
```

| Name | Method | Resource | Request Body | Response | Purpose |
| --- | --- | --- | --- | --- | --- |
| Prepare | PUT | `/api/tests/<test_id>` | [PreparationDto](https://github.com/jeap-admin-ch/jeap-bptestagent-api/blob/main/src/main/java/ch/admin/bit/jeap/testagent/api/prepare/PreparationDto.java) | [PreparationResultDto](https://github.com/jeap-admin-ch/jeap-bptestagent-api/blob/main/src/main/java/ch/admin/bit/jeap/testagent/api/prepare/PreparationResultDto.java) | The TestAgent is asked to prepare the business application for a test. Similarly, a simulator can be prepared for a test.<br/>- The request body references an `initialState` known to the Test Agent/Simulator (optionally, the body can contain parameters as key/value pairs)<br/>- The response body allows information about the initial state to be returned to the orchestrator (this information may potentially be required for initializing other business applications) |
| Update | PUT | `/api/tests/<test_id>/dynamicdata` | [DynamicDataDto.java](https://github.com/jeap-admin-ch/jeap-bptestagent-api/blob/main/src/main/java/ch/admin/bit/jeap/testagent/api/update/DynamicDataDto.java) | - | Pass dynamic data to the business application or the simulator (key/value pairs).<br/>This may be necessary if the information (e.g. an id) was not yet known at the start of the process. |
| Act | POST | `/api/tests/<test_id>/actions` | [ActionDto](https://github.com/jeap-admin-ch/jeap-bptestagent-api/blob/main/src/main/java/ch/admin/bit/jeap/testagent/api/act/ActionDto.java) | [ActionResultDto](https://github.com/jeap-admin-ch/jeap-bptestagent-api/blob/main/src/main/java/ch/admin/bit/jeap/testagent/api/act/ActionResultDto.java) | Trigger an action on the test.<br/>- The request body references the action known to the TestAgent/Simulator (optionally, the body can contain parameters as key/value pairs)<br/>This is used to trigger an action on a simulator or a business application that is required for the process to continue. |
| Verify | GET | `/api/tests/<test_id>/report` | - | [ReportDto](https://github.com/jeap-admin-ch/jeap-bptestagent-api/blob/main/src/main/java/ch/admin/bit/jeap/testagent/api/verify/ReportDto.java) | Verify whether the expectations (data, interactions) were met:<br/>- whether the business application or the simulator has reached the expected state<br/>- whether the expected interactions (with the simulator) have taken place |
| CleanUp | DELETE | `/api/tests/` | - | - | Delete test data |

### Build your own TestAgent

:::info
Reference implementations of two TestAgents can be found in the [jme-bptest-example](https://github.com/jme-admin-ch/jme-bptest-example) example ([jme-bptest-billing-testagent-service](https://github.com/jme-admin-ch/jme-bptest-example/tree/main/jme-bptest-billing-testagent-service), [jme-bptest-order-testagent-service](https://github.com/jme-admin-ch/jme-bptest-example/tree/main/jme-bptest-order-testagent-service)).
:::

## Links

| Link | Description |
| --- | --- |
| [jeap-bptestagent-api](https://github.com/jeap-admin-ch/jeap-bptestagent-api) | API definition between the orchestrator and TestAgents / simulators |
| [jeap-bptest-orchestrator](https://github.com/jeap-admin-ch/jeap-bptest-orchestrator) | jEAP library as the basis for implementing an orchestrator |
| [jme-bptest-example](https://github.com/jme-admin-ch/jme-bptest-example) | Example with 2 test agents and an orchestrator implementation |
