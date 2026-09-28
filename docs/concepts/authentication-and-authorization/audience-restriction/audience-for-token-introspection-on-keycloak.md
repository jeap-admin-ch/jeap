# Audience for token introspection on Keycloak

Use this page when configuring the audiences of tokens introspected by a resource server to pass
Keycloak's token introspection client audience check.

For an existing system, follow the [migration guide](audience-introduce-for-existing-resources.md#goal-support-keycloaks-introspection-audience-check)
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

Either effective exception permits a missing audience membership, subject to the other introspection checks.
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

On managed platforms, client provisioning and server-wide compatibility options are typically owned
by the platform team. Coordinate the setup, credential delivery and the later removal of compatibility options with them.

To create the introspection client for a resource with id `https://resources.example.org/shop/orders`, go to the
target realm's Admin Console and follow these steps:

1. Open **Clients → Create client**. Choose **Client type: OpenID Connect** and
   **Client ID: `https://resources.example.org/shop/orders`**.
2. In **Capability config**, set **Client authentication: On** and **Authorization: Off**.
   Leave all **Authentication flow** capabilities disabled: Standard flow, Direct access grants,
   Implicit flow, Service account roles, OAuth 2.0 Device Authorization Grant and OIDC CIBA Grant.
   Also leave Standard Token Exchange and JWT Authorization Grant disabled if displayed.
   Introspection authenticates the client directly; it needs no token-issuing flows, roles or scopes.
3. Save the client. Under **Credentials**, use **Client Authenticator: Client Id and Secret**
   and provision the client secret to the resource server through its normal secret management.

## Configuring the resource server in jEAP

For a resource server with id `https://resources.example.org/shop/orders` already using `lightweight` introspection:

```yaml
jeap:
  security:
    oauth2:
      resourceserver:
        resource-id: https://resources.example.org/shop/orders
        introspection:
          mode: lightweight
        authorization-server:
          issuer: https://keycloak.example.org/realms/shop
          introspection:
            client-secret: ${ORDERS_INTROSPECTION_CLIENT_SECRET}
```

Since jEAP Security Starter **24.26.0**, an omitted `introspection.client-id` falls back to `resource-id`,
so that token introspection automatically uses the resource ID as the introspection client ID,
as required by Keycloak's introspection client audience check.

## Related

- [Audience validation](audience-validation.md) — distinguish local validation from introspection.
- [Naming audiences](audience-naming.md) — choose the resource/client identifier.
- [Keycloak configuration](audience-configuration-in-keycloak.md) — issue audiences to the calling clients.
- [Audience migration guide](audience-introduce-for-existing-resources.md) — prepare token audiences, switch existing introspection clients and coordinate enforcement.
- [Security Starter reference](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-starter#token-introspection) — configure jEAP resource server token introspection.
