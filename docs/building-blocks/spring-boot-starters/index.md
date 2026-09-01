# Spring Boot Starters

The jEAP Maven **parents** and the auto-configuring **Spring Boot starters** that provide
application setup and cross-functional defaults. For how the parents fit together and the
dependency-management model, see [Using jEAP](../../using-jeap.md).

## Maven parents

| Parent | Purpose | Source |
|---|---|---|
| [jeap-spring-boot-parent](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-parent/) | The Maven parent applications based on jEAP should inherit from. Manages the versions of the jEAP dependencies (starters, messaging, crypto, …). | [GitHub](https://github.com/jeap-admin-ch/jeap-spring-boot-parent) |
| [jeap-internal-spring-boot-parent](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-internal-spring-boot-parent/) | Manages the Spring Boot version, inherits Spring Boot's dependency management, and pre-configures common Maven plugins. Used mostly jEAP-internally. | [GitHub](https://github.com/jeap-admin-ch/jeap-internal-spring-boot-parent) |

## Starter collection

**[jeap-spring-boot-starters](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/)**
bundles the commonly used starters. See its
[README](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/README.md)
for the authoritative list; it currently includes:

| Starter | Purpose |
|---|---|
| [jeap-spring-boot-application-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-application-starter) | Frontend route handling and DB pooling defaults; includes the [logging starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-logging-starter). |
| [jeap-spring-boot-logging-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-logging-starter) | Structured JSON logging including tracing information. |
| [jeap-spring-boot-monitoring-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-monitoring-starter) | Monitoring with Prometheus / Micrometer. |
| [jeap-spring-boot-rest-request-tracing](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-rest-request-tracing) | Technology-neutral servlet request/response tracing with header masking — the core consumed by the logging starter's REST request logging. |
| [jeap-spring-boot-security-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-starter) | Secure HTTP/REST APIs using OAuth2 (the resource-server side). |
| [jeap-spring-boot-security-client-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-client-starter) | Configures the service as an OAuth2 *client* for service-to-service calls, with preconfigured `RestClient.Builder` instances that attach access tokens. |
| [jeap-spring-boot-security-starter-test](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-starter-test) | Test support for services secured with the security starter: authenticated MockMvc requests, `JeapAuthenticationToken` fixtures, signed test JWTs and a mock JWKS endpoint. |
| [jeap-spring-boot-swagger](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-swagger) | The core jEAP OpenAPI auto-configuration on top of springdoc-openapi, without the Swagger UI. |
| [jeap-spring-boot-swagger-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-swagger-starter) | OpenAPI specs for Spring controllers plus Swagger UI (bundles `jeap-spring-boot-swagger`). |
| [jeap-spring-boot-postgresql-aws-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-postgresql-aws-starter) | PostgreSQL configuration for AWS RDS, supporting different cluster types. |
| [jeap-spring-boot-tx](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-tx) | Read-replica-aware transaction routing: `@TransactionalReadReplica` sends read-only transactions to an RDS read replica, relieving the writer. |
| [jeap-spring-boot-object-storage-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-object-storage-starter) | S3 client configuration. |
| [jeap-spring-boot-vault-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-vault-starter) | Secrets management with Vault. |
| [jeap-spring-boot-featureflag-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-featureflag-starter) | Feature flags based on configuration properties and Togglz. |
| [jeap-spring-boot-web-config-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-web-config-starter) | HTTP caching and frontend security headers. |

## Standalone starters

| Starter | Purpose | Source |
|---|---|---|
| [jeap-spring-boot-config-aws-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-config-aws-starter/) | Integrates with AWS AppConfig and AWS Secrets Manager. | [GitHub](https://github.com/jeap-admin-ch/jeap-spring-boot-config-aws-starter) |
| [jeap-spring-boot-db-migration-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-db-migration-starter/) | Run DB migrations as separate jobs (e.g. on Kubernetes). | [GitHub](https://github.com/jeap-admin-ch/jeap-spring-boot-db-migration-starter) |
| [jeap-spring-boot-tls-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-tls-starter/) | Enables TLS on the Spring Boot web server, optionally generating a certificate at startup (suitable for AWS ALB ↔ application). | [GitHub](https://github.com/jeap-admin-ch/jeap-spring-boot-tls-starter) |
| [jeap-spring-boot-roles-anywhere-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-roles-anywhere-starter/) | Integration with AWS IAM Roles Anywhere — secure, certificate-based credentials without external helper tools. | [GitHub](https://github.com/jeap-admin-ch/jeap-spring-boot-roles-anywhere-starter) |
| [jeap-spring-boot-jwe-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-jwe-starter/) | Transparent JSON Web Encryption (JWE) for HTTP APIs. The Angular counterpart is [jeap-jwe-client](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-jwe-client/). | [GitHub](https://github.com/jeap-admin-ch/jeap-spring-boot-jwe-starter) |
| [jeap-spring-modulith-error-handling-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-modulith-error-handling-starter/) | Retries failed Spring Modulith event publications and escalates exhausted failures to the jEAP Error Handling Service. | [GitHub](https://github.com/jeap-admin-ch/jeap-spring-modulith-error-handling-starter) |
| [jeap-open-api-publisher-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-open-api-publisher-starter/) | Publishes the service's OpenAPI specification to the Architecture Repository on application startup — a drop-in dependency that uploads the `springdoc-openapi` document asynchronously, without code changes. | [GitHub](https://github.com/jeap-admin-ch/jeap-open-api-publisher-starter) |
| [jeap-opensearch-client-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-opensearch-client-starter/) | Type-safe, authorization-aware read access to OpenSearch indices. Auto-configures an `OpenSearchClient` and `SearchItemClient` for indices defined by [`IndexType`](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-opensearch-index-type/) descriptors, over Apache HTTP or AWS-signed transports with role-based access control. | [GitHub](https://github.com/jeap-admin-ch/jeap-opensearch-client-starter) |

## Related

- [Using jEAP](../../using-jeap.md) — parent hierarchy and dependency management.
- [App Building Blocks](../index.md) — overview of all categories.
