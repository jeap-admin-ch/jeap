# How to: disable security in a Spring Boot test

If the goal is only to test functionality, a cross-cutting concern such as security can unnecessarily
complicate the tests and distract from what a specific test is actually about. It can therefore be
legitimate to leave security aspects out of such tests. When using the `jeap-spring-boot-security-starter`,
a few things have to be taken into account for this.

If a Spring Boot test is executed, i.e. in particular a test with autoconfiguration enabled, and the
`jeap-spring-boot-security-starter` is part of the project, a web security configuration protecting the REST
endpoints from unauthorized access is activated automatically.

## Steps

To lift this protection for a test that should run without security aspects:

1. Import the configuration `DisableJeapSecurityStarterAutoConfiguration` from
   `jeap-spring-boot-security-starter-test` in the test.
2. If the application accesses the `jeapAuthorization` bean programmatically — e.g. to perform
   authorization checks or to obtain details about the user — define this bean in the test and mock it
   appropriately for the tests. This step does not apply if `jeapAuthorization` is only used in security
   annotations such as `@PreAuthorize`.

This [test class](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-resource-service/src/test/java/ch/admin/bit/jeap/jme/security/oauth/resource/PartnerResourceBootServerNoSecurityIT.java) gives examples of Spring Boot tests without security with a mocked `jeapAuthorization` bean.

## Related

- [Testing secured REST APIs](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md) — the test-support classes used above, and the other test use cases.
- [How to: test a REST endpoint with full OAuth2 security](test-a-rest-endpoint-with-full-oauth2-security.md) — the opposite case, where a Spring Boot test should pass through the whole security chain.
- [How to: test programmatic authorization checks in a unit test](test-programmatic-authorization-checks-in-a-unit-test.md) — mocking the `jeapAuthorization` bean outside a Spring application context.
