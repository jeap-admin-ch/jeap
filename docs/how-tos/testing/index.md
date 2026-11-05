# How-Tos: Testing

Business-process test automation and consumer-driven contract testing across applications.

- [Build a Business-Process-Test orchestrator service](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-bptest-orchestrator/getting-started) and implement a `TestCaseBaseInterface`.
- Turn a Spring Boot service into a test agent ([jeap-bptestagent-api](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-bptestagent-api/getting-started)) by implementing `TestAgentOperations`.
  - [Send notifications and logs back to the orchestrator](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-bptestagent-api/orchestrator-callbacks) from a test agent.
- [Write a Pact consumer test](write-a-pact-consumer-test.md) — record the requests a consumer sends and the responses it expects, as a contract for the provider to verify against.
- [Write a Pact provider test](write-a-pact-provider-test.md) — verify a provider's real behavior against the pacts its consumers recorded, including provider-state methods.
