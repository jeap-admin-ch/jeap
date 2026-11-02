# How to: enable and debug jEAP token introspection

## Enable token introspection

1. Select the jEAP Security library
   [introspection mode](../../concepts/authentication-and-authorization/tokens/token-introspection.md#introspection-modes)
   that fits your resource server's use case (`none`, `lightweight`, `always`, `custom` or `explicit`).
2. Configure Keycloak for the selected mode: register an
   [introspection client](../../concepts/authentication-and-authorization/tokens/token-introspection.md#introspection-clients)
   and, if needed, the
   [jEAP Roles Pruning Token Mapper](../../concepts/authentication-and-authorization/tokens/token-introspection.md#roles-pruning).
3. Configure your resource server with the selected mode and the introspection client parameters — see
   [Configuration of the token introspection in jEAP](../../concepts/authentication-and-authorization/tokens/token-introspection.md#configuration-of-the-token-introspection-in-jeap)
   for the full property reference.

See the [jme-security-example](https://github.com/jme-admin-ch/jme-security-example) for a worked example
with the jEAP OAuth Mock Server, including an endpoint that returns the roles fetched by introspection.

## Debug the authorizations of an introspected user

A lightweight access token created by roles pruning does not list a user's roles, so decoding the access
token (JWT) alone no longer shows the user's authorizations. To debug them instead:

- **Decode the ID token** instead of the access token — both are returned together in Keycloak's token
  response, and roles pruning only affects the access token.
- **Call the token introspection endpoint** yourself with the user's access token and the introspection
  client's credentials. The JSON response includes the user's roles as assigned by Keycloak.
- **Enable the jEAP [current-user endpoint](../../concepts/frontend/current-user-endpoint.md)** in the
  microservice and call it with the user's access token — the response includes the roles jEAP Security
  assigned, whether fetched from the token or by introspection.
- **Enable debug logging on access-denied:** set
  `jeap.security.oauth2.resourceserver.log.access-denied.debug: true` in addition to
  `...log.access-denied.enabled: true` (see
  [Authentication and authorization for REST APIs](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authentication-and-authorization.md#configuration)).
  This logs a denied user's roles at debug level.

## Related

- [Token introspection](../../concepts/authentication-and-authorization/tokens/token-introspection.md) — introspection modes, caching, metrics and the Keycloak-side configuration reference.
- [Minimizing access token sizes](../../concepts/authentication-and-authorization/tokens/minimizing-access-token-sizes.md) — roles pruning and lightweight tokens.
- [jeap-oauth-mock-server — Getting started](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-oauth-mock-server/getting-started)
