# How-Tos: Architecture & Observability

Tracking and understanding what runs where: the architecture repository, deployment log, reaction
tracking, governance, and logging.

- [Construct a working log deep link](../../concepts/logging/log-deep-links.md) — build a Splunk/CloudWatch link that jumps straight to the relevant log entries.
- [Expose monitoring endpoints](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-monitoring-starter) — add the monitoring starter, set the Prometheus/actuator password, generate build info.
- [Register a service with Spring Boot Admin](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-monitoring-starter) — client configuration and exposing the Actuator endpoints it needs.
- [Embed an Architecture Repository instance](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-archrepo-service/getting-started) in a system, and verify it with a first import.
- [Embed a Deployment Log Service instance](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-deploymentlog-service/getting-started) end to end (technical user, Confluence root page, DB, API users, recording a first deployment).
- Track what reacts to what at runtime:
  - [Embed a Reaction Observer Service instance](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-reaction-observer-service/getting-started).
  - [Use the Reaction Observer client library](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-reaction-observer/getting-started) to have a service publish reaction events automatically.
- [Write a custom Governance Service plugin](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-governance-service/plugin-mechanism) — a `DataSourceImporter`, `ComponentDeletionListener` or `SystemDeletionListener`.
