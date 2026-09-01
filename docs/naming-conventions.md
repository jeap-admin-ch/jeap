# Naming Conventions

Consistent names make a system landscape easier to understand and let tooling attribute components
to systems automatically. Apply them wherever **interfaces or externally visible artifacts** are
published — deployables, message types, Kafka topics. Naming *inside* a single microservice is left
to the team, as long as it is consistent.

This page covers only the conventions that jEAP components or tooling actually rely on. Naming of
infrastructure resources (Keycloak realms/clients, database clusters, object-storage buckets, Git
repositories/projects) is a platform concern and is documented with the respective platform, not
here.

> The concrete examples use placeholder agency and system names (`bazg`, `eets`, `vsp`, …);
> substitute your own.

## Glossary

| Term | Example | Meaning |
|---|---|---|
| `context` | `assessment`, `discrepancy` | A bounded context — typically the domain a microservice encapsulates. |
| agency | `BAZG`, `BIT` | The organization (federal office) that owns the application. |
| `system` | `EETS`, `VSP` | The business application. |
| service | `eets-assessment-service` | A single microservice. |

## Deployable elements

Services, frontends and other individually deployable elements.

### Standardized type ids

| Type id | Description |
|---|---|
| `service` | Microservice without a UI |
| `ui` | Single-page application |
| `scs` | Self-contained system (backend **and** UI) |
| `mobileapp` | Mobile app |
| `gateway` | API gateway |

If no standardized type fits, propose a new one to the jEAP team rather than inventing a local one.

### Convention

| Status | Element | Convention | Example | Rationale |
|---|---|---|---|---|
| MUST | Individually deployable / runnable elements | `<system>-<context>-<typeid>` — `system` matching `[a-z]+[a-z0-9_]*`, `context` matching `[a-z]+[a-z0-9-]*`, `typeid` from the table above | `eets-assessment-service`, `eets-assessment-ui`, `eets-manualtask-connector-service` | Attribution to the system; the kind of component is visible in the name. The name is also used as the Spring application name — the id under which the service appears in monitoring and distributed tracing. |

## Message types

### Domain events

| Status | Element | Convention | Example | Rationale |
|---|---|---|---|---|
| MUST | All events (internal / external) | `<System><EventName>` — `System` matching `[A-Z][a-z0-9_]*` is the publishing or defining system; `EventName` in CamelCase. `System` is omitted for event types published by many different systems (e.g. the framework's error-handling event). | `JmeDeclarationCreatedEvent` | Clear attribution to a system where possible. |
| MUST | Event name | `<BusinessObject><VerbPastTense>[V<version>]Event` — the version is added only for a new major version (see [parallel change](https://martinfowler.com/bliki/ParallelChange.html)) | `DeclarationCreatedEvent`; new major version: `DeclarationCreatedV2Event` | Uniformity; the business meaning is recognizable from the name. |

### Commands

| Status | Element | Convention | Example | Rationale |
|---|---|---|---|---|
| MUST | All commands (internal / external) | `<System><CommandName>` — `System` matching `[A-Z][a-z0-9_]*` is the receiving or defining system; `CommandName` in CamelCase. `System` is omitted for framework command types used by many systems. | `JmeCreateDeclarationCommand` | Clear attribution to a system where possible. |
| MUST | Command name | `<Verb><BusinessObject>[V<version>]Command` — the version is added only for a new major version (see [parallel change](https://martinfowler.com/bliki/ParallelChange.html)) | `CreateDeclarationCommand`; new major version: `CreateDeclarationV2Command` | Uniformity; the business meaning is recognizable from the name. |

## Kafka topics

Topic naming is documented with the messaging library — see
[jeap-messaging](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/).

## Pact participants

The consumer/provider names jEAP registers on the Pact Broker (used by the deployment pipeline's
`can-i-deploy` checks and by the governance service) follow
`{agency}-{spring.application.name}[_{apiName}]`, e.g. `bazg-agir-task-scs`,
`bazg-agir-task-scs_apiA`.

## Commit messages

| Status | Convention | Example | Rationale |
|---|---|---|---|
| MUST | The commit message contains the issue-tracker id when one exists | `TASK-1234 Add button` | jEAP's deployment-log and changelog tooling extracts the id to link a deployment to its issues and to compute lead time. |

## PostgreSQL default schema

jEAP configures the PostgreSQL default schema as **`data`** (not `public`, which is deprecated since
PostgreSQL 15) — applied by `jeap-spring-boot-db-migration-starter` and
`jeap-spring-boot-postgresql-aws-starter`.

## See also

- [Documenting jEAP](documenting-jeap.md) — how jEAP documentation is written and published.
- [Using jEAP](using-jeap.md) — the Maven parents and dependency management.
