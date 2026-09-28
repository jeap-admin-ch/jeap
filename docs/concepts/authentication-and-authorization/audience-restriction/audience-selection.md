# Selecting audiences

Use this page when configuring or implementing how a client selects audiences at token acquisition.

The authorization server controls which audiences a client can obtain. With the
[Keycloak scope-and-mapper setup](audience-configuration-in-keycloak.md), the client selects from
assigned resource scopes; it cannot write arbitrary recipients into its token. These scopes choose
recipients, while roles govern what the caller may do there.

## Three ways to select

| Selection | Where it happens | Behavior |
|---|---|---|
| Server assignment | Keycloak Default Client Scopes | Audience is included even when the application does not request the scope |
| Client configuration | A fixed scope list, such as a Spring client registration | Application explicitly requests configured scopes when obtaining a token |
| Runtime selection | Application logic using the current call or state | Application requests a token with the appropriate scope combination |

Default/static scopes remain effective in all three cases. Use optional/dynamic scopes for audiences that must
be deselectable.

## Select at token acquisition

For **Authorization Code**, request the scopes in the authorization request. For **Client
Credentials**, request them at the token endpoint. The following excerpts show the encoded scope
parameters; other flow parameters, client authentication, state and PKCE are managed by the OAuth
client integration.

Authorization request for `shop-frontend`, selecting Orders:

```text
GET /realms/shop/protocol/openid-connect/auth?...&scope=openid%20resource-https%3A%2F%2Fresources.example.org%2Fshop%2Forders
```

Client-credentials token request for `shop-worker`, selecting Orders and Inventory:

```http
POST /realms/shop/protocol/openid-connect/token HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Authorization: Basic <encoded-client-credentials>

grant_type=client_credentials&scope=resource-https%3A%2F%2Fresources.example.org%2Fshop%2Forders%20resource-https%3A%2F%2Fresources.example.org%2Fshop%2Finventory
```

Spaces separate scope names before URL/form encoding. `openid` requests OIDC login semantics in
the first example; it is not an audience selector. Use an OAuth client library to construct complete requests.

## Configuring Spring client registrations for dynamic audience selection

For a fixed Orders audience, configure
`spring.security.oauth2.client.registration.<registrationId>.scope`:

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          orders:
            provider: shop
            client-id: shop-worker
            client-secret: ${SHOP_WORKER_CLIENT_SECRET}
            authorization-grant-type: client_credentials
            scope:
              - resource-https://resources.example.org/shop/orders
        provider:
          shop:
            issuer-uri: https://keycloak.example.org/realms/shop
```

Use `JeapOAuth2RestClientBuilderFactory.createForClientRegistryId("orders")` to build the
corresponding client. For several known target combinations, define separate registrations with
different scope lists. Application logic can choose between those prepared clients at runtime. See the
[Security Client Starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-client-starter#building-a-restclient).

## Default/static audience assignments

For a client that always needs the same audience, assign the corresponding scope as default/static.
This way the application does not need to request it explicitly. A Spring client registry configuration
for the client can then omit the scope configuration entirely.

## Testing audience selection with the mock server

The jEAP OAuth Mock Server's default mapper writes the fixed `audience` list configured per client;
requesting different resource scopes does not change `aud`. For local tests of several audience
combinations, configure a mock client per combination and use those client IDs in your test
registrations. Allow the requested scopes in the mock configuration as well; see the
[Mock Server reference](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-oauth-mock-server/configuration).
This simulates the resulting audiences. Verify actual scope-to-audience selection against Keycloak.

## Resource Indicators
[RFC 8707](https://www.rfc-editor.org/rfc/rfc8707.html#section-2) defines the standard `resource`
parameter as another selection mechanism. jEAP currently uses scopes as Keycloak does not yet support Resource
Indicators (though Keycloak 26.7 added experimental support).

## Related

- [Audience validation](audience-validation.md) — understand what recipients validate.
- [Naming audiences](audience-naming.md) — choose resource identifiers.
- [Keycloak configuration](audience-configuration-in-keycloak.md) — assign scopes and audience mappers.
- [Security Client Starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-client-starter#building-a-restclient) — build clients for token acquisition or forwarding.
- [Migrating existing resource access to audience validation](audience-introduce-for-existing-resources.md) — choose the scope, coordinate callers and recipients, and enable validations.
