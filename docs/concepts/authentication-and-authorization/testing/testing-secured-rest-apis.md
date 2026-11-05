# Testing secured REST APIs

[Authentication and authorization for REST APIs](../protecting-rest-apis/rest-api-authentication-and-authorization.md) describes how access
to REST APIs, and to the functions and data they provide, can be secured. Central to this is the authentication
and authorization of the user performing the access. This functionality can be activated in a Spring Boot project by
adding the `jeap-spring-boot-security-starter`.

This page shows how to verify the correct implementation of the "authorization" aspect in a project with
integration tests, and how to mock programmatic authorization checks in unit tests.

## Basics

The consumer of an API secured with the `jeap-spring-boot-security-starter` must identify itself on every request
with a **bearer access token** that was previously issued by a central authorization server. Provided the bearer
token is valid, the `jeap-spring-boot-security-starter` converts it into a Spring Security `Authentication` of type
`JeapAuthenticationToken` and stores it as the authentication in the Spring Security context. All authorization
functionality provided by the `jeap-spring-boot-security-starter` is based on the data of this authentication. To
verify the correct authorization of an access to a function or to data, a `JeapAuthenticationToken` instance must
therefore be available.

Depending on which part of an application is tested, the `JeapAuthenticationToken` has to be made available to
the tests in different ways. The following how-tos describe five different test use cases. The list is *not* meant to
imply that a functionality under test should be verified with all five variants.

## Examples of test use cases

- [How to: test a REST controller with MockMvc](../../../how-tos/security/test-a-rest-controller-with-mockmvc.md) — integration test on a REST controller, with the authentication set explicitly on the request via MockMvc.
- [How to: test a component with a given authentication](../../../how-tos/security/test-a-component-with-a-given-authentication.md) — integration test "in isolation" on a component, without going through the HTTP request processing chain.
- [How to: test programmatic authorization checks in a unit test](../../../how-tos/security/test-programmatic-authorization-checks-in-a-unit-test.md) — unit test of a method performing a programmatic authorization check, outside a Spring application context.
- [How to: disable security in a Spring Boot test](../../../how-tos/security/disable-security-in-a-spring-boot-test.md) — leave security aspects out of a Spring Boot test that is only about functionality.
- [How to: test a REST endpoint with full OAuth2 security](../../../how-tos/security/test-a-rest-endpoint-with-full-oauth2-security.md) — pass a real access token through the whole OAuth2 resource security chain.

## Test support

The module `jeap-spring-boot-security-starter-test` provides classes that simplify testing the authorization of
resources protected with the `jeap-spring-boot-security-starter`. These classes are also used by the examples
described above.

### Integration

The test support classes can be used in your own tests via the following Maven dependency:

```xml
<dependency>
    <groupId>ch.admin.bit.jeap</groupId>
    <artifactId>jeap-spring-boot-security-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

The following functionality is then available to the tests:

### JeapAuthenticationTestTokenBuilder

The class
[JeapAuthenticationTestTokenBuilder](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/resource/JeapAuthenticationTestTokenBuilder.java)
implements a builder for easily creating `JeapAuthenticationToken` instances. Such tokens are the basis of
both the declarative and the programmatic authorization queries of the resources protected by the
`jeap-spring-boot-security-starter`.

With the `JeapAuthenticationTestTokenBuilder`, both the roles and the user/system information of the
`JeapAuthenticationToken` to be created can be defined.

The `JeapAuthenticationToken` instances created with the `JeapAuthenticationTestTokenBuilder` can, for example, be set
on MockMvc/WebTestClient requests in tests, or directly in the Spring Security context with which a test is executed.

### AuthorizationMock classes

For the concrete authorization of a user based on their `JeapAuthenticationToken`, the
`jeap-spring-boot-security-starter` provides the `jeapAuthorization` bean, which is of type
`ServletSimpleAuthorization` (simple roles) or `ServletSemanticAuthorization` (semantic roles).

The test support classes
[ServletSimpleAuthorizationMock](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/resource/ServletSimpleAuthorizationMock.java)
and
[ServletSemanticAuthorizationMock](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/resource/ServletSemanticAuthorizationMock.java)
implement mock variants that answer all authorization queries based on a `JeapAuthenticationToken` stored in the
mock. The stored token can simply be created with the `JeapAuthenticationTestTokenBuilder` (see above), for example.

The main purpose of the `AuthorizationMock` classes is the simple mocking of programmatic authorization queries in
unit tests. Alternatively, plain Mockito mocks can be used for this as well.

### PermitAllWebSecurityConfiguration

In a Spring Boot test (for WebMvc), the module `jeap-spring-boot-security-starter-test` automatically activates a web
security configuration that permits all requests, and does so with high priority. This overrides the web security
configuration automatically activated by the `jeap-spring-boot-security-starter` and effectively disables it. This is
useful whenever tests set the required authentication themselves, in particular in integration tests of REST
controllers with MockMvc.

If required, the `jeap-spring-boot-security-starter-test` can be prevented from activating the
`PermitAllWebSecurityConfiguration` automatically. To do so, the configuration
[DisableJeapPermitAllSecurityConfiguration](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/resource/configuration/DisableJeapPermitAllSecurityConfiguration.java)
provided by the `jeap-spring-boot-security-starter-test` can be imported in the test.

### JwsBuilder

The class
[JwsBuilder](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/jws/JwsBuilder.java)
implements a builder for easily creating JWS tokens, i.e. *signed* JWT tokens. Users, applications and
microservices usually have to authenticate themselves to a called microservice with such tokens.

With the `JwsBuilder`, both the roles and the user/system information of the JWS token to be created can be defined.
The RSA key to be used for signing the token can be defined as well.

The tokens created with the `JwsBuilder` can be set as bearer authorization token in the header of the HTTP request
when testing OAuth2-protected REST endpoints, in order to authenticate to the protected endpoint.

### MockJeapOAuth2RestClientBuilderFactory

The class
[MockJeapOAuth2RestClientBuilderFactory](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/client/MockJeapOAuth2RestClientBuilderFactory.java)
is a mock implementation of the `JeapOAuth2RestClientBuilderFactory`. The mock factory produces `RestClient.Builder`
instances whose `RestClient` instances do not obtain their access tokens from an OAuth2 authorization server such as
Keycloak or the mock server, but from an `AuthTokenProvider` instance defined by the mock factory. The access token
required for the execution of a specific test can be loaded dynamically into the `AuthTokenProvider`. The tokens can
be created with the `JwsBuilder`, for example.

### ServletJwksEndpointMock

An OAuth2 resource protected with the `jeap-spring-boot-security-starter` must verify the signature of the access
tokens sent to it. To do so, the resource obtains the public keys matching the private keys with which the
authorization server signs its tokens from a dedicated web endpoint of the authorization server. To avoid
depending on an external authorization server in integration tests of an OAuth2-protected web endpoint, the class
[ServletJwksEndpointMock](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/resource/jwks/ServletJwksEndpointMock.java)
implements such an endpoint locally as a REST controller serving public keys, under the same path as the mock server,
`/.well-known/jwks.json`.

For an OAuth2 resource protected with the `jeap-spring-boot-security-starter` to use the mock JWKS endpoint
in a test, the OAuth2 resource configuration property
`jeap.security.oauth2.resourceserver.authorization-server.jwk-set-uri` must also point to the mock JWKS
endpoint.

### RSAKeyUtils

[RSAKeyUtils](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/jws/RSAKeyUtils.java)
is a simple helper class providing methods to load an RSA key from a keystore and to generate an RSA key. The keys
loaded/generated this way can be used in the `JwsBuilder` or the `ServletJwksEndpointMock`, for example.

### TestKeyProvider and JwsBuilderFactory

The class
[TestKeyProvider](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/jws/TestKeyProvider.java)
implements a Spring bean that loads a predefined RSA key from a predefined keystore and provides it for test purposes.
The
[JwsBuilderFactory](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/jws/JwsBuilderFactory.java)
implements a factory that creates `JwsBuilder` instances which obtain the key used for signing their tokens from a
`TestKeyProvider` instance. When these classes are used in Spring Boot tests, the RSA key predefined in
`jeap-spring-boot-security-starter-test` is used automatically. If required, your own key/keystore can be used through a
custom configuration of the
[TestKeyProviderConfigurationProperties](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/jws/TestKeyProviderConfigurationProperties.java).

### JeapOAuth2IntegrationTestConfiguration

The configuration
[JeapOAuth2IntegrationTestConfiguration](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/configuration/JeapOAuth2IntegrationTestConfiguration.java)
can be imported into a Spring Boot test to extend the loaded Spring context for integration tests on
OAuth2-protected resources in which a call to the protected resource passes through the whole security stack.

The `JeapOAuth2IntegrationTestConfiguration` provides a `TestKeyProvider`, a `JwsBuilderFactory`, a `JwksEndpoint`, a
`MockJeapOAuth2RestClientBuilderFactory` and a `MockJeapOAuth2WebclientBuilderFactory`, all of which rely on the RSA
key shipped with `jeap-spring-boot-security-starter-test`. This ensures that the OAuth2 resource under test in an
integration test accepts the tokens created with the `JwsBuilderFactory`.

In addition to importing the `JeapOAuth2IntegrationTestConfiguration`, the JWK set URI must always be configured to
point to the JWKS mock endpoint in an integration test (see section [ServletJwksEndpointMock](#servletjwksendpointmock)).

## Further documentation

- [Spring MockMvc](https://docs.spring.io/spring-framework/docs/current/spring-framework-reference/testing.html#spring-mvc-test-framework)
- [REST Assured](http://rest-assured.io/)

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Authentication and authorization for REST APIs](../protecting-rest-apis/rest-api-authentication-and-authorization.md) — how REST APIs are secured with the jEAP Security Starter.
- [Tokens in the Blueprint Microservice](../tokens/tokens-in-the-blueprint-microservice.md) — structure and claims of the access tokens the tests create.
- [OpenID Connect / OAuth2 mock server](oauth2-mock-server.md) — a local authorization server for tests beyond the JWKS mock endpoint.
