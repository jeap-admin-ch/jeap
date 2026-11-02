# How-Tos: REST APIs & Web

Building and publishing HTTP APIs, and real-time updates to the browser.

- [Enable HTTP compression](../../concepts/rest-apis/http-compression.md) for a Spring Boot server and its REST clients.
- [Publish an OpenAPI spec to the Architecture Repository](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-open-api-publisher-starter/getting-started) — add the starter, enable publishing, configure OAuth2.
- [Push resource-change events to the browser](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-server-sent-events/getting-started) and subscribe to them, via Server-Sent Events.

## Known gaps — no how-to exists yet

See [`doc-refactoring-plan.md`](https://github.com/jeap-admin-ch/jeap/blob/main/doc-refactoring-plan.md)
for the full list and status. Notably missing: a concrete Java/Spring walk-through of adding a new,
backward/forward-compatible REST API version (the existing page narrates the Expand/Migrate/Contract
approach but gives no code-level steps), and a troubleshooting guide for a failed OpenAPI publish.
