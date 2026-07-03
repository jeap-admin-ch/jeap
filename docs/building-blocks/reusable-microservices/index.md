# Reusable Microservices

Ready-made **service templates**: each is a complete, deployable Spring Boot application
that you run as its own service. The common usage model is to **depend on the template,
then add specific configuration** (and, for some, plugin implementations). For libraries
you add inside your own service, see [Libraries](../libraries/index.md).

| Service                              | Purpose                                                                                                                                                       | Source                                                                          |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| jeap-error-handling                  | Process faulty messages: retry for temporary issues, persistence and retry/handling for permanent errors.                                                     | [GitHub](https://github.com/jeap-admin-ch/jeap-error-handling)                  |
| jeap-process-context-service         | Store and retrieve context information for cross-service processes in an event-driven architecture (choreography over orchestration). Extensible via plugins. | [GitHub](https://github.com/jeap-admin-ch/jeap-process-context-service)         |
| [jeap-process-archive-service](https://jeap-admin-ch.github.io/docs/jeap-process-archive-service/) | Archive artifacts pertaining to a process (for audit or business requirements). Extensible via plugins.                                                       | [GitHub](https://github.com/jeap-admin-ch/jeap-process-archive-service)         |
| jeap-message-exchange-service        | Exchange incoming and outgoing messages with external parties via an HTTP-based messagebox API.                                                               | [GitHub](https://github.com/jeap-admin-ch/jeap-message-exchange-service)        |
| jeap-message-contract-service        | Manage messaging contracts used in compatibility checks upon deployment, similar to consumer-driven contract testing.                                         | [GitHub](https://github.com/jeap-admin-ch/jeap-message-contract-service)        |
| jeap-archrepo-service                | Centralized system for automatically managing and documenting the application architecture inventory.                                                         | [GitHub](https://github.com/jeap-admin-ch/jeap-archrepo-service)                |
| jeap-deploymentlog-service           | Trace the deployments of microservices across stages.                                                                                                         | [GitHub](https://github.com/jeap-admin-ch/jeap-deploymentlog-service)           |
| jeap-governance-service              | Quick overview of system and service compliance with defined policies. Extensible via plugin implementations.                                                 | [GitHub](https://github.com/jeap-admin-ch/jeap-governance-service)              |
| [jeap-opensearch-index-writer-service](https://jeap-admin-ch.github.io/docs/jeap-opensearch-index-writer-service/) | Event-driven indexing of search items into OpenSearch.                                                                                                        | [GitHub](https://github.com/jeap-admin-ch/jeap-opensearch-index-writer-service) |
| jeap-oauth-mock-server               | Configurable OAuth2/OpenID-Connect server for local development and testing.                                                                                  | [GitHub](https://github.com/jeap-admin-ch/jeap-oauth-mock-server)               |

## Business process testing

| Building block           | Purpose                                                                                                                           | Source                                                              |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| jeap-bptest-orchestrator | Orchestrator for automated business process tests (the top of the test pyramid: testing the interaction of several applications). | [GitHub](https://github.com/jeap-admin-ch/jeap-bptest-orchestrator) |
| [jeap-bptestagent-api](https://jeap-admin-ch.github.io/docs/jeap-bptestagent-api/)     | TestAgent API used by the business-process-test orchestrator.                                                                     | [GitHub](https://github.com/jeap-admin-ch/jeap-bptestagent-api)     |

## Related

- [Libraries](../libraries/index.md) and [Spring Boot Starters](../spring-boot-starters/index.md) — what you add inside
  a service.
- [App Building Blocks](../index.md) — overview of all categories.
