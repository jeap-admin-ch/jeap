# How to: create a Keycloak introspection client for a resource

jEAP recommends a dedicated confidential introspection client per resource, with its client ID equal to the
resource's `resource-id` — this way the same audience entry satisfies both the resource server's own
audience check and Keycloak's introspection-client audience check (required since Keycloak 26.6.2), and
each resource keeps independent access and credential rotation.

On managed platforms, client provisioning and server-wide compatibility options are typically owned by the
platform team — coordinate the setup, credential delivery and the later removal of compatibility options
with them.

## Steps

To create the introspection client for a resource with id `https://resources.example.org/shop/orders`, in
the target realm's Admin Console:

1. Open **Clients → Create client**. Choose **Client type: OpenID Connect** and
   **Client ID: `https://resources.example.org/shop/orders`**.
2. In **Capability config**, set **Client authentication: On** and **Authorization: Off**. Leave all
   **Authentication flow** capabilities disabled: Standard flow, Direct access grants, Implicit flow,
   Service account roles, OAuth 2.0 Device Authorization Grant and OIDC CIBA Grant. Also leave Standard
   Token Exchange and JWT Authorization Grant disabled if displayed. Introspection authenticates the client
   directly — it needs no token-issuing flows, roles or scopes.
3. Save the client. Under **Credentials**, use **Client Authenticator: Client Id and Secret** and provision
   the client secret to the resource server through its normal secret management.

## Configure the resource server in jEAP

For a resource server with id `https://resources.example.org/shop/orders` already using `lightweight`
introspection:

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

Since jEAP Security Starter **24.26.0**, an omitted `introspection.client-id` falls back to `resource-id`, so
token introspection automatically uses the resource ID as the introspection client ID, as Keycloak's check
requires.

Also assign the audience scopes to the **token-obtaining clients** — see
[Keycloak configuration](../../concepts/authentication-and-authorization/audience-restriction/audience-configuration-in-keycloak.md) — and enable both
**Add to lightweight access token** and **Add to token introspection** on the audience mapper, since jEAP
validates the JWT before introspecting it and needs the `aud` claim present either way.

## Related

- [Audience for token introspection on Keycloak](../../concepts/authentication-and-authorization/audience-restriction/audience-for-token-introspection-on-keycloak.md) — the full backward-compatibility and naming rationale.
- [Migrate existing resource access to audience validation](migrate-to-audience-restriction.md) — the rollout procedure this client creation is one step of.
- [How to: enable and debug jEAP token introspection](enable-and-debug-token-introspection.md)
