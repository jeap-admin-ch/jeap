# How to: test a REST controller with MockMvc

For efficient integration tests on REST controllers, Spring Test provides **MockMvc** for WebMvc
applications. It runs integration tests on controllers without starting a whole application server each
time. With MockMvc, the Spring Security `Authentication` with which a test request is executed can be set
explicitly on the request.

## Steps

1. Add the test dependency `jeap-spring-boot-security-starter-test` to the project (see
   [Integration](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md#integration)).
   This dependency automatically configures a web security configuration with the highest priority that
   simply lets all requests through. Since the test adds the `JeapAuthenticationToken` instances with
   which requests are executed directly via MockMvc, no further authentication filters should be traversed
   in the web filter chain.
2. Write the integration test using MockMvc, setting the `JeapAuthenticationToken` with which the request
   is executed explicitly on the request. jEAP provides an example of testing an OAuth2 resource using
   [MockMvc](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-resource-service/src/test/java/ch/admin/bit/jeap/jme/security/oauth/resource/PartnerResourceMockMvcIT.java)
   directly. For those who prefer REST Assured, there is also an example of how the tests can be written
   [in REST Assured syntax on top of MockMvc](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-resource-service/src/test/java/ch/admin/bit/jeap/jme/security/oauth/resource/PartnerResourceRestAssuredIT.java).
3. In the Spring Boot application started for the test, activate the auto-configuration of the
   `jeap-spring-boot-security-starter` for OAuth2 resources so that security is configured appropriately.
   This means that the following property must be set:
   `jeap.security.oauth2.resourceserver.authorization-server.issuer`

## Related

- [Testing secured REST APIs](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md) — the test-support classes used above, and the other test use cases.
- [How to: test a component with a given authentication](test-a-component-with-a-given-authentication.md) — verify authorization in isolation, without going through the HTTP request processing chain.
- [How to: test a REST endpoint with full OAuth2 security](test-a-rest-endpoint-with-full-oauth2-security.md) — pass a real access token through the whole OAuth2 resource security chain instead of setting the authentication directly.
- [Authentication and authorization for REST APIs](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authentication-and-authorization.md) — how access to REST APIs is secured.
