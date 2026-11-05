# How to: test programmatic authorization checks in a unit test

Unit tests are meant to test classes in isolation. Consequently, these tests also take place outside a Spring
application context. Therefore, neither the autoconfiguration of the `jeap-spring-boot-security-starter` nor
any declarative authorization checks have any influence on the test. However, if a method under test performs
programmatic authorization checks, a `JeapAuthenticationToken` must be provided for it.

## Steps

1. Add the test dependency `jeap-spring-boot-security-starter-test` to the project (see
   [Integration](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md#integration)).
2. Mock the `JeapAuthenticationToken` for the programmatic authorization check under test, for example with the
   [AuthorizationMock classes](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md#authorizationmock-classes)
   — `ServletSimpleAuthorizationMock` or `ServletSemanticAuthorizationMock` — storing a token created with the
   [JeapAuthenticationTestTokenBuilder](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md#jeapauthenticationtesttokenbuilder).
   Alternatively, plain Mockito mocks can be used for this as well.

This [example](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-resource-service/src/test/java/ch/admin/bit/jeap/jme/security/oauth/resource/PartnerResourceTest.java) shows how the `JeapAuthenticationToken` can be mocked for the test of a method with a
programmatic authorization check.

## Related

- [Testing secured REST APIs](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md) — the test-support classes used above, and the other test use cases.
- [How to: test a component with a given authentication](test-a-component-with-a-given-authentication.md) — the equivalent for integration tests that run inside a (partial) Spring application context.
- [How to: disable security in a Spring Boot test](disable-security-in-a-spring-boot-test.md) — mocking the same `jeapAuthorization` bean when security should otherwise be left out of a Spring Boot test.
