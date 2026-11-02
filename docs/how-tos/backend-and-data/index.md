# How-Tos: Backend & Data

Databases, schema migrations, and OpenSearch.

- [Configure the default Postgres schema with Spring and Flyway](../../concepts/database/postgresql-with-spring-and-flyway.md) — set up the "data" schema for Postgres 15, Spring, Flyway and H2 consistently.
- [Run database migrations as a separate deployment step](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-db-migration-starter/getting-started) — add the starter, add migration scripts, configure the migration mode, local dev fallback.
- [Publish a database schema to the Architecture Repository](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-db-schema-publisher/getting-started) automatically on startup.
- Use OpenSearch in a jEAP service:
  - [Add the OpenSearch client starter and search](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-opensearch-client-starter/getting-started).
  - [Implement and register a custom IndexType](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-opensearch-index-type/getting-started).
  - [Expose a SearchItemsProvider endpoint](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-opensearch-searchitem-api/getting-started) for the jEAP OpenSearch Index Writer to call.
  - [Set up an OpenSearch Index Type Registry project](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-opensearch-index-type-registry-maven-plugin/getting-started) end to end.
  - [Build and run an OpenSearch Index Writer Service instance](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-opensearch-index-writer-service/getting-started).

## Known gaps — no how-to exists yet

See [`doc-refactoring-plan.md`](https://github.com/jeap-admin-ch/jeap/blob/main/doc-refactoring-plan.md)
for the full list and status. Notably missing: a walkthrough for an index-type major-version migration
with backfill (only a short list buried inside a reference-heavy page today).
