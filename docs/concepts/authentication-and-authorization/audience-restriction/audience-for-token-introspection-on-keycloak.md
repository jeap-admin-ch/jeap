# Audience for token introspection on Keycloak

Use this page when configuring the audiences of tokens introspected by a resource server to pass
Keycloak's token introspection client audience check.

For an existing system, follow the
[migration guide](../../../how-tos/security/migrate-to-audience-restriction.md#goal-support-keycloaks-introspection-audience-check)
to identify the affected token flows and roll out the required changes in the right order. This page provides
the configuration details used by that guide.

Since Keycloak **26.6.2**, the authenticated introspection client's ID must be present in the
inspected access token's audience. Otherwise, introspection returns `{"active": false}` unless a
backward compatibility exception applies.

[RFC 7662](https://www.rfc-editor.org/rfc/rfc7662.html#section-2.1) requires authentication and
authorization of introspection requests, but does not prescribe this client-ID membership rule, which is
specific to Keycloak.

## Keycloak's temporary backward compatibility options

Keycloak provides two temporary backward compatibility exceptions:

| Scope | Setting |
|---|---|
| Server-wide | `--spi-login-protocol--openid-connect--allow-token-introspection-without-audience-check=true`; set to `false` (the default) or remove to disable the exception |
| Introspecting client | **Clients → client → Advanced → OpenID Connect Compatibility Modes → Allow token introspection without audience check: On** |

Either exception, if effective, allows the introspection client's ID to be missing from the audience; the other introspection checks still apply.
See the [provider configuration reference](https://www.keycloak.org/server/all-provider-config#_openid_connect).

Since these options are already marked as deprecated, jEAP recommends migrating to the target configuration
described below, rather than relying on the exceptions.

## Use the resource ID as the introspection client ID

jEAP recommends a dedicated confidential introspection client per resource, with its client ID equal
to the resource's `resource-id`.

A different introspection client ID would need its own entry in the inspected token's audience.
Using the resource ID avoids that extra entry. In addition, separate introspection clients
preserve resource-specific access and independent credential rotation. 

## Assigning audience scopes
Assign audience scopes to the **token-obtaining clients** as described in [Keycloak configuration](audience-configuration-in-keycloak.md).

If an introspected token has no `aud` claim, Keycloak can reconstruct the audience for its introspection client
audience check. jEAP, however, validates the JWT before introspecting it. Therefore, always enable both
**Add to lightweight access token** and **Add to token introspection** in the
[Keycloak audience mapper configuration](audience-configuration-in-keycloak.md#add-the-audience-mapper).

## Creating the introspection client in Keycloak

**See [How to: create a Keycloak introspection client for a resource](../../../how-tos/security/configure-keycloak-introspection-client.md)**
for the client-creation steps and the matching jEAP resource-server configuration.

## Related

- [Audience validation](audience-validation.md) — distinguish local validation from introspection.
- [Naming audiences](audience-naming.md) — choose the resource/client identifier.
- [Keycloak configuration](audience-configuration-in-keycloak.md) — issue audiences to the calling clients.
- [How to: migrate existing resource access to audience validation](../../../how-tos/security/migrate-to-audience-restriction.md) — prepare token audiences, switch existing introspection clients and coordinate enforcement.
- [Security Starter reference](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-starter#token-introspection) — configure jEAP resource server token introspection.
