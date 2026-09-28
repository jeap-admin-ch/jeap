# Protecting REST APIs

Every REST API of a jEAP microservice must be authenticated and authorized, including APIs that are only called
internally. The jEAP Security Starter turns a microservice into an OAuth2 resource server: it validates the JWT
bearer access token of every request, converts it into a jEAP authentication and lets the application authorize the
request against the roles carried in the token. This section describes how a REST API is protected this way, which
steps jEAP Security runs through for a request, and the three authorization models the roles of a token can be
checked against: simple roles, semantic roles and authorities derived from roles. It also describes how to provide an
additional Spring Security configuration for the APIs of a microservice that should not be protected as an OAuth2
resource.

**Start with** [Authentication and authorization for REST APIs](rest-api-authentication-and-authorization.md). It
covers the integration and configuration of the jEAP Security Starter and explains where authorization takes place.
Then pick the page of the authorization model your application uses; consult the
[role concept documentation](../role-concept.md) for choosing between the models.

If your microservice also provides APIs that should not be protected as an OAuth2 resource, but should e.g. be public
or protected with basic auth, read [Spring Security configuration](spring-security-configuration.md). It gives
guidance on providing the additional Spring Security configuration needed and points to the JME example projects
with working example configurations.

## Contents

| Page | Description |
|---|---|
| [Authentication and authorization for REST APIs](rest-api-authentication-and-authorization.md) | Protecting REST APIs with the jEAP Security Starter: integration, configuration and where authorization takes place |
| [Authorization with simple roles](rest-api-authorization-with-simple-roles.md) | Declarative and programmatic authorization checks against simple roles |
| [Authorization with semantic roles](rest-api-authorization-with-semantic-roles.md) | Declarative and programmatic authorization checks against semantic roles, role and business partner queries |
| [Authorization with authorities](rest-api-authorization-with-authorities.md) | Deriving fine-grained authorities from roles and authorizing against them |
| [Spring Security configuration](spring-security-configuration.md) | Providing an additional Spring Security configuration for APIs that are not protected as an OAuth2 resource, e.g. public or basic auth protected APIs |
| [JWT access token authorization flow in jEAP Security](jwt-access-token-authorization-flow.md) | The steps and components jEAP Security runs through when authorizing a request with a JWT bearer token |

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Role concept in the Blueprint Microservice](../role-concept.md) — user roles, business partner roles and the role models.
- [Tokens](../tokens/index.md) — the access tokens a protected REST API validates.
- [Calling secured REST APIs from Java](../calling-secured-rest-apis-from-java.md) — the client side: calling a protected REST API from a microservice.
- [Testing](../testing/index.md) — testing protected REST APIs and running them against the OAuth2 mock server.
