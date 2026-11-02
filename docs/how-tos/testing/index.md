# How-Tos: Testing

Business-process test automation across applications.

- [Build a Business-Process-Test orchestrator service](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-bptest-orchestrator/getting-started) and implement a `TestCaseBaseInterface`.
- Turn a Spring Boot service into a test agent ([jeap-bptestagent-api](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-bptestagent-api/getting-started)) by implementing `TestAgentOperations`.
  - [Send notifications and logs back to the orchestrator](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-bptestagent-api/orchestrator-callbacks) from a test agent.

## Known gaps — no how-to exists yet

See [`doc-refactoring-plan.md`](https://github.com/jeap-admin-ch/jeap/blob/main/doc-refactoring-plan.md)
for the full list and status. Notably missing: a clean "write your first consumer-driven contract
(Pact) test" how-to — the real procedure exists but is split across an explanation-heavy page and a
separate page bundling several already-clean recipes (pin the main branch via the Pact CLI, override
consumer version selectors, debug a provider test in IntelliJ, fix mock-server connection issues) with
Pact-concept background. A dedicated interaction-tests how-to is also missing despite a page titled for
one — it is purely conceptual, with no implementation steps.
