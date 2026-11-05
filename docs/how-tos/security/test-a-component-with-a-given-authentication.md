# How to: test a component with a given authentication

To verify the authorization "in isolation" on a component, without executing the HTTP request processing
chain, MockMvc (see [How to: test a REST controller with MockMvc](test-a-rest-controller-with-mockmvc.md))
cannot be used. The `JeapAuthenticationToken` for the test call must therefore be provided to the Spring
Security context by other means.

## Steps

1. Add the test dependency `jeap-spring-boot-security-starter-test` to the project (see
   [Integration](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md#integration)).
   This module provides a JUnit 5 extension with which a test method can be executed with a given
   `JeapAuthenticationToken`.
2. Define a method on the test class that provides the `JeapAuthenticationToken` to use for the test, for
   example built with the
   [JeapAuthenticationTestTokenBuilder](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md#jeapauthenticationtesttokenbuilder).
3. Activate this test functionality on the test method through the annotation
   [@WithAuthentication](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/resource/extension/WithAuthentication.java),
   referencing the name of the method from step 2.

This [example](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-resource-service/src/test/java/ch/admin/bit/jeap/jme/security/oauth/resource/PartnerResourceIT.java) shows how to use this annotation in integration tests for components/services.

The example does not start a complete Spring Boot application but a Spring application context containing only the
elements required by the test. The Spring Boot autoconfiguration of the `jeap-spring-boot-security-starter` is not
executed, i.e. the property `jeap.security.oauth2.resourceserver.authorization-server.issuer` mentioned in
[How to: test a REST controller with MockMvc](test-a-rest-controller-with-mockmvc.md) is irrelevant for these tests.

## Related

- [Testing secured REST APIs](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md) — the test-support classes used above, and the other test use cases.
- [How to: test a REST controller with MockMvc](test-a-rest-controller-with-mockmvc.md) — the alternative for testing through the HTTP request processing chain.
- [How to: test programmatic authorization checks in a unit test](test-programmatic-authorization-checks-in-a-unit-test.md) — the equivalent for tests that run outside a Spring application context.
