# Calling secured REST APIs from Java

Microservices frequently call **REST APIs** of other microservices that are protected against unauthorized access. To do so, the caller must authenticate itself to the provider of the API, which then authorizes the caller accordingly. In the jEAP Blueprint Microservice, authentication and authorization of the caller of a REST API are based on **OAuth2** (see [OIDC in the Blueprint Microservice](oidc-in-the-blueprint-microservice.md)). A caller (also called **client**) must identify itself with an **access token** issued by a central authorization server. Two cases need to be distinguished:

- The microservice calls the other service with its own access token (system context).
- The microservice uses a token that it has itself received from a caller (token propagation).

## Integration

**Spring Security** supports OAuth2 directly. The starter **jeap-spring-boot-security-client-starter** implements the OAuth2-based authentication of a client towards a resource as prescribed by the jEAP Blueprint Microservice.

> **Note:** The `jeap-spring-boot-security-client-starter` comes automatically as a dependency of the `jeap-spring-boot-security-starter` and up to version 17.43.0 was even an integral part of it. As of version 18.0.0, the client-related functionality of the jEAP Security Starter is also available as the separate dependency `jeap-spring-boot-security-client-starter`.

Adding the `jeap-spring-boot-security-client-starter` as a dependency:

```xml
<dependency>
    <groupId>ch.admin.bit.jeap</groupId>
    <artifactId>jeap-spring-boot-security-client-starter</artifactId>
</dependency>
```

To use the starter, an OAuth2 authorization server must be available (e.g. [Keycloak](authorization-servers/keycloak.md) or the [OAuth2 mock server](testing/oauth2-mock-server.md)).

## Configuration

To access a REST API in the system context, the following properties must be configured:

| Property | Value |
| --- | --- |
| `spring.security.oauth2.client.registration.our-client-name.client-id` | ID of an OAuth2 client configured in an authorization server |
| `spring.security.oauth2.client.registration.our-client-name.client-secret` | Secret (password) of the OAuth2 client |
| `spring.security.oauth2.client.registration.our-client-name.authorization-grant-type` | `client_credentials` |
| `spring.security.oauth2.client.registration.our-client-name.provider` | `auth-server-name` (refers to the configuration of an OAuth2 provider named "auth-server-name" under `spring.security.oauth2.client.provider.auth-server-name.*`) |
| `spring.security.oauth2.client.provider.auth-server-name.issuer-uri` | URI of the authorization server |

The jEAP Security Starter only provides its client functionality if such a client configuration is present.

### Configuring different authorization servers

If a microservice has to call REST APIs whose access management is handled by different authorization servers, each of these authorization servers must be configured under `spring.security.oauth2.client.provider.{auth-server}.*`. The configuration of an OAuth2 client for a specific provider under `spring.security.oauth2.client.registration.{client-name}.*` must then reference the corresponding provider name with `spring.security.oauth2.client.registration.{client-name}.provider={auth-server}`.

See [Spring Boot Property Mappings](https://docs.spring.io/spring-security/reference/servlet/oauth2/login/core.html#oauth2login-boot-property-mappings) in the Spring Security documentation for details on configuring OAuth2 clients in the Spring Security client registry through Spring Boot properties.

## Accessing protected resources

A protected resource is accessed with the Spring **RestClient**. The Spring **RestTemplate** is not supported.

## Creating a client instance

The Spring RestClient provides a convenient builder for creating its instances. With the **JeapOAuth2RestClientBuilderFactory**, the jEAP Security Starter provides a factory that creates specially pre-configured client builder instances. The builder can then be configured further as needed, e.g. by setting a base URL, before the desired client instance is created.

**See [How to: call a secured REST API from Java](../../how-tos/security/call-a-secured-rest-api-from-java.md)**
for a worked example of creating and using a client instance, in both the system context and for token propagation.

Currently, three factory methods for RestClient builder instances are available:

| Method | Behavior of the created client instances | Token context |
| --- | --- | --- |
| `createForClientRegistryId(String clientRegistryId)` | All outgoing requests carry an OAuth2 access token that is obtained from the authorization server using the client configuration referenced by `clientRegistryId`. | "System" |
| `createForTokenFromIncomingRequest()` | All outgoing requests carry the OAuth2 access token from the current incoming request if such a token is present; otherwise, no token is added to the outgoing requests. | Token propagation if possible, otherwise no token |
| `createForClientRegistryIdPreferringTokenFromIncomingRequest(String clientRegistryId)` | A mix of `createForClientRegistryId()` and `createForTokenFromIncomingRequest()`: if the current incoming request contains an access token, this token is used; otherwise, a token is obtained from the authorization server using the client configuration referenced by `clientRegistryId`. | Token propagation if possible, otherwise "System" |

## Examples

**See [How to: call a secured REST API from Java](../../how-tos/security/call-a-secured-rest-api-from-java.md)**
for worked examples of calling a secured REST API from Java, both with the microservice's own access token
(system context) and with a token propagated from an incoming request.

## Further documentation

- [Spring RestClient documentation](https://docs.spring.io/spring-framework/reference/integration/rest-clients.html#rest-restclient)
- [Spring Security OAuth2 Client WebMvc documentation](https://docs.spring.io/spring-security/site/docs/current/reference/htmlsingle/#oauth2client)

## Related

- [Authentication and authorization](index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Authentication and authorization for REST APIs](protecting-rest-apis/rest-api-authentication-and-authorization.md) — protect the REST APIs that are called here.
- [OIDC in the Blueprint Microservice](oidc-in-the-blueprint-microservice.md) — the OAuth2/OIDC flows used in the Blueprint Microservice.
- [Integrating different authorization servers](authorization-servers/integrating-different-authorization-servers.md) — accept tokens from several authorization servers on the resource side.
- [Cross-platform authentication](authorization-servers/cross-platform-authentication.md) — token propagation across platforms.
- [OpenID Connect / OAuth2 mock server](testing/oauth2-mock-server.md) — local authorization server for development.
- [Keycloak](authorization-servers/keycloak.md) — the authorization server used in the target environments.
- [How to: call a secured REST API from Java](../../how-tos/security/call-a-secured-rest-api-from-java.md) — create and use a client instance, for the system context and for token propagation.
