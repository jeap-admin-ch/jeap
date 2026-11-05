# How to: test a REST endpoint with full OAuth2 security

If a test of a REST request should also pass through the OAuth2 resource part of the security chain, a valid OAuth2
access token must be created for the request, and a JWKS endpoint must be available to verify the signature of the
access token. The configuration class
[JeapOAuth2IntegrationTestConfiguration](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter-test/src/main/java/ch/admin/bit/jeap/security/test/configuration/JeapOAuth2IntegrationTestConfiguration.java)
from the module `jeap-spring-boot-security-starter-test` makes both easy.

## Steps

1. Import the configuration `JeapOAuth2IntegrationTestConfiguration` in the test.
2. Override the following two OAuth2 resource properties appropriately:
   - `jeap.security.oauth2.resourceserver.authorization-server.jwk-set-uri`
   - `jeap.security.oauth2.resourceserver.authorization-server.issuer`
3. Create an OAuth2 access token suitable for the specific test case with the help of the `JwsBuilderFactory`.
4. Pass the access token as bearer authorization token in the header of the HTTP request to the protected
   resource.

This [test class](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-resource-service/src/test/java/ch/admin/bit/jeap/jme/security/oauth/resource/PartnerResourceBootServerWithSecurityIT.java) gives examples of Spring Boot tests with full security. The example uses
[REST Assured](http://rest-assured.io/) to implement the tests on the REST endpoints.
Setting the OAuth2 access token in the request is very simple: `given().auth().oauth2("the-token")...`

Details on how the test support provided by the `JeapOAuth2IntegrationTestConfiguration` works can be found in
[Test support](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md#test-support), in particular
[JeapOAuth2IntegrationTestConfiguration](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md#jeapoauth2integrationtestconfiguration)
and [ServletJwksEndpointMock](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md#servletjwksendpointmock).

## Related

- [Testing secured REST APIs](../../concepts/authentication-and-authorization/testing/testing-secured-rest-apis.md) — the test-support classes used above, and the other test use cases.
- [How to: disable security in a Spring Boot test](disable-security-in-a-spring-boot-test.md) — the opposite case, where a Spring Boot test should leave security aspects out.
- [Tokens in the Blueprint Microservice](../../concepts/authentication-and-authorization/tokens/tokens-in-the-blueprint-microservice.md) — structure and claims of the access tokens the `JwsBuilderFactory` creates.
