# Spring Security configuration

The jEAP Security Starter (`jeap-spring-boot-security-starter`) uses Spring Security for the
[authentication and authorization of REST APIs](rest-api-authentication-and-authorization.md). By default, the
starter protects all URIs of a microservice as an OAuth2 resource, including CORS and CSRF protection. An application
can override these settings with an additional Spring Security configuration, e.g. to provide a public API, an API
with a different protection such as basic auth, or a self-contained system (SCS) with a public UI. This documentation
gives guidance for how to configure such APIs securely together with the jEAP Security Starter.
Working example configurations are provided by the JME example projects listed under [Examples](#examples).

## Basics

Spring Security is configured with `SecurityFilterChain` beans. Each of these configurations
defines with a `RequestMatcher` which requests it is responsible for, and with an `@Order` annotation the order in
which the configurations are applied.

The order of each configuration must be unique: no two `SecurityFilterChain` beans may have the same order. The
highest priority is the order `Ordered.HIGHEST_PRECEDENCE` (-2147483648), the lowest priority is the order
`Ordered.LOWEST_PRECEDENCE` (+2147483647). The easiest way to define an order is relative to one of these constants,
e.g. `Ordered.HIGHEST_PRECEDENCE + 10` for the tenth-highest priority (the plus sign may look confusing, but
`HIGHEST_PRECEDENCE` is the smallest possible value).

On startup, Spring Security collects all configurations and sorts them by their order, from the highest to the lowest
priority. For every request, Spring Security goes through this chain and looks for the first configuration whose
`RequestMatcher` matches the request. This configuration is applied to the request, the rest of the chain is
ignored. This way, a configuration with a higher priority overrides the configurations with a lower priority for
specific requests. Only one configuration is ever applied to a request.

The jEAP Security Starter defines its security filter chain as `Ordered.LOWEST_PRECEDENCE`. Using the lowest priority
reflects the idea of a general OAuth2 protection as a baseline, which applications can opt out of for their specific
needs with configurations of a higher priority.

In addition, the jEAP Monitoring Starter (`jeap-spring-boot-monitoring-starter`) defines a security configuration that
makes some actuator endpoints available (Prometheus, info, health). It does so with a very high priority
(`Ordered.HIGHEST_PRECEDENCE + 9`) to reduce the risk of the default configuration of these endpoints being overridden
unintentionally, as they are required for monitoring and health checks in operation.

## Guidance

- Start a configuration by defining the requests it applies to with a `RequestMatcher`. Keep this scope as narrow as
  possible. No other configuration is applied to the requests it matches.
- Use several configurations for requests that need a different protection. If an application needs to protect
  one API with basic auth and make another API publicly accessible, define two independent configurations.
- Always define an explicit order on a configuration, e.g. with the `@Order` annotation.
- Authorize requests against a dedicated role, i.e. with `hasRole()` and not just with e.g. `fullyAuthenticated()`.
  This prevents the requests from being accessible with a different login by accident.
- Do not use session management.

## Examples

Working example configurations are provided by the following JME example projects:

- [jme-security-example](https://github.com/jme-admin-ch/jme-security-example) shows how to protect REST APIs with
  the jEAP Security Starter and how to provide additional Spring Security configurations for APIs that are not
  protected as an OAuth2 resource.
- [jme-swagger-example](https://github.com/jme-admin-ch/jme-swagger-example) shows how to provide the OpenAPI
  documentation and the Swagger UI of a microservice with the jEAP Swagger Starter.

## Related

- [Authentication and authorization for REST APIs](rest-api-authentication-and-authorization.md) — integration and
  configuration of the jEAP Security Starter, which provides the baseline OAuth2 protection.
- [API Documentation with OpenAPI / Swagger](../../rest-apis/openapi-documentation.md) — the jEAP Swagger Starter and
  its configuration.
- [Monitoring endpoints](../../monitoring/monitoring-endpoints.md) — the actuator endpoints and their security
  configuration.
