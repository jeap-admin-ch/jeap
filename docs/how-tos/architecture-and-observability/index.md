# How-Tos: Architecture & Observability

Tracking and understanding what runs where: the architecture repository, deployment log, reaction
tracking, governance, and logging.

- [Construct a working log deep link](../../concepts/logging/log-deep-links.md) — build a Splunk/CloudWatch link that jumps straight to the relevant log entries.
- [Embed an Architecture Repository instance](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-archrepo-service/getting-started) in a system, and verify it with a first import.
- [Embed a Deployment Log Service instance](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-deploymentlog-service/getting-started) end to end (technical user, Confluence root page, DB, API users, recording a first deployment).
- Track what reacts to what at runtime:
  - [Embed a Reaction Observer Service instance](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-reaction-observer-service/getting-started).
  - [Use the Reaction Observer client library](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-reaction-observer/getting-started) to have a service publish reaction events automatically.
- [Write a custom Governance Service plugin](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-governance-service/plugin-mechanism) — a `DataSourceImporter`, `ComponentDeletionListener` or `SystemDeletionListener`.

## Known gaps — no how-to exists yet

See [`doc-refactoring-plan.md`](https://github.com/jeap-admin-ch/jeap/blob/main/doc-refactoring-plan.md)
for the full list and status. Notably missing: a single walkthrough wiring Prometheus + Grafana + Spring
Boot Admin into a new microservice (today split across three reference-heavy pages), a "query the
Reaction Observer REST API for a specific task" how-to, and a renaming/merging-systems walkthrough for
the Deployment Log Service.

## Housekeeping (not a how-to gap, but found during this audit)

- `jeap-deploymentlog-service` and `jeap-reaction-observer-service` both have a real `docs/` folder with
  a `getting-started.md`, but their `README.md` does not link it — the doc link table is missing
  entirely, so a reader following only the README would conclude there is no documentation. See
  [`doc-refactoring-plan.md`](https://github.com/jeap-admin-ch/jeap/blob/main/doc-refactoring-plan.md).
