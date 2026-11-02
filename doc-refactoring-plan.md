# jEAP Documentation Refactoring Plan — JEAP-7611

**Not published to the doc site** (not under `docs/`) — this is an internal working document tracking
the how-tos cleanup. Context: [JEAP-7611](https://jira.bit.admin.ch/browse/JEAP-7611).

## What this is

A full audit of the jEAP documentation corpus (this repo's `docs/concepts/**` plus every component
repo's `docs/`) against the [Diataxis](https://diataxis.fr/) framework, done to build the
[How-Tos index](docs/how-tos/index.md). A page only counts as a clean, indexable **how-to** if it is
predominantly task-oriented steps toward one goal, without being padded with reference tables
(config/API/data-model) or explanatory background (design rationale, how a mechanism works) — a short
"why" sentence is fine, a whole section of either is not.

This document records, per page, what the audit found and what would need to happen to get the rest of
the corpus into the same state: extracting a clean how-to out of a mixed page, writing a how-to that
doesn't exist at all, or a plain documentation-hygiene fix. Each row below becomes a candidate follow-up
ticket, to be created and approved individually.

**Placement rule:** a how-to belongs in its building block's own repo unless there is a good reason it
doesn't have one — it genuinely spans several building blocks (e.g. Kafka integration: `jeap-messaging` +
the Message Type Registry + the Error Handling Service), or it covers something no repo owns (e.g.
Keycloak admin-console configuration). Everything else moves to the owning repo rather than growing a
second copy in `jeap`.

## Extraction progress across repos

Branches exist on `jeap`, `jeap-messaging`, `jeap-spring-boot-starters` and `jeap-internal-spring-boot-parent`
(all `feature/JEAP-7611-how-tos`, none committed yet). 16 of the ~118 mixed/gap rows below have been
extracted or merged so far:

- **Stayed in `jeap`** (multi-building-block or no owning repo): the flagship Kafka-integration merge —
  `jeap`'s and `jeap-messaging`'s two drifted `kafka-how-to.md` copies combined into one canonical
  `docs/how-tos/messaging/integrate-kafka-into-a-service.md` — plus EMC Message Evolution, token
  introspection enable/debug, the Keycloak introspection-client steps, and the audience-restriction
  migration guide (all Keycloak-admin-console-adjacent, no owning repo).
- **Moved to `jeap-messaging`**: the idempotent message handler, declaring message contracts, multi-cluster
  Kafka configuration and self-message EMC evolution were each single-`jeap-messaging`-feature content
  that had been duplicated into `jeap`. The duplicate `jeap` pages were deleted; the corresponding
  `jeap-messaging` docs (`idempotent-message-handler.md`, `message-contracts.md`, `configuration.md`,
  `message-evolution.md`) were enriched with anything `jeap`'s copy had that theirs didn't (the
  bean-injection table and Lombok caveat for multi-cluster; the full before/after schema and rollout steps
  for self-messages); `jeap`'s own concept pages now link out to them instead.
- **Moved to `jeap-spring-boot-starters`**: feature flags and monitoring endpoints / Spring Boot Admin
  registration, same pattern — the `jeap` duplicates were deleted, and `docs/jeap-spring-boot-featureflag-starter.md`
  (custom activation strategy) / `docs/jeap-spring-boot-monitoring-starter.md` (password generation,
  build-info, Spring Boot Admin registration) were enriched with the missing procedural detail.
- **Added to `jeap-internal-spring-boot-parent`, deliberately not yet linked from `jeap`**: 4 new pages
  covering what was bundled in `jeap-pact-integration-details.md` (setting a pacticipant's main branch,
  overriding consumer version selectors, running/debugging provider tests in IntelliJ, fixing mock-server
  connection issues), linked from that repo's README and from its existing `pact-broker.md`. **`jeap`'s
  copy was deliberately left untouched** — see "Rollout independence" below.

### Rollout independence

Each repo's branch must be mergeable/deployable on its own, in any order, without the jEAP site build
breaking (cross-repo doc links are validated at site-build time — see [Publishing](https://github.com/jeap-admin-ch/jeap/blob/main/docs/concepts/documenting-jeap.md#publishing)).
Concretely: **`jeap` must never link to a page or anchor that is new in this refactoring and doesn't yet
exist on another repo's default branch.** Two cases came up:

- A link can safely drop a **new anchor** and fall back to the bare page when the page itself already
  existed (done for Spring Boot Admin registration → links to `jeap-spring-boot-monitoring-starter`
  without the new `#registering-with-spring-boot-admin` fragment).
- A link to a **brand-new page** has no safe fallback. For the 4 Pact how-tos, `jeap`'s side of the split
  (trimming `jeap-pact-integration-details.md` and adding the links) was **reverted** — the page is back
  to its original, pre-session content. The new pages in `jeap-internal-spring-boot-parent` ship
  independently either way; `jeap`'s trim-and-link edit is a **follow-up**, to be applied only once that
  repo's branch is live.

The other moves (idempotent handler, message contracts, multi-cluster config, self-message evolution,
feature flags, monitoring endpoints) were checked and are safe as-is: every link/anchor they use already
existed on the target repo's default branch before this session (the branches only added prose *under*
those existing headings, never introduced the heading itself).
- **Not extracted, duplicate resolved the same way**: the OAuth2 mock-server "create an instance" steps and
  the Business Process Test orchestrator build steps each turned out to have a single clear owning
  building block (`jeap-oauth-mock-server`, `jeap-bptest-orchestrator`) whose own getting-started already
  covered the same ground — no `jeap` copy was ever kept; the corresponding `jeap/docs/concepts/**`
  sections point at the component repo's page.

The remaining ~103 rows are unchanged from the audit.

## Status legend

| Symbol | Meaning |
|---|---|
| ✅ | Done — indexed in `docs/how-tos/` on this branch |
| 🔶 | Split needed — page mixes a real how-to with reference/explanation |
| ❌ | Gap — no how-to exists for this task; write one from scratch |
| 🧹 | Housekeeping — not a how-to issue, a plain doc-hygiene fix |
| ⚪ | No action — correctly reference/explanation, not a how-to candidate (listed only where the filename is misleading) |

## Summary

| Area | Indexed ✅ | Extracted/moved ✅ (these branches) | Split needed 🔶 | Gaps ❌ | Housekeeping 🧹 |
|---|---|---|---|---|---|
| `jeap` (this repo) `docs/concepts/**` | 6 | 5 (stayed here) + 6 (moved out, see below) | 9 | 7 | 0 |
| `jeap-messaging` | 4 | 4 (received from `jeap`: idempotent handler, message contracts, multi-cluster config, self-message evolution) | 7 | 2 | 0 |
| `jeap-spring-boot-starters` | 11 | 2 (received from `jeap`: feature flags, monitoring endpoints + Spring Boot Admin) | ~30 (incl. 14 per-module starter pages) | 7 | 0 |
| Libraries (11 other repos) | 11 | 0 | 13 | 10 | 0 |
| Reusable Microservices (14 repos) | 17 | 0 | 13 | 9 | 2 |
| Tooling & Registries (13 repos) | 7 | 0 | 9 | 0 | 2 |
| **Total** | **~56** | **17** | **~81** | **~35** | **4** |

(The 6 "moved out" rows from `jeap` are counted again under their new home, so they're not double-counted
in the total.)

Four repos (`jeap-renovate-presets`, `jeap-python-pipeline-lib`, `jeap-central-publishing-maven-plugin`,
`jeap-license-template`) have no `docs/` at all yet — out of scope for extraction (nothing to extract),
noted for the repo owners.

---

## A. `jeap` (this repo) — `docs/concepts/**`

| Page | Verdict | Action needed | Status |
|---|---|---|---|
| `authentication-and-authorization/audience-restriction/audience-configuration-in-keycloak.md` | Clean how-to | — | ✅ Indexed (Security) |
| `authentication-and-authorization/audience-restriction/audience-for-token-introspection-on-keycloak.md` | Mixed | Extract: create the introspection client in Keycloak. Leave behind: Keycloak compatibility-options explanation. | ✅ Extracted → [configure-keycloak-introspection-client.md](docs/how-tos/security/configure-keycloak-introspection-client.md) |
| `authentication-and-authorization/audience-restriction/audience-introduce-for-existing-resources.md` | Mixed | Extract: the numbered migration procedure (inventory → identifiers → deploy receivers → issue audiences → align callers → verify → enforce). Leave behind: goal-selection guidance, troubleshooting tables. | ✅ Extracted (whole page relocated) → [migrate-to-audience-restriction.md](docs/how-tos/security/migrate-to-audience-restriction.md); original path kept as a redirect stub |
| `authentication-and-authorization/audience-restriction/audience-naming.md` | Explanation/Reference | None — not a how-to despite the filename. | ⚪ |
| `authentication-and-authorization/authorization-servers/authorizing-keycloak-clients-for-consuming-applications-resources.md` | Explanation | None — not a how-to despite the filename. | ⚪ |
| `authentication-and-authorization/authorization-servers/integrating-different-authorization-servers.md` | Mixed | Extract: implement a custom claim-set converter. Leave behind: claim-set-converter concept + config reference. | 🔶 |
| `authentication-and-authorization/calling-secured-rest-apis-from-java.md` | Mixed | Extract: the worked call-a-secured-API examples as a how-to. Leave behind: config-property and factory-method reference tables. | 🔶 |
| `authentication-and-authorization/protecting-rest-apis/rest-api-authentication-and-authorization.md` | Mixed | Extract: customizing `EntryPoint`/`AccessDeniedHandler`/`MethodSecurityExpressionHandler` as a how-to. Leave behind: config-property reference, authorization-location explanation. | 🔶 |
| `authentication-and-authorization/protecting-rest-apis/rest-api-authorization-with-authorities.md` | Mixed | Extract: declarative/programmatic integration steps. Leave behind: `AuthoritiesResolver` API reference. | 🔶 |
| `authentication-and-authorization/protecting-rest-apis/rest-api-authorization-with-semantic-roles.md` | Mixed | Extract: the integration step. Leave behind: query-method reference table. | 🔶 |
| `authentication-and-authorization/protecting-rest-apis/rest-api-authorization-with-simple-roles.md` | Mixed | Same pattern as semantic-roles. | 🔶 |
| `authentication-and-authorization/testing/oauth2-mock-server.md` | Mixed | Extract: the 4-step "Usage" setup. Leave behind: config/example reference. | ⚪ Not extracted — **confirmed duplicate** of `jeap-oauth-mock-server/docs/getting-started.md` (already indexed). Per the building-block placement rule, `jeap-oauth-mock-server` is the single clear owner; this page's "Usage" section now points there directly instead of carrying its own copy. |
| `authentication-and-authorization/testing/testing-secured-rest-apis.md` | Mixed | Split: the 5 test-use-case recipes into standalone how-tos. Leave behind: test-support class reference. | 🔶 |
| `authentication-and-authorization/tokens/minimizing-access-token-sizes.md` | Mixed | Split: each sub-task (dynamic scopes, lightweight tokens, roles pruning) into its own how-to. | 🔶 |
| `authentication-and-authorization/tokens/token-introspection.md` | Mixed | Extract: "How to enable jEAP token introspection" and "How to debug..." as standalone how-tos. Leave behind: introspection-mode/metrics/config reference. | ✅ Extracted → [enable-and-debug-token-introspection.md](docs/how-tos/security/enable-and-debug-token-introspection.md) |
| `backend/idempotency/idempotent-message-handler.md` | Mixed, duplicate | **Confirmed duplicate of `jeap-messaging/docs/idempotent-message-handler.md`.** | ✅ Moved — single building block (`jeap-messaging`). `jeap`'s copy trimmed to a pointer; `jeap-messaging`'s copy was already complete, no changes needed there. |
| `config-secrets-management/feature-flags.md` | Mixed, duplicate | Single building block (`jeap-spring-boot-starters`, featureflag starter). | ✅ Moved → `jeap-spring-boot-starters/docs/jeap-spring-boot-featureflag-starter.md`, enriched with the custom-activation-strategy how-to. `jeap`'s copy trimmed to a pointer. |
| `continuous-delivery/expand-migrate-contract.md` | Mixed | Extract: the 4-step EMC Message Evolution procedure. Leave behind: strategy-selection/motivation discussion, replacement-strategy table. | ✅ Extracted → [apply-emc-message-evolution.md](docs/how-tos/messaging/apply-emc-message-evolution.md) |
| `continuous-delivery/zero-downtime-deployments.md` | Explanation | None — not a how-to despite the filename (describes what happens, not what the reader does). | ⚪ |
| `database/postgresql-with-spring-and-flyway.md` | Clean how-to | — | ✅ Indexed (Backend & Data) |
| `frontend/current-user-endpoint.md` | Mixed | Extract: enable/customize steps. Leave behind: attribute reference table. | 🔶 |
| `frontend/direct-frontend-route-navigation-redirect-in-spring-boot-scs.md` | Mixed | Extract: the concrete code fix. Shorten: the "Context"/"Problem" lead-in. | 🔶 |
| `logging/distributed-tracing.md` | Mixed | Extract: integration/config steps. Leave behind: Overview/Instrumentation/Custom Spans explanation. | 🔶 |
| `logging/log-deep-links.md` | Clean how-to | — | ✅ Indexed (Architecture & Observability) |
| `messaging/evolution-of-messages/index.md` | Mixed, single-building-block procedure embedded | The "EMC when Consuming Events Produced in the Same Microservice" procedure is pure `jeap-messaging` mechanics. | ✅ Moved — expanded into `jeap-messaging/docs/message-evolution.md`'s "Self-messages" section (was a 3-sentence pointer, now the full before/after schema + rollout steps). `jeap`'s page trimmed to a pointer; compatibility-rules reference/explanation stays. |
| `messaging/jeap-messaging-library/signing-messages-and-checking-signatures-without-jeap.md` | Clean how-to | — | ✅ Indexed (Security) |
| `messaging/jeap-messaging-library/support-for-multiple-kafka-clusters.md` | Mixed, single-building-block config duplicated | The config example is pure `jeap-messaging` mechanics; `jeap-messaging/docs/configuration.md` already had the YAML but not the bean-injection table or Lombok caveat. **Also:** the page's own example module path could not be verified against the current `jme-messaging-example` repo — doc drift, left as-is, not independently fixed. | ✅ Moved — `jeap-messaging/docs/configuration.md`'s "Clusters" section enriched with the bean-injection table and Lombok caveat. `jeap`'s page trimmed to the diagram + autoconfiguration-internals explanation + a pointer. |
| `messaging/jeap-messaging-library/index.md` | Mixed/sprawling | No single how-to to extract; consider narrowing this page's scope (it currently reads as a full library reference). | 🔶 |
| `messaging/kafka/kafka-how-to.md` | Mixed, **duplicated** | Extract the clean 11-step integration checklist as the canonical Kafka how-to — **pick one owning repo** (recommend `jeap-messaging`, closer to the code) and delete the losing duplicate (see `jeap-messaging/docs/kafka-how-to.md` below — same page, already drifted: different docker-compose examples, different wording). Leave behind / fold into `kafka-consumer-producer-topic-configuration.md`: the topic-settings reference and partition/replication explanation. | ✅ Extracted & merged → [integrate-kafka-into-a-service.md](docs/how-tos/messaging/integrate-kafka-into-a-service.md), combining both repos' checklists and the better (KRaft) docker-compose example. This repo's page is now reference-only. `jeap-messaging`'s own copy still needs trimming to point here — separate repo, follow-up ticket. |
| `messaging/kafka/index.md` | Mixed | Fold "Starting Kafka locally" into the canonical Kafka how-to above. Leave behind: topic-naming reference. | ✅ Extracted |
| `messaging/message-contracts/index.md` | Mixed, duplicate | **Confirmed duplicate** of the core annotation syntax in `jeap-messaging/docs/message-contracts.md`, which was already complete there. | ✅ Moved — the "Declaring Message Contracts" section now points to `jeap-messaging`'s page; no changes needed there. The PCS/PAS template-annotation example (`@JeapMessageConsumerContractsByTemplates`) stayed here, since `jeap-messaging`'s own docs explicitly call PCS/PAS "out of scope" and this content is genuinely about configuring those two reusable microservices, not the library in general. |
| `messaging/message-type-registry/installing-message-types-locally.md` | Clean how-to | — | ✅ Indexed (Messaging) |
| `monitoring/monitoring-endpoints.md` | Mixed, duplicate | Single building block (`jeap-spring-boot-starters`, monitoring starter). | ✅ Moved → `jeap-spring-boot-starters/docs/jeap-spring-boot-monitoring-starter.md`, enriched with the password-generation command and build-info Maven snippet it was missing. `jeap`'s copy trimmed to a pointer. |
| `monitoring/spring-boot-admin.md` | Mixed, duplicate | Client-registration steps are `jeap-spring-boot-monitoring-starter`-specific (server setup is third-party, nothing jEAP-specific to extract there). | ✅ Moved → new "Registering with Spring Boot Admin" section in `jeap-spring-boot-starters/docs/jeap-spring-boot-monitoring-starter.md`. `jeap`'s copy trimmed to a pointer. |
| `rest-apis/http-compression.md` | Clean how-to | — | ✅ Indexed (REST APIs & Web) |
| `rest-apis/openapi-documentation.md` | Mixed | Extract: the Integration section steps. Leave behind: OpenAPI object/tag/operation/schema property reference tables. | 🔶 |
| `testing/business-process-testautomation/index.md` | Mixed | Extract: the "Build your own Orchestrator" 1–6 step procedure. Leave behind: goal/architecture/component-responsibility explanation. | ⚪ Not extracted — **confirmed duplicate** of `jeap-bptest-orchestrator`'s own getting-started (already indexed). Per the building-block placement rule, `jeap-bptest-orchestrator` is the single clear owner; this section now points there directly instead of carrying its own copy. |
| `testing/consumer-driven-contract-tests/index.md` | Mixed | Extract: "Create Consumer/Provider Tests" steps as how-to(s). Leave behind: motivation/big-picture/provider-states explanation. | 🔶 |
| `testing/consumer-driven-contract-tests/jeap-pact-integration-details.md` | Mixed bundle, single-building-block procedures | The 4 bundled recipes (main branch via Pact CLI, overriding consumer version selectors, debugging in IntelliJ, fixing mock-server connection issues) are all about overriding/using `jeap-internal-spring-boot-parent`'s own Pact preconfiguration. | 🟡 Half done — the 4 pages exist in `jeap-internal-spring-boot-parent/docs/` (`pact-main-branch.md`, `pact-consumer-version-selectors.md`, `pact-provider-tests-in-intellij.md`, `pact-mock-server-connection-issues.md`), linked from its README and `pact-broker.md`, and can ship on their own. **`jeap`'s page is untouched on purpose** — trimming it and linking out must wait until that repo's branch is live, or `jeap`'s site build would reference pages that don't exist yet. Follow-up: once merged, trim `jeap`'s copy the same way as the other moved rows. |
| `testing/interaction-tests.md` | Explanation (misleading title) | This page itself **is** the gap — it reads like "how to write an interaction test" but has zero implementation steps. Either add them here or point to where they actually live. | ❌ |
| `testing/unit-integration-testing-with-kafka.md` | Mixed/cookbook | The 7-item "General Recommendations" list is a cookbook of independent techniques, not one task — keep as a reference cookbook rather than forcing a single how-to. Split out the unrelated mock-config/base-class topics into their own reference page. | 🔶 |

**Gaps (no page to extract from):**

| Gap | Notes |
|---|---|
| ❌ Security quick-start for a brand-new microservice | Closest page (`rest-api-authentication-and-authorization.md`) is dominated by config reference. |
| ❌ Audience restriction greenfield quick-start | Only a migration guide for *existing* resources exists. |
| ❌ Monitoring end-to-end setup | Prometheus + Grafana + Spring Boot Admin wired into one new service — currently 3 separate reference-heavy pages, no walkthrough. |
| ❌ REST API evolution in practice | `evolution-versioning.md` narrates Expand/Migrate/Contract and versioning rules in prose/tables but gives no concrete Java/Spring steps for adding a new API version. |
| ❌ Clean "write your first Pact test" | Buried half in `consumer-driven-contract-tests/index.md` (half motivational) — becomes moot once that page is split above. |
| ❌ Kafka integration, steps-only | No clean version exists anywhere once `kafka-how-to.md` is split — this is the deliverable of that split, tracked here so it isn't lost. |

---

## B. `jeap-messaging`

| Page | Verdict | Action needed | Status |
|---|---|---|---|
| `docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Messaging) |
| `docs/publishing-messages.md` | Clean how-to | — | ✅ Indexed (Messaging) |
| `docs/consuming-messages.md` | Clean how-to | — | ✅ Indexed (Messaging) |
| `docs/encrypting-messages.md` | Clean how-to | — | ✅ Indexed (Security + Messaging) |
| `docs/kafka-how-to.md` | Mixed, **duplicated** | See `jeap/docs/concepts/messaging/kafka/kafka-how-to.md` above — same action, one canonical page. | 🔶 |
| `docs/avro-maven-plugin.md` | Mixed | Extract: "Generating classes from Avro IDL" steps. Leave behind: goals/parameters reference tables. | 🔶 |
| `docs/message-type-registry.md` | Mixed | Extract: the "Maintenance" (checkout/branch/PR) steps. Leave behind: descriptor data-model reference. **Check overlap with `jeap/docs/concepts/messaging/message-type-registry/index.md`.** | 🔶 |
| `docs/message-contracts.md` | Mixed | Extract: "Declaring contracts" steps. Leave behind: how-contracts-work explanation, annotation-processor internals reference. | 🔶 |
| `docs/idempotent-message-handler.md` | Mixed | Extract: the usage snippet. Leave behind: concurrency-semantics/storage reference/explanation. **Check overlap with `jeap/docs/concepts/backend/idempotency/idempotent-message-handler.md`** — likely the same topic documented twice. | 🔶 |
| `docs/health-indicators.md` | Mixed | Extract: the probe-integration snippet. Leave behind: properties reference. | 🔶 |
| `docs/error-handling.md` | Mixed | The real integration how-to is an external link to the EHS getting-started page (already indexed). Extract this page's own "Integration steps" into a short "configure this service's side" how-to; leave the exception-classification explanation/reference behind. | 🔶 |
| `docs/architecture.md`, `dependencies.md`, `configuration.md`, `message-types.md`, `defining-messages.md`, `message-evolution.md`, `kafka-topics-and-configuration.md`, `schema-registry-confluent.md`, `schema-registry-aws-glue.md`, `aws-msk-iam-authentication.md`, `signing-messages.md`, `message-filtering.md`, `testing.md`, `avro-class-security.md` | Reference/Explanation | None — correctly not how-to candidates. | ⚪ |

**Gaps:**

| Gap | Notes |
|---|---|
| ❌ Switching Confluent → AWS Glue + MSK IAM auth | Both target pages are pure property reference; no task-oriented migration walkthrough. |
| ❌ Turning on message signing | `signing-messages.md` explains the mechanism and config, never walks through key generation/cert distribution/enabling it. |

---

## C. Libraries (12 other repos)

| Repo / page | Verdict | Action needed | Status |
|---|---|---|---|
| `jeap-audit/docs/getting-started.md` | Mixed | Split: 3 distinct goals (build-only / send-via-outbox / consume) bundled together — one how-to per goal. | 🔶 |
| `jeap-audit/docs/building-the-command.md` | Mixed | Extract: builder usage. Leave behind: builder-method reference table, event-vs-object-data explanation. | 🔶 |
| `jeap-audit/docs/transactional-outbox.md` | Mixed | Extract: required-setup steps (producer contract, topic config, DB tables). Leave behind: sender-method reference, bean-naming reference. | 🔶 |
| `jeap-audit/docs/consuming-audit-commands.md` | Mixed | Extract: the one-line "mapping a command" how-to. Leave behind: `AuditRecord` model reference. | 🔶 |
| `jeap-audit` — ❌ gap | | No how-to for configuring audit-command encryption via jeap-crypto. | ❌ |
| `jeap-crypto/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Security) |
| `jeap-crypto/docs/database-columns.md` | Clean how-to | — | ✅ Indexed (Security) |
| `jeap-crypto/docs/s3-object-storage.md` | Clean how-to | — | ✅ Indexed (Security) |
| `jeap-crypto/docs/key-management.md` | Mixed/no steps | Backend comparison + caching/escrow rationale + metrics reference; no actionable steps to extract — likely stays explanation. | ⚪ |
| `jeap-crypto` — ❌ gap | | No how-to for rotating a wrapping key (publish a new version / retire an old one, Vault or AWS KMS). | ❌ |
| `jeap-db-schema-publisher/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Backend & Data) |
| `jeap-db-schema-publisher/docs/authentication.md` | Mixed | Extract: config steps. Leave behind: token-uri reference, required-role reference. | 🔶 |
| `jeap-db-schema-publisher` — ❌ gap | | No troubleshooting how-to for a failed/silent schema publish. | ❌ |
| `jeap-initializer/docs/extending.md` | Clean how-to | — | ✅ Indexed (Platform & Tooling) |
| `jeap-initializer/docs/getting-started.md` | Mixed | Extract: add-dependency/configure-template steps. Leave behind: full REST API reference. | 🔶 |
| `jeap-initializer` — ❌ gap | | No step-by-step for authoring a template from scratch (`template-authoring.md` is pure syntax reference). | ❌ |
| `jeap-jwe-client/docs/npm-publishing-setup.md` | Clean how-to | — | ✅ Indexed (Platform & Tooling) |
| `jeap-jwe-client/docs/getting-started.md` | Mixed | Extract: install/register steps. Leave behind: protocol explanation (flow diagram, metadata/header reference). | 🔶 |
| `jeap-jwe-client/docs/development.md` | Mixed | Extract: dev/test/build steps. Leave behind: workspace/npm-scripts reference, CI-pipeline explanation. | 🔶 |
| `jeap-jwe-client/docs/testing.md` | Mixed, misscoped | Covers the library's own test suite, not a consuming app — reclassify or rescope rather than index as a consumer how-to. | 🔶 |
| `jeap-jwe-client/docs/publishing-and-versioning.md` | Mixed | Extract: release steps. Leave behind: version/location reference, Dependabot explanation. | 🔶 |
| `jeap-jwe-client` — ❌ gaps | | No how-to for integration-testing an Angular app that consumes jeap-jwe-client; no explicit backend-facing key-rotation procedure (`key-rotation.md` documents client behavior only). | ❌ |
| `jeap-messaging-outbox/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Messaging) |
| `jeap-messaging-outbox/docs/sending-messages.md` | Mixed | Extract: "send with optional headers" how-to. Leave behind: API/delivery-mode comparison, pros/cons. | 🔶 |
| `jeap-messaging-outbox/docs/failure-handling.md` | Mostly reference | Minimal steps to extract; likely stays reference. | ⚪ |
| `jeap-messaging-outbox/docs/database.md` | Mixed | Extract: the rolling-upgrade procedure. Leave behind: DDL/column reference. | 🔶 |
| `jeap-messaging-outbox/docs/multi-cluster.md` | Mixed | Extract: "selecting a cluster" how-to. Leave behind: bean-registration/fallback explanation. | 🔶 |
| `jeap-messaging-outbox` — ❌ gap | | No how-to for testing outbox-based sending locally (Testcontainers/embedded Kafka). | ❌ |
| `jeap-messaging-sequential-inbox/docs/getting-started.md` | Mixed | Extract: core setup steps (dependency, declaration, handler). Leave behind: DDL block, schema-upgrade note. | 🔶 |
| `jeap-messaging-sequential-inbox` — ❌ gap | | No standalone how-to for the two-phase recording-mode rollout (buried in explanation-heavy `how-it-works.md`) — extract as its own how-to. | ❌ |
| `jeap-opensearch-index-type/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Backend & Data) |
| `jeap-opensearch-index-type` — ❌ gap | | No how-to for evolving/versioning an existing index type's mapping. | ❌ |
| `jeap-opensearch-searchitem-api/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Backend & Data) |
| `jeap-opensearch-searchitem-api` — ❌ gap | | No how-to for testing a `SearchItemsProvider` implementation locally. | ❌ |
| `jeap-process-archive-reader/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Messaging) |
| `jeap-process-archive-reader/docs/reading-encrypted-artifacts.md` | Clean how-to | — | ✅ Indexed (Messaging) |
| `jeap-process-archive-reader` — ❌ gap | | No how-to for testing archive reads locally (mocked S3). | ❌ |
| `jeap-reaction-observer/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Architecture & Observability) |
| `jeap-reaction-observer` — ❌ gap | | No how-to for testing reaction-observer behaviour from a consuming service's own tests. | ❌ |
| `jeap-server-sent-events/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (REST APIs & Web) |
| `jeap-server-sent-events/docs/authorization.md` | Mixed/cookbook | 3 mutually exclusive auth-mode recipes + failure explanation — likely stays a reference cookbook rather than one how-to. | ⚪ |
| `jeap-server-sent-events/docs/client-integration.md` | Mixed | Extract: "subscribe from the browser" how-to. Leave behind: event-type reference, auth-approach explanation. | 🔶 |
| `jeap-server-sent-events` — ❌ gap | | No how-to for testing SSE push end-to-end across multiple backend instances (Kafka fan-out) locally. | ❌ |

---

## D. Spring Boot Starters & Parents (11 repos)

| Repo / page | Verdict | Action needed | Status |
|---|---|---|---|
| `jeap-spring-boot-parent/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Platform & Tooling) |
| `jeap-spring-boot-parent/docs/dependent-repo-validation.md` | Mixed | Extract: "run manually" steps. Leave behind: CI-mechanism explanation. | 🔶 |
| `jeap-spring-boot-parent` — ❌ gap | | No consumer-facing guide for upgrading to a new major/breaking parent version. | ❌ |
| `jeap-internal-spring-boot-parent/docs/pact-broker.md` | Clean how-to | — | ✅ Indexed (Platform & Tooling) |
| `jeap-internal-spring-boot-parent/docs/getting-started.md` | Mixed | Extract: the "use as parent" step. Leave behind: "what you get" list, comparison-vs-`jeap-spring-boot-parent` explanation. | 🔶 |
| `jeap-internal-spring-boot-parent/docs/dependency-management.md` | Mixed | Extract: "pin a CVE override" how-to. Leave behind: properties/BOM/plugin reference. | 🔶 |
| `jeap-internal-spring-boot-parent/docs/dependent-library-validation.md` | Mixed | Extract: "run manually" steps. Leave behind: explanation. | 🔶 |
| `jeap-internal-spring-boot-parent/docs/version-pin-check.md` | Mixed | Extract: "running manually" and "fixing a finding" / "adding a version-pin exception" as standalone how-tos. Leave behind: AHEAD/EQUAL/BEHIND reference table. | 🔶 |
| `jeap-spring-boot-starters/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Platform & Tooling) |
| `jeap-spring-boot-starters/docs/{application,logging,monitoring,security,security-client,security-starter-test,rest-request-tracing,vault,object-storage,postgresql-aws,tx,web-config,swagger,swagger-starter,featureflag}*.md` (14 per-module pages) | Mixed (all) | Each mixes explanation ("how it works"/"why") + full property-reference tables + a short usage snippet + a pitfalls list. Extract the short "add/use this starter" steps from each into a clean how-to per module; leave the rest as the module's reference/explanation page. | 🔶 ×14 |
| `jeap-spring-boot-starters` — ❌ gaps | | No how-to for rotating Prometheus/actuator Basic-Auth credentials via Vault; no generalized "override a starter's auto-configured bean/default" how-to (currently one pitfall bullet per module). | ❌ |
| `jeap-spring-boot-config-aws-starter/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Platform & Tooling) |
| `jeap-spring-boot-config-aws-starter/docs/appconfig.md` | Mixed | Extract: "enable AppConfig import" steps. Leave behind: loading-mechanism explanation, profile-layout reference. | 🔶 |
| `jeap-spring-boot-config-aws-starter/docs/secrets-management.md` | Mixed | Extract: "import secrets" steps. Leave behind: naming/prefix and client-config reference. | 🔶 |
| `jeap-spring-boot-config-aws-starter/docs/dynamic-refresh.md` | Explanation | None. | ⚪ |
| `jeap-spring-boot-config-aws-starter` — ❌ gap | | No how-to for picking up a rotated Secrets Manager secret without a restart/redeploy (reads once at startup; AppConfig's refresh is documented, Secrets Manager's isn't). | ❌ |
| `jeap-spring-boot-db-migration-starter/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Backend & Data) |
| `jeap-spring-boot-db-migration-starter/docs/migration-modes.md` | Explanation | None. | ⚪ |
| `jeap-spring-boot-db-migration-starter/docs/kubernetes-deployment.md` | Mixed | Extract: Helm-values/app-config/multi-db-wiring steps. Leave behind: "why a separate migration job" explanation. | 🔶 |
| `jeap-spring-boot-db-migration-starter` — ❌ gap | | No runbook for diagnosing/recovering a failed init-container migration job. | ❌ |
| `jeap-spring-boot-tls-starter/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Security) |
| `jeap-spring-boot-tls-starter/docs/actuator-endpoints.md` | Clean how-to | — | ✅ Indexed (Security) |
| `jeap-spring-boot-tls-starter/docs/how-it-works.md` | Explanation | None. | ⚪ |
| `jeap-spring-boot-roles-anywhere-starter/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Security) |
| `jeap-spring-boot-roles-anywhere-starter/docs/certificates-and-keys.md` | Mixed | Extract: "loading ARNs from JSON" snippet. Leave behind: formats/chain-handling/default-paths reference. | 🔶 |
| `jeap-spring-boot-roles-anywhere-starter/docs/messaging-integration.md` | Mixed, 3 purposes | Split into: a config how-to + a troubleshooting reference. Leave behind: "how it fits together" explanation. | 🔶 |
| `jeap-spring-boot-roles-anywhere-starter` — ❌ gap | | No how-to for rotating/renewing the X.509 client certificate before expiry. | ❌ |
| `jeap-spring-boot-jwe-starter/docs/testing.md` | Clean how-to | — | ✅ Indexed (Security) |
| `jeap-spring-boot-jwe-starter/docs/vault-integration.md` | Mixed | Extract: "set up Vault for JWE" (numbered prerequisites + Vault CLI commands). Leave behind: explanation/diagrams. | 🔶 |
| `jeap-spring-boot-jwe-starter/docs/{getting-started,servlet-filter,client-integration}.md` | Mixed | Each interleaves real steps with protocol/internals explanation and reference — extract the steps from each. | 🔶 |
| `jeap-spring-boot-jwe-starter/docs/{architecture,key-management,security-considerations}.md` | Explanation | None. | ⚪ |
| `jeap-spring-boot-jwe-starter/docs/{configuration,jwks-endpoint,observability}.md` | Reference | None. | ⚪ |
| `jeap-spring-boot-jwe-starter/docs/troubleshooting.md` | Reference cookbook | Symptom→cause→fix tables, not a single task — keep as a reference cookbook. | ⚪ |
| `jeap-spring-boot-jwe-starter` — ❌ gap | | No standalone, clean "rotate the Vault transit key in production" how-to — procedure is correct but embedded in `vault-integration.md`/`security-considerations.md`. | ❌ |
| `jeap-spring-modulith-error-handling-starter/docs/getting-started.md` | Mixed, 5 concerns | Split into: (1) add-the-starter how-to, (2) configure-Kafka-topics-and-EHS how-to, (3) reference tables, (4) verify-the-integration how-to. | 🔶 |
| `jeap-spring-modulith-error-handling-starter/docs/architecture.md` | Explanation | None. | ⚪ |
| `jeap-spring-modulith-error-handling-starter` — ❌ gap | | No operator-facing runbook for retrying/discarding an escalated failed publication in the EHS UI. | ❌ |
| `jeap-opensearch-client-starter/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Backend & Data) |
| `jeap-opensearch-client-starter/docs/search-item-client.md` | Reference | None. | ⚪ |
| `jeap-opensearch-client-starter/docs/authorization.md` | Mixed | Optional: extract the short usage snippets as a how-to. Leave behind: pre-check/BP-filter/post-filter explanation and reference. | 🔶 |
| `jeap-opensearch-client-starter` — gap now covered | | "How to create/register a new IndexType" — covered by `jeap-opensearch-index-type-registry-maven-plugin/docs/getting-started.md` (already indexed); just cross-link from this starter's getting-started page instead of writing new content. | 🧹 |
| `jeap-open-api-publisher-starter/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (REST APIs & Web) |
| `jeap-open-api-publisher-starter/docs/how-it-works.md` | Explanation | None. | ⚪ |
| `jeap-open-api-publisher-starter/docs/authentication.md` | Mostly reference | getting-started.md already covers the task; trim overlap rather than extract. | ⚪ |
| `jeap-open-api-publisher-starter` — ❌ gap | | No troubleshooting guide for a failed OpenAPI publish (only logs "Failed to publish OpenAPI spec", no diagnostics). | ❌ |

---

## E. Reusable Microservices (14 repos)

| Repo / page | Verdict | Action needed | Status |
|---|---|---|---|
| `jeap-error-handling/docs/{getting-started,customization,development}.md` | Clean how-to ×3 | — | ✅ Indexed (Messaging) |
| `jeap-error-handling/docs/operations.md` | Mixed | Extract: reactivating dead-letter messages. Leave behind: metrics/housekeeping/scheduled-jobs reference, multi-cluster explanation. | 🔶 |
| `jeap-error-handling` — ❌ gap | | No day-to-day "triage/resend/discard a failed message via UI or API" walkthrough (`user-interface.md` is reference only). | ❌ |
| `jeap-process-context-service/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Messaging) |
| `jeap-process-context-service/docs/maintenance-jobs.md` | Mixed, not self-contained | Write the actual command-syntax walkthrough here (it currently defers to an external jEAP CLI doc) as a standalone how-to; leave the REST/YAML contract as reference. | 🔶 |
| `jeap-process-context-service` — ❌ gaps | | No step-by-step for submitting/monitoring a maintenance job (reevaluation/backfill/republication); no guidance for resolving `UNKNOWN` tasks after a template migration. | ❌ |
| `jeap-process-archive-service/docs/{getting-started,local-development}.md` | Clean how-to ×2 | — | ✅ Indexed (Messaging) |
| `jeap-process-archive-service/docs/consuming-messages.md` | Mixed | Extract: the messages.json how-to. Leave behind: attribute reference, plugin-interfaces reference. | 🔶 |
| `jeap-process-archive-service/docs/backfill.md` | Mixed | Extract: enable/submit how-to steps. Leave behind: REST/YAML API reference, state/result tables. | 🔶 |
| `jeap-process-archive-service` — ❌ gap | | No consolidated "onboard a new message type for archiving end-to-end" walkthrough (spread across 3 pages). | ❌ |
| `jeap-message-exchange-service/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Messaging) |
| `jeap-message-exchange-service/docs/scan-status-in-database.md` | Mixed | Extract: upgrade steps. Leave behind: bug rationale, config reference. | 🔶 |
| `jeap-message-exchange-service/docs/malware-scanning.md` | Mixed | Extract: enable/disable-scanning how-to. Leave behind: state-diagram reference, AWS infra/compatibility explanation. | 🔶 |
| `jeap-message-exchange-service` — ❌ gap | | No dedicated "onboard a new business partner" walkthrough (requirements scattered across getting-started.md's tables). | ❌ |
| `jeap-message-contract-service/docs/message-contract-service.md` | Mixed, no getting-started | Extract: the setup how-to into its own `getting-started.md`. Leave behind: REST API reference, data-model reference. | 🔶 |
| `jeap-message-contract-service` — ❌ gap | | No task-focused page for "run a can-i-deploy compatibility check from a build pipeline" (raw REST reference only). | ❌ |
| `jeap-archrepo-service/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Architecture & Observability) |
| `jeap-archrepo-service/docs/importers.md` | Mixed | Expand the 4-bullet "Writing an importer" into a standalone how-to. Leave behind: ordering/registration/removal reference. | 🔶 |
| `jeap-deploymentlog-service/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Architecture & Observability) |
| `jeap-deploymentlog-service` — 🧹 housekeeping | | `README.md` has no `docs/` link table at all despite a full `docs/` folder existing — fix the README. | 🧹 |
| `jeap-deploymentlog-service` — ❌ gap | | No task-focused walkthrough for renaming/merging systems (`migrate-to`/`merge-from` documented as reference only). | ❌ |
| `jeap-doc-service/docs/getting-started.md` | Mixed | Extract: the setup steps. Leave behind: rationale for every decision (parent-vs-dependency, Node-runtime requirement). | 🔶 |
| `jeap-doc-service/docs/site-image.md` | Mixed | Extract: the Dockerfile/build-config steps. Leave behind: rationale, sizing reference. | 🔶 |
| `jeap-doc-service` — ❌ gap (significant) | | No step-by-step for a team to package and upload its own `docs/` folder to the Doc Service — `custom-documentation.md`/`uploads.md`/`upload-validation.md` explain the rules only, never walk through doing it. This is literally the task every doc-contributing team needs. | ❌ |
| `jeap-governance-service/docs/plugin-mechanism.md` | Clean how-to | — | ✅ Indexed (Architecture & Observability) |
| `jeap-governance-service/docs/rules.md` | Mixed | Extract: the 4-step "implement a custom rule" how-to. Leave behind: built-in-rule reference catalog. | 🔶 |
| `jeap-governance-service` — ❌ gap | | No walkthrough for setting up the Confluence reporting integration end-to-end. | ❌ |
| `jeap-opensearch-index-writer-service/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Backend & Data) |
| `jeap-opensearch-index-writer-service/docs/message-configuration.md` | Mixed | Extract: `ReferenceProvider`/`IndexingCondition` how-to snippets. Leave behind: messages.json field reference. | 🔶 |
| `jeap-opensearch-index-writer-service/docs/native-analysis.md` | Mixed | Split into: "add native analysis settings" how-to + "migrate on a major version bump" how-to. Leave behind: ownership/startup explanation, compatibility reference. | 🔶 |
| `jeap-oauth-mock-server/docs/{getting-started,custom-token-claims,client-integration-examples,upgrading}.md` | Clean how-to ×4 | — | ✅ Indexed (Security) — cleanest doc set in the whole audit, no gaps flagged |
| `jeap-bptest-orchestrator/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Testing) |
| `jeap-bptest-orchestrator/docs/testing-test-cases.md` | Mostly reference | Low priority; mostly API reference with one example. | ⚪ |
| `jeap-bptest-orchestrator` — ❌ gap | | No setup/troubleshooting walkthrough for the Zephyr reporting integration. | ❌ |
| `jeap-bptestagent-api/docs/{getting-started,orchestrator-callbacks}.md` | Clean how-to ×2 | — | ✅ Indexed (Testing) — no gaps flagged |
| `jeap-reaction-observer-service/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Architecture & Observability) |
| `jeap-reaction-observer-service` — 🧹 housekeeping | | `README.md` has no `docs/` link table despite a full `docs/` folder existing — fix the README. | 🧹 |
| `jeap-reaction-observer-service/docs/testing.md` | Mixed | Extract: the "replace GraphHolder in downstream tests" how-to. Leave behind: test-support/Docker-infra reference. | 🔶 |
| `jeap-reaction-observer-service` — ❌ gap | | No how-to for querying the REST API for a specific task. | ❌ |

---

## F. Tooling & Registries (13 repos)

| Repo / page | Verdict | Action needed | Status |
|---|---|---|---|
| `jeap-cli/docs/building.md` | Clean how-to | — | ✅ Indexed (Platform & Tooling) |
| `jeap-cli/docs/installation.md` | Mixed | Extract: install steps. Leave behind: launcher env-var reference, proxy/truststore explanation. | 🔶 |
| `jeap-cli/docs/upgrade-to-2.md` | Mixed | Extract: upgrade steps. Leave behind: 1.x-vs-2.x comparison table, troubleshooting reference. | 🔶 |
| `jeap-cli/docs/{migrate-java-25,migrate-spring-boot-4}.md` | Mixed, mostly reference | Single usage command + a long reference/explanation of what the automation does internally — low priority to split since the reader performs one command, not a sequence. | ⚪ |
| `jeap-cli/docs/pas-backfill.md` | Mixed | Extract: CLI usage steps. Leave behind: YAML/CSV field, validation and HTTP-response reference tables. | 🔶 |
| `jeap-cli/docs/pcs-maintenance.md` | Mixed | Extract: CLI usage steps. Leave behind: limits/response reference tables. | 🔶 |
| `jeap-cli/docs/docs-preview.md` | Mixed | Extract: preview/build steps. Leave behind: options reference, "what is rendered" reference. | 🔶 |
| `jeap-cli` — note | | No content gap; every page needs splitting, not new content — a pure cleanup target. | 🔶 |
| `jeap-renovate-presets`, `jeap-python-pipeline-lib`, `jeap-central-publishing-maven-plugin`, `jeap-license-template` | No `docs/` at all | Out of scope for extraction (nothing to extract) — flag to repo owners that no how-to/doc exists yet. | ❌ (repo-level, not page-level) |
| `jeap-truststore-maven-plugin/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Platform & Tooling) |
| `jeap-opensearch-index-type-registry-maven-plugin/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Backend & Data) |
| `jeap-opensearch-index-type-registry-maven-plugin/docs/versioning.md` | Mixed | Extract: the "major version workflow"/"minor version workflow" procedures at the end as a standalone "evolve an index type" how-to. Leave behind: compatibility/versioning reference tables. | 🔶 |
| `jeap-rewrite-recipes/docs/getting-started.md` | Mixed | Split into: "apply a recipe" how-to + "develop a recipe" how-to. Leave behind: the available-recipes catalog as reference. | 🔶 |
| `jeap-rewrite-recipes` — 🧹 housekeeping | | `README.md` has no `docs/` link table at all even though `docs/getting-started.md` and `docs/architecture.md` exist — fix the README. | 🧹 |
| `jeap-frontend-license-checker/docs/{getting-started,migration,npm-publishing-setup}.md` | Clean how-to ×3 | — | ✅ Indexed (Platform & Tooling) |
| `jeap-frontend-license-checker/docs/publishing-and-versioning.md` | Mixed | Extract: the release checklist. Leave behind: semver policy reference, release-workflow explanation. | 🔶 |
| `jeap-frontend-license-checker` — note | | No gaps; cleanest-documented repo in this set. | — |
| `jeap-message-type-registry/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Messaging) |
| `jeap-archive-type-registry/docs/getting-started.md` | Clean how-to | — | ✅ Indexed (Messaging) |
| `jeap-test-message-type-registry` — 🧹 housekeeping | | `README.md` has no `docs/` link table (minor — internal test fixture, low priority). | 🧹 |
| `jeap-devops-tools/docs/cli-oauth2-login.md` | Mixed | Extract: the OAuth2-token how-to (oidc-agent/curl). Leave behind: OIDC-discovery-override explanation, config-key reference (§8.1). | 🔶 |
| `jeap-devops-tools` — note | | No urgent gap; only one tool documented so far. | — |

---

## Next steps

1. Review this plan and the [How-Tos index](docs/how-tos/index.md) on branch `feature/JEAP-7611-how-tos`.
2. For each 🔶/❌/🧹 row above, spin up a follow-up ticket (one repo/topic at a time) — **to be created and
   approved individually**, not in bulk.
3. As pages get split, update the relevant category page under `docs/how-tos/` to link the new clean
   how-to, and update this plan's status column to ✅.
