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
the tests in different ways. The following sections describe five different test use cases. The list is *not* meant to
imply that a functionality under test should be verified with all five variants.

## Examples of test use cases

### Integration test on a REST controller

For efficient integration tests on REST controllers, Spring Test provides **MockMvc** for
WebMvc applications. It runs integration tests on controllers without starting a whole application
server each time. With MockMvc, the Spring Security `Authentication` with which a
test request is executed can be set explicitly on the request.

jEAP provides an example of testing an OAuth2 resource using [MockMvc](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-resource-service/src/test/java/ch/admin/bit/jeap/jme/security/oauth/resource/PartnerResourceMockMvcIT.java) directly. For those who prefer REST Assured, there is also
an example of how the tests can be written [in REST Assured syntax on top of MockMvc](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-resource-service/src/test/java/ch/admin/bit/jeap/jme/security/oauth/resource/PartnerResourceRestAssuredIT.java).

> **Note:** In the Spring Boot application started for the test, the auto-configuration of the
> `jeap-spring-boot-security-starter` for OAuth2 resources must be active so that security is configured
> appropriately. This means that the following property must be set:
> `jeap.security.oauth2.resourceserver.authorization-server.issuer`

> **Note:** The example above assumes that it is run with the test dependency `jeap-spring-boot-security-starter-test`
> (see below). This dependency automatically configures a web security configuration with the highest priority that
> simply lets all requests through. Since the tests add the `JeapAuthenticationToken` instances with which requests
> are executed directly via MockMvc, no further authentication filters should be traversed in the web filter
> chain.

### Integration test on a component

To verify the authorization "in isolation" on a component, without
executing the HTTP request processing chain, MockMvc (see previous section) cannot be used. The
`JeapAuthenticationToken` for the test call must therefore be provided to the Spring Security context
by other means.

For this purpose, the module `jeap-spring-boot-security-starter-test` provides a JUnit 5 extension with
which a test method can be executed with a given `JeapAuthenticationToken`. This test functionality is activated
through the annotation
[@WithAuthentication](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/resource/extension/WithAuthentication.java).
The annotation references the name of the method of the test class that provides the `JeapAuthenticationToken` for
the test.

This [example](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-resource-service/src/test/java/ch/admin/bit/jeap/jme/security/oauth/resource/PartnerResourceIT.java) shows how to use this annotation in integration tests for components/services.

The example does not start a complete Spring Boot application but a Spring application context containing only the
elements required by the test. The Spring Boot autoconfiguration of the `jeap-spring-boot-security-starter` is not
executed, i.e. the property `jeap.security.oauth2.resourceserver.authorization-server.issuer` mentioned above is
irrelevant for these tests.

### Unit test

Unit tests are meant to test classes in isolation. Consequently, these tests also take place outside a Spring
application context. Therefore, neither the autoconfiguration of the `jeap-spring-boot-security-starter` nor
any declarative authorization checks have any influence on the test. However, if a method under test performs
programmatic authorization checks, a `JeapAuthenticationToken` must be provided for it.

This [example](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-resource-service/src/test/java/ch/admin/bit/jeap/jme/security/oauth/resource/PartnerResourceTest.java) shows how the `JeapAuthenticationToken` can be mocked for the test of a method with a
programmatic authorization check. The example uses test support classes from `jeap-spring-boot-security-starter-test`
(see below).

### Spring Boot tests without security

If the goal is only to test functionality, a cross-cutting concern such as security can unnecessarily
complicate the tests and distract from what a specific test is actually about. It can
therefore be legitimate to leave security aspects out of such tests. When using the
`jeap-spring-boot-security-starter`, a few things have to be taken into account for this.

If a Spring Boot test is executed, i.e. in particular a test with autoconfiguration enabled, and the
`jeap-spring-boot-security-starter` is part of the project, a web security configuration protecting the REST
endpoints from unauthorized access is activated automatically. To lift this protection for a test that should run
without security aspects, the following has to be done:

- The configuration `DisableJeapSecurityStarterAutoConfiguration` from `jeap-spring-boot-security-starter-test` must be
  imported in the test.
- The `jeapAuthorization` bean must be defined in the test and mocked appropriately for the tests if the application
  accesses this bean programmatically, e.g. to perform authorization checks or to obtain details about the user.

The second point does not apply if `jeapAuthorization` is only used in security annotations such as `@PreAuthorize`.

This [test class](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-resource-service/src/test/java/ch/admin/bit/jeap/jme/security/oauth/resource/PartnerResourceBootServerNoSecurityIT.java) gives examples of Spring Boot tests without security with a mocked `jeapAuthorization` bean.

### Spring Boot tests with full security

If a test of a REST request should also pass through the OAuth2 resource part of the security chain, a valid OAuth2
access token must be created for the request, and a JWKS endpoint must be available to verify the signature of the
access token. The configuration class
[JeapOAuth2IntegrationTestConfiguration](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/configuration/JeapOAuth2IntegrationTestConfiguration.java)
from the module `jeap-spring-boot-security-starter-test` makes both easy.

Specifically, the following has to be done in a test:

- The configuration `JeapOAuth2IntegrationTestConfiguration` must be imported in the test.
- The following two OAuth2 resource properties must be overridden appropriately:
  - `jeap.security.oauth2.resourceserver.authorization-server.jwk-set-uri`
  - `jeap.security.oauth2.resourceserver.authorization-server.issuer`
- An OAuth2 access token suitable for the specific test case must be created with the help of the `JwsBuilderFactory`.
- The access token must be passed as bearer authorization token in the header of the HTTP request to the protected
  resource.

This [test class](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-resource-service/src/test/java/ch/admin/bit/jeap/jme/security/oauth/resource/PartnerResourceBootServerWithSecurityIT.java) gives examples of Spring Boot tests with full security. The example uses
[REST Assured](http://rest-assured.io/) to implement the tests on the REST endpoints.
Setting the OAuth2 access token in the request is very simple: `given().auth().oauth2("the-token")...`

Details on how the test support provided by the `JeapOAuth2IntegrationTestConfiguration` works can be found in the
following sections.

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
