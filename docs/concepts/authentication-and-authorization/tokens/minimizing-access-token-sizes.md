# Minimizing access token sizes

In HTTP requests from a client to a resource, access tokens usually are provided to the resource as bearer tokens in
HTTP authentication headers. If a user is authorized to act on behalf of many business partners, the user's access
token might exceed size limits established by applications or network components. This page describes technical
solutions to work around such limits.

## Access token for a specific business partner

Often, a user authorized to act on behalf of many business partners works for just one of those
business partners at a time. In such cases, an access token containing just the roles the user has been granted for
this business partner is sufficient. Such an access token would be much smaller than an access token containing all
the roles for all the business partners the user is authorized for.

The jEAP Keycloak plugin provides a specific custom token mapper named "Scoped Businesspartner Access Token
Mapper" which restricts the business partner roles included in an access token to a given business partner.
The requested business partner has to be specified in an authentication request as the variable part of the dynamic
Keycloak scope `bproles`.

**See [How to: restrict business partner roles in a token with the dynamic scope `bproles`](../../../how-tos/security/use-dynamic-oauth2-scopes.md)**
for requesting a token scoped to one partner, to all partners, or without partner roles, and for the required
Keycloak configuration.

## Opaque/lightweight access tokens

The OAuth2 standard does not require an access token to be a JWT that explicitly lists the user's authorizations.
An access token can also just be an opaque string with only the authorization server knowing the authorizations
attached to the token. The validity of such a token and the associated user authorizations can be queried at the
authorization server's token introspection endpoint by passing the access token as a parameter. Access to the
token introspection endpoint is restricted to authenticated and authorized clients, specifically "confidential
clients". The jEAP security library supports transparent token introspection. For details, see
[Token introspection](token-introspection.md).

Keycloak does not support opaque access tokens; it always issues readable JWT tokens. However, starting with Keycloak
version 23 (released in November 2023), the content of an access token and the content of a corresponding token
introspection endpoint response can differ in terms of the user information they contain. This was made possible by
adding the new "**Add to token introspection**" switch to token mappers, complementing the existing "*Add to access
token*" switch. Keycloak version 24 officially introduced **lightweight access tokens**. In this version, a new token
mapper switch "**Add to lightweight access token**" explicitly determines whether a mapper adds information to a
lightweight access token or not. By default, this switch is off for most standard mappers.

If a client uses such a lightweight access token to authorize a request to a resource, the resource cannot directly
derive the user's authorizations from the token. Instead, the resource must first query the Keycloak token
introspection endpoint, providing the token as a parameter to retrieve the user's authorizations. These additional
queries to the Keycloak token introspection endpoint are part of the costs associated with using lightweight tokens.
Other potential costs include increased latency for resource responses due to introspection queries. The jEAP
Security library can [cache introspection results](token-introspection.md#caching-of-introspection-results) in the
resource to reduce these costs.

**See [How to: use lightweight access tokens with Keycloak](../../../how-tos/security/use-lightweight-access-tokens.md)**
for enabling mappers on lightweight tokens and configuring a client to issue them.

## Jeap Roles Pruning Token Mapper

The jEAP Keycloak plugin provides a Jeap Roles Pruning Token Mapper which will
remove the `userroles` and `bproles` claims from a token if the number of characters used by those claims exceeds a
given limit. If the mapper has pruned the roles, it adds the claim `roles_pruned_chars`, which contains the number
of characters the pruned claims would have used.

The Jeap Roles Pruning Token Mapper can be used to restrict the size of access tokens, as the size of those tokens
is usually dominated by the number of roles a user has. If a user has more roles than should fit in an access
token, the Jeap Roles Pruning Token Mapper can be used to prune those roles from the token.

If a client uses an access token that had its roles pruned by the Jeap Roles Pruning Token Mapper to authorize a
request to a resource, the resource cannot directly derive the user's authorizations from the token. Instead, the
resource must first query the Keycloak token introspection endpoint, providing the access token as a parameter to
retrieve the user's authorizations. These additional queries increase the latency of the resource's responses.

**See [How to: prune roles from access tokens with the Jeap Roles Pruning Token Mapper](../../../how-tos/security/prune-roles-from-access-tokens.md)**
for adding the mapper to a client and sizing its character limit.

## Access token compression

Large access tokens commonly occur when a user has identical permissions for a significant number of business
partners. These tokens are, in principle, well-suited for effective compression. Since HTTP/2 supports header
compression, switching from HTTP/1.1 to HTTP/2 could address issues caused by excessively large headers.

## Further documentation

- [Keycloak client scopes](https://www.keycloak.org/docs/latest/server_admin/#_client_scopes)
- [OAuth 2.0 Token Introspection (RFC 7662)](https://datatracker.ietf.org/doc/html/rfc7662)

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Role concept in the Blueprint Microservice](../role-concept.md) — user roles and business partner roles.
- [Tokens in the Blueprint Microservice](tokens-in-the-blueprint-microservice.md) — token types and claims.
- [Token introspection](token-introspection.md) — resolving pruned or lightweight tokens at the authorization server.
- [Keycloak](../authorization-servers/keycloak.md) — about the Keycloak authorization server.
- [OpenID Connect / OAuth2 mock server](../testing/oauth2-mock-server.md) — dynamic scope support in the mock server.
- [How to: use dynamic OAuth2 scopes](../../../how-tos/security/use-dynamic-oauth2-scopes.md) — restrict business partner roles in a token to one partner, all partners, or none.
- [How to: use lightweight access tokens](../../../how-tos/security/use-lightweight-access-tokens.md) — issue Keycloak lightweight access tokens.
- [How to: prune roles from access tokens](../../../how-tos/security/prune-roles-from-access-tokens.md) — cap token size with the Jeap Roles Pruning Token Mapper.
