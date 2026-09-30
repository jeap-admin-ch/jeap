# Authentication and authorization for REST APIs

Microservices frequently provide **REST APIs**. These APIs must be protected so that only authorized callers have
access. In the jEAP Blueprint Microservice, the authentication and authorization of the caller is based on **OAuth2**
(see [OIDC in the Blueprint Microservice](../oidc-in-the-blueprint-microservice.md)). A caller has to identify itself
with an **access token** issued by an authorization server. A microservice that offers a REST API (also called a
**resource**) must therefore be able to process such an access token. This processing includes in particular:

- reading the token from the request
- validating the token according to the rules of the jEAP Blueprint Microservice (see
  [Tokens in the Blueprint Microservice](../tokens/tokens-in-the-blueprint-microservice.md))
- checking the authorization of the caller for the specific REST API call

Protected APIs can no longer be called directly. To test them anyway, an API client such as
Postman can be used with an access token obtained from the authorization server.

## Integration

**Spring Security** supports OAuth2 directly. The starter
**jeap-spring-boot-security-starter** implements OAuth2-based authorization according to the rules of the jEAP
Blueprint Microservice.

```xml
<dependency>
    <groupId>ch.admin.bit.jeap</groupId>
    <artifactId>jeap-spring-boot-security-starter</artifactId>
</dependency>
```

To use the starter, an OAuth2 authorization server must be available (e.g.
[Keycloak](../authorization-servers/keycloak.md), an [OAuth2 mock server](../testing/oauth2-mock-server.md),
a B2B Gateway etc.).

The starter supports the Spring WebMvc stack.

If a microservice has to offer APIs that should not be protected with OAuth2 in addition to its OAuth2-protected
APIs, these differently protected or unprotected APIs can be exposed with an additional, specific Spring Security
filter chain (see [Spring Security configuration](spring-security-configuration.md)).

## Configuration

To protect a REST API as an OAuth2 resource with jeap-spring-boot-security-starter, the following properties must be
configured appropriately:

| Property | Optional | Value |
| --- | :---: | --- |
| `jeap.security.oauth2.resourceserver.authorization-server.issuer` | yes | OAuth2 authorization server whose tokens the resource should accept. This property configures an authorization server that issues tokens in the user and system contexts. The value is typically a URI pointing to the authorization server. |
| `jeap.security.oauth2.resourceserver.authorization-server.jwk-set-uri` | yes | URI of the JWK set endpoint of the OAuth2 authorization server. If the authorization server is a Keycloak instance, this property does not have to be defined explicitly; it is then derived automatically from the configured issuer. Configure only together with `jeap.security.oauth2.resourceserver.authorization-server.issuer`. |
| `jeap.security.oauth2.resourceserver.b2b-gateway.issuer` | yes | B2B gateway whose tokens the resource should accept. This property configures an authorization server that issues tokens in the B2B context. |
| `jeap.security.oauth2.resourceserver.b2b-gateway.jwk-set-uri` | yes | URI of the JWK set endpoint of the B2B gateway. Configure only together with `jeap.security.oauth2.resourceserver.b2b-gateway.issuer`. |
| `jeap.security.oauth2.resourceserver.resource-id` | yes | ID of the OAuth2 resource. If this property is not set, the application name (`spring.application.name`) is used as the ID. The ID of the resource is needed for the check against the `aud` claim (audience) of tokens. |
| `jeap.security.oauth2.resourceserver.system-name` | yes | Name of the business application (system) the microservice belongs to. This system name is used for the authorization against semantic roles, so that the system name does not have to be repeated in every authorization check. If this property is not set, semantic roles cannot be checked. |
| `jeap.security.oauth2.resourceserver.log.authentication-failure.enabled` | yes | If this property is defined and set to `true`, certain information about authentication failures is logged at the info level. |
| `jeap.security.oauth2.resourceserver.log.access-denied.enabled` | yes | If this property is defined and set to `true`, certain information about access-denied errors is logged at the info level. |
| `jeap.security.oauth2.resourceserver.log.access-denied.debug` | yes | If this property is defined and set to `true`, the logged-in user and their permissions are additionally logged for a logged access-denied error. This logging takes place at the debug level. Information about the logged-in user and their permissions is usually sensitive or security-critical. This logging must therefore usually remain disabled, in particular in production-like environments. |

### Configuring multiple authorization servers

The `authorization-server` and `b2b-gateway` properties described above allow a simple configuration of one Keycloak
authorization server and one B2B gateway. In addition (as of version 12.6.0 of jeap-spring-boot-security-starter), a
more general configuration option is available through the `auth-servers` properties. They configure a list of
authorization servers that the OAuth2 resource should trust. The authorization servers in this list can be configured
in addition to or as a replacement for the authorization servers under `authorization-server` and `b2b-gateway`. In
the more general configuration, each authorization server can be configured with the jEAP authentication contexts
for which it is allowed to issue tokens.

| Property | Optional | Value |
| --- | :---: | --- |
| `jeap.security.oauth2.resourceserver.auth-servers[i].issuer`<br/>(i=0: first authorization server configuration, i=1: second authorization server configuration, ...) | yes | OAuth2 authorization server whose tokens the resource should accept. The value is typically a URI pointing to the authorization server. |
| `jeap.security.oauth2.resourceserver.auth-servers[i].jwk-set-uri` | yes | URI of the JWK set endpoint of the OAuth2 authorization server. If the authorization server is a Keycloak instance, this property does not have to be defined explicitly; it is then derived automatically from the configured issuer. |
| `jeap.security.oauth2.resourceserver.auth-servers[i].authentication-contexts[j]`<br/>(j=0: first context, j=1: second context, ...) | yes | List of jEAP authentication contexts for which the OAuth2 authorization server is allowed to issue tokens. Supported values are `user`, `sys` and `b2b`. If the property is not specified, `user` and `sys` are configured implicitly. |

The `auth-servers` properties are most easily defined in a YAML configuration. The following code gives an example:

```yaml
jeap:
  security:
    oauth2:
      resourceserver:
        auth-servers:
          - issuer: "https://some-keycloak-auth-server/auth"
          - issuer: "https://another-keycloak-auth-server/auth"
            authentication-contexts: [sys]
          - issuer: "https://b2b-gateway/auth"
            jwk-set-uri: "https://b2b-gateway/auth/.well-known/jwks.json"
            authentication-contexts: [b2b]
```

> **Note:** If `jeap-spring-boot-security-starter` is added to a microservice as a dependency but no authorization
> server is configured (via `jeap.security.oauth2.resourceserver.authorization-server.issuer`,
> `jeap.security.oauth2.resourceserver.b2b-gateway.issuer` or
> `jeap.security.oauth2.resourceserver.auth-servers[0].issuer`), the starter activates a deny-all protection instead of
> the OAuth2 resource server protection, which rejects all access to REST APIs. This does not apply to REST APIs
> that are activated by other jEAP starters (e.g. the monitoring starter) or that are protected by a custom security
> configuration with a priority higher than the minimal priority.

> **Info:** It is recommended to configure the authorization server, or the "main" one if there are several, via
> `jeap.security.oauth2.resourceserver.authorization-server.*`. This
> configuration is used by other jEAP starters (e.g. the Swagger starter) to automatically apply certain preconfigurations
> for the developer's convenience. If the authorization servers of the resource are configured exclusively under
> `jeap.security.oauth2.resourceserver.auth-servers`, these preconfigurations are omitted and the developer has to
> configure the corresponding properties of the affected starters themselves (according to the documentation of the
> starters).

### Example configurations

System name in `application.yml`:

```yaml
spring:
  application:
    name: jme-security-resource-service

jeap:
  security:
    oauth2:
      resourceserver:
        system-name: "jme"
```

Authorization server and B2B gateway in `application-<env>.yml` (here for the local environment with the OAuth2 mock
server):

```yaml
jeap:
  security:
    oauth2:
      resourceserver:
        log:
          authentication-failure:
            enabled: true
          access-denied:
            enabled: true
            debug: true
        authorization-server:
          issuer: "http://localhost:8081/jme-security-auth-scs"
          jwk-set-uri: "${jeap.security.oauth2.resourceserver.authorization-server.issuer}/.well-known/jwks.json"
        b2b-gateway:
          issuer: "http://localhost:8181/jme-security-auth-scs"
          jwk-set-uri: "${jeap.security.oauth2.resourceserver.b2b-gateway.issuer}/.well-known/jwks.json"
```

The same trust configuration expressed with the more general `auth-servers` properties:

```yaml
jeap:
  security:
    oauth2:
      resourceserver:
        auth-servers:
          # OAuth2 mock server 1
          - issuer: "http://localhost:8081/jme-security-auth-scs"
          # OAuth2 mock server 2
          - issuer: "http://localhost:8089/jme-security-auth-scs"
          # B2B gateway mock
          - issuer: "http://localhost:8181/jme-security-auth-scs"
            jwk-set-uri: "http://localhost:8181/jme-security-auth-scs/.well-known/jwks.json"
            authentication-contexts: [b2b]
```

The complete configurations can be found in the
[jme-security-example](https://github.com/jme-admin-ch/jme-security-example) project.

### Customizing the AuthenticationEntryPoint and the AccessDeniedHandler

It is possible to override the AuthenticationEntryPoint and the AccessDeniedHandler of the OAuth2 resource server
configuration (as of version 12.6.0 of jeap-spring-boot-security-starter). To do so, simply define a custom bean of type
`JeapOauth2ResourceAccessDeniedHandler` or `JeapOauth2ResourceAuthenticationEntryPoint`.
As a rule, these beans should follow the default behavior otherwise configured by Spring Boot (see
`BearerTokenAuthenticationEntryPoint` and `BearerTokenAccessDeniedHandler`).

Example AuthenticationEntryPoint (WebMvc), see
[LoggingBearerTokenAuthenticationEntryPoint.java](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter/src/main/java/ch/admin/bit/jeap/security/resource/log/LoggingBearerTokenAuthenticationEntryPoint.java):

```java
package ch.admin.bit.jeap.security.resource.log;

import ch.admin.bit.jeap.security.resource.configuration.JeapOauth2ResourceAuthenticationEntryPoint;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.oauth2.server.resource.web.BearerTokenAuthenticationEntryPoint;

@Slf4j
public class LoggingBearerTokenAuthenticationEntryPoint implements JeapOauth2ResourceAuthenticationEntryPoint {

    private final BearerTokenAuthenticationEntryPoint bearerTokenAuthenticationEntryPoint = new BearerTokenAuthenticationEntryPoint();

    @Override
    public void commence(HttpServletRequest request, HttpServletResponse response, AuthenticationException authException) {
        log.info("Authentication failure on request path '{}' : '{}'.", request.getRequestURI(), authException.getMessage());
        bearerTokenAuthenticationEntryPoint.commence(request, response, authException);
    }

}
```

Example AccessDeniedHandler (WebMvc), see
[LoggingBearerTokenAccessDeniedHandler.java](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter/src/main/java/ch/admin/bit/jeap/security/resource/log/LoggingBearerTokenAccessDeniedHandler.java):

```java
package ch.admin.bit.jeap.security.resource.log;

import ch.admin.bit.jeap.security.resource.configuration.JeapOauth2ResourceAccessDeniedHandler;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.oauth2.server.resource.web.access.BearerTokenAccessDeniedHandler;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@RequiredArgsConstructor
@Slf4j
public class LoggingBearerTokenAccessDeniedHandler implements JeapOauth2ResourceAccessDeniedHandler {

    private final BearerTokenAccessDeniedHandler bearerTokenAccessDeniedHandler = new BearerTokenAccessDeniedHandler();
    private final boolean debugEnabled;

    @Override
    public void handle(HttpServletRequest request, HttpServletResponse response, AccessDeniedException accessDeniedException) {
        if (!debugEnabled) {
            log.info("Access denied to request path '{}': '{}'.", request.getRequestURI(), accessDeniedException.getMessage());
        }
        else {
            log.debug("Access denied to request path '{}': '{}'. Authentication: '{}'.",
                    request.getRequestURI(), accessDeniedException.getMessage(), AuthenticationLogInfo.from(request.getUserPrincipal()));
        }
        bearerTokenAccessDeniedHandler.handle(request, response, accessDeniedException);
    }

}
```

### Customizing the MethodSecurityExpressionHandler

`jeap-spring-boot-security-starter` configures its own instance of the `MethodSecurityExpressionHandler`. To let
applications customize it further if needed, the extension point
`JeapMethodSecurityExpressionHandlerCustomizer` is available. If an application provides a Spring bean implementing
this interface, it is used for customizing the `MethodSecurityExpressionHandler` instance. The following code (see
[MethodSecurityExpressionHandlerCustomizer.java](https://github.com/jme-admin-ch/jme-security-oauth2-example/blob/main/jme-security-oauth2-resource-authorities-service/src/main/java/ch/admin/bit/jeap/jme/security/oauth/resource/MethodSecurityExpressionHandlerCustomizer.java))
gives an example:

```java
package ch.admin.bit.jeap.jme.security.oauth.resource;

import ch.admin.bit.jeap.security.resource.configuration.JeapMethodSecurityExpressionHandlerCustomizer;
import org.springframework.security.access.expression.method.DefaultMethodSecurityExpressionHandler;
import org.springframework.security.access.expression.method.MethodSecurityExpressionHandler;
import org.springframework.stereotype.Component;

/**
 * Only needed for special cases when you have to customize the method security expression handler instantiated by
 * the jEAP security starter. Use e.g. to register a custom permission evaluator.
 */
@Component
public class MethodSecurityExpressionHandlerCustomizer implements JeapMethodSecurityExpressionHandlerCustomizer {
    @Override
    public MethodSecurityExpressionHandler customize(DefaultMethodSecurityExpressionHandler expressionHandler) {
        expressionHandler.setPermissionEvaluator(new ThingPermissionEvaluator());
        return expressionHandler;
    }
}
```

## Basic access protection

If `jeap-spring-boot-security-starter` is added to an application, all web endpoints of the application are protected
with OAuth2. If `jeap-spring-boot-monitoring-starter` is used at the same time, the monitoring endpoints are exposed
as described in [Monitoring endpoints](../../monitoring/monitoring-endpoints.md) (the Prometheus endpoint, for
example, is exposed protected by basic authentication). If `jeap-spring-boot-swagger-starter` is used as well, the
Swagger UI is exposed as described in
[API documentation with OpenAPI / Swagger](../../rest-apis/openapi-documentation.md). Further exceptions must be
defined explicitly in the application with an additional Spring Security filter chain (see
[Spring Security configuration](spring-security-configuration.md)).

## Authorization

In the Blueprint Microservice, authorization is in principle performed against roles according to the
[role concept in the Blueprint Microservice](../role-concept.md), i.e. against user roles and business partner roles,
specifically the access token claims `userroles` and `bproles`. The Blueprint Microservice supports different ways
of interpreting and checking these roles in an access token:

- as [simple roles](../role-concept.md#simple-roles)
- as [semantic roles](../role-concept.md#semantic-roles)
- as [authorities](../role-concept.md#authorities)

Each of these models supports different query options and places different
requirements on the application. The requirements, options and usage of each model are described on
the following pages:

- [Authorization with simple roles](rest-api-authorization-with-simple-roles.md)
- [Authorization with semantic roles](rest-api-authorization-with-semantic-roles.md)
- [Authorization with authorities](rest-api-authorization-with-authorities.md)

An application must choose one of these models for the authorization of its users.

### Where authorization takes place

The authorization for REST APIs is a property of REST services. For this reason, the check must be performed in the
REST layer. In a clean architecture, the security context should not be accessed outside the REST layer; the service
and domain layers should be built technology-neutral. Otherwise there may be problems, for example, with tests or with
scheduling and event processing, because no security context exists there.

With declarative authorization this is usually simple: the corresponding annotations can simply be placed in the REST
layer. With programmatic authorization it can be more difficult, because, for example, elements of the security
context have to be used to filter objects in the database. The REST layer should pass the necessary information on to
the other layers, so that they do not have to access the security context directly. The same information can then
also be supplied from other inputs.

Example of authorization in the REST layer:

```java
class RestController {
  private final ServletSemanticAuthorization jeapAuthorization;
  private final ServiceController serviceController;

  // Declarative authorization must always take place in the REST layer, i.e. in the same place as e.g. @GetMapping
  @PreAuthorize("hasRole('example', 'read')")
  @GetMapping("/api/examples/{id}")
  Example getExampleById(@PathVariable("id") String id) {
    Example example = serviceController.findById(id);
    // Programmatic authorization must always take place in the REST layer, i.e. in the same place as e.g. @GetMapping
    if (!jeapAuthorization.hasRoleForPartner("example", "read", example.getPartner())) {
      throw new NotAllowedException();
    }
    return example;
  }

  // Declarative authorization must always take place in the REST layer, i.e. in the same place as e.g. @GetMapping
  @PreAuthorize("hasRole('example', 'read')")
  @GetMapping("/api/examples")
  List<Example> getExamples() {
    // When filtering, for example, it makes no sense to perform the authorization after the filtering.
    // In that case, the information needed for the filtering should be passed to the service layer.
    // The service layer, however, should not access the security context directly.
    List<String> partners = jeapAuthorization.getPartnersForRole("example","read");
    return serviceController.findAllForPartners(partners);
  }

  ...
}

class Service {
  ...

  List<Example> findAllForPartners(List<String> partners){
    // No authorization should take place here. There may, however, be filtering based on the parameters (partners).
    ..
  }

  List<Example> findById(String id){
    // No authorization should take place here. There may, however, be filtering based on the parameters (id).
    ..
  }
}
```

Example of authorization in another layer (WRONG):

```java
class RestController {
  private final ServiceController serviceController;

  @GetMapping("/api/examples/{id}")
  Example getExampleById(@PathVariable("id") String id) {
    return serviceController.findById(id);
  }

  @GetMapping("/api/examples")
    return serviceController.findAllForPartners(partners);
  }
  ...
}

class Service {
  // Authorization beans must not be used outside the REST layer
  // DO NOT DO THIS
  private final ServletSemanticAuthorization jeapAuthorization;
  // DO NOT DO THIS
  ...

  // Declarative authorization outside the REST layer is not allowed
  // DO NOT DO THIS
  @PreAuthorize("hasRole('example', 'read')")
  // DO NOT DO THIS
  List<Example> findAllForPartners(List<String> partners){
    List<Example> examples = ...
    // Programmatic authorization outside the REST layer is not allowed
    // Filtering must be based on the inputs, not on the security context
    // DO NOT DO THIS
    return examples.stream()
        .filter(e -> jeapAuthorization.hasRoleForPartner("example", "read", e.getPartner()))
        .collect(Collectors.toList());
    // DO NOT DO THIS
  }

  // Declarative authorization outside the REST layer is not allowed
  // DO NOT DO THIS
  @PreAuthorize("hasRole('example', 'read')")
  // DO NOT DO THIS
  List<Example> findById(String id){
    // Programmatic authorization outside the REST layer is not allowed
    // DO NOT DO THIS
    if (!jeapAuthorization.hasRoleForPartner("example", "read", example.getPartner())) {
      throw new NotAllowedException();
    }
    // DO NOT DO THIS
    ...
  }
}
```

## Examples

Two example projects are available that show different use cases of the `jeap-spring-boot-security-starter` library.

- [jme-security-example](https://github.com/jme-admin-ch/jme-security-example) shows
  - the authorization with semantic roles ([jme-security-resource-service](https://github.com/jme-admin-ch/jme-security-example/tree/main/jme-security-resource-service))
  - the direct use of access tokens with claims as required by jEAP security
  - the calling of OAuth2-protected endpoints ([jme-security-client-service](https://github.com/jme-admin-ch/jme-security-example/tree/main/jme-security-client-service))
  - the configuration of an OAuth2 mock server instance ([jme-security-auth-scs](https://github.com/jme-admin-ch/jme-security-example/tree/main/jme-security-auth-scs))
  - details in the [Readme](https://github.com/jme-admin-ch/jme-security-example/blob/main/README.md)
- [jme-security-oauth2-example](https://github.com/jme-admin-ch/jme-security-oauth2-example) shows
  - the authorization with
    - simple roles ([jme-security-oauth2-resource-service](https://github.com/jme-admin-ch/jme-security-oauth2-example/tree/main/jme-security-oauth2-resource-service))
    - authorities ([jme-security-oauth2-resource-authorities-service](https://github.com/jme-admin-ch/jme-security-oauth2-example/tree/main/jme-security-oauth2-resource-authorities-service))
  - the transformation of access tokens with a claim set converter to provide the claims required by jEAP security
  - the calling of OAuth2-protected endpoints ([jme-security-oauth2-client-service](https://github.com/jme-admin-ch/jme-security-oauth2-example/tree/main/jme-security-oauth2-client-service), [jme-security-oauth2-client-authorities-service](https://github.com/jme-admin-ch/jme-security-oauth2-example/tree/main/jme-security-oauth2-client-authorities-service))
  - the configuration of an OAuth2 mock server instance ([jme-security-oauth2-auth-scs](https://github.com/jme-admin-ch/jme-security-oauth2-example/tree/main/jme-security-oauth2-auth-scs))
  - details in the [Readme](https://github.com/jme-admin-ch/jme-security-oauth2-example/blob/main/README.md)

Both examples require an authorization server with a matching configuration. Locally and in the DEV environment, an
instance of the [OAuth2 mock server](../testing/oauth2-mock-server.md) is used for this; in the REF environment, the
corresponding [Keycloak](../authorization-servers/keycloak.md) server.

## Further documentation

- [Spring Security documentation: OAuth2 resource server](https://docs.spring.io/spring-security/site/docs/current/reference/htmlsingle/#oauth2resourceserver)

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Authorization with simple roles](rest-api-authorization-with-simple-roles.md) — check roles as arbitrary strings.
- [Authorization with semantic roles](rest-api-authorization-with-semantic-roles.md) — check roles by system, tenant, resource and operation.
- [Authorization with authorities](rest-api-authorization-with-authorities.md) — derive fine-grained permissions from roles.
- [Token introspection](../tokens/token-introspection.md) — validate access tokens against the authorization server.
- [Role concept in the Blueprint Microservice](../role-concept.md) — user roles, business partner roles and role models.
- [Integrating different authorization servers](../authorization-servers/integrating-different-authorization-servers.md) — claim set converters per issuer.
- [Testing secured REST APIs](../testing/testing-secured-rest-apis.md) — test support for protected endpoints.
- [Audience validation](../audience-restriction/audience-validation.md) — how the `aud` claim is checked against the resource ID.
- [Spring Security configuration](spring-security-configuration.md) — additional Spring Security configuration for APIs that are not protected as an OAuth2 resource, e.g. public or basic auth protected APIs.
