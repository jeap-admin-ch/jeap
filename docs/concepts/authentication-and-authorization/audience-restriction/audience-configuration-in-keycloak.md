# Configuring audiences in Keycloak

Use this page when configuring the scopes and mappers that put resource audiences into access tokens.

Use one reusable OpenID Connect client scope per resource, containing one explicit **Audience**
mapper. Assign that scope to each calling client as **Default** for an always-present audience, or
as **Optional** when the client application should request it. Several resource scopes produce
several audience entries.

This makes recipient selection explicit and keeps it separate from roles and permissions. A
scope's name alone does not create an audience: its mapper writes the `aud` entry. Avoid mixing
this approach with role-driven **Audience Resolve** mappers that add unintended recipients.

The following steps use the Keycloak 26.7 Admin Console terminology. They configure audiences
for existing calling clients; retain their existing authentication and grant settings. For a live
system, follow the [migration guide](audience-introduce-for-existing-resources.md) to choose the affected
clients and resources and deploy receivers before assigning new scopes.

If your platform manages realms declaratively, apply the same scope, mapper and assignment settings
through that mechanism. The settings and their rollout order also apply there.

## Identify the resource and caller

Choose the resource identifier using [Naming audiences](audience-naming.md). The example in this documentation uses:

| Purpose | Value |
|---|---|
| Calling OAuth client | `shop-frontend` or `shop-worker` |
| Orders application name | `shop-orders-service` |
| Orders `resource-id` and token audience | `https://resources.example.org/shop/orders` |
| Resource-selection client scope | `resource-https://resources.example.org/shop/orders` |
| Orders introspection client ID, if needed | `https://resources.example.org/shop/orders` |
| Second resource | `https://resources.example.org/shop/inventory` |

The scope name follows the naming convention `resource-<resource-name>`, including the full logical HTTPS resource name.
The logical resource URL is neither the API's configured network address nor an automatically
provided discovery endpoint.

## Create a resource scope

In the realm, open **Client scopes → Create client scope**:

| Setting | Value |
|---|---|
| Name | `resource-https://resources.example.org/shop/orders` |
| Protocol | `OpenID Connect` |
| Type | `None` |
| Include in token scope | `On` |
| Include in OpenID Provider Metadata | `On` |

Save the scope. **Type: None** keeps it out of the realm's automatic Default/Optional assignments
for new clients. It does not make the scope Optional on any particular client; assign it explicitly
below. **Include in token scope** exposes its name in the token's scope claim and introspection
response. **Include in OpenID Provider Metadata** advertises it through discovery, without itself
granting a client access to it.

## Add the audience mapper

Open the scope's **Mappers** tab, select **Configure a new mapper** (or **Add mapper → By
configuration** when mappers already exist), and choose **Audience**:

| Setting | Value |
|---|---|
| Name | `orders-audience` |
| Included Client Audience | Leave unset |
| Included Custom Audience | `https://resources.example.org/shop/orders` |
| Add to ID token | `Off` |
| Add to access token | `On` |
| Add to lightweight access token | `On` |
| Add to token introspection | `On` |

Save the mapper. Use the exact same identifier as the resource server. The lightweight setting is
needed because jEAP validates the JWT before introspection; reconstructing `aud` only in the
introspection response is insufficient for strict local validation.

When applying these settings through an API, omit `included.client.audience` instead of serializing
it as an empty string.

Repeat these steps for Inventory with scope `resource-https://resources.example.org/shop/inventory`,
mapper name `inventory-audience`, and custom audience `https://resources.example.org/shop/inventory`.

## Assign scopes to callers

Open **Clients → calling client → Client scopes → Add client scope**. Select the resource scope,
then use **Add → Default** or **Add → Optional**:

| Assignment | Effect |
|---|---|
| Default | The audience is included without an explicit scope request. Omitting it from the request cannot deselect it. |
| Optional | The client must name the scope when obtaining a token to include this audience. |

Assign only the resources the client needs. Optional selection may be fixed in application
configuration or determined at runtime; it is not inherently dynamic. A Default scope may also be
requested explicitly, for example in a Spring client registration, to document the expected
assignment. See [Selecting audiences](audience-selection.md) for examples and the limits of that check.

## Remove unintended role-driven audiences

Inspect the calling client's effective mappers, including inherited client scopes. Keycloak's
built-in `roles` scope normally contains an **Audience Resolve** mapper named `audience resolve`,
which adds the IDs of clients whose roles are included in the token to `aud`. If this produces a
nonempty audience without the receiving jEAP resource's `resource-id`, `USER`/`SYS` requests fail.
Even when the intended ID is present, additional recipients broaden where the token can pass an
audience check. For this explicit-audience setup, remove that mapper from the effective configuration.
Do not delete the whole `roles` scope: its other mappers may be needed to issue roles.

If the resource uses introspection, create its separate
[introspection client](audience-for-token-introspection-on-keycloak.md#creating-the-introspection-client-in-keycloak). The
resource scopes above belong on the callers that obtain tokens, not on that introspection client.

## Verify the result

Under **Clients → calling client → Client scopes → Evaluate**, inspect the effective mappers and
generated token. Test no optional resource scope, one scope, and two scopes; Default audiences must
remain in all cases. Then obtain real tokens through the application's grant flow and inspect `aud`:

```json
{
  "aud": [
    "https://resources.example.org/shop/orders",
    "https://resources.example.org/shop/inventory"
  ]
}
```

This excerpt shows both resource scopes being effective. Check normal and, where used,
lightweight access tokens, and compare the introspection response. Also check that no unintended
audiences remain. Evaluation previews do not replace these integration checks.

## Related

- [Keycloak audience support](https://www.keycloak.org/docs/latest/server_admin/#audience-support) — understand the mapper model.
- [Audience validation](audience-validation.md) — check the receiving side's behavior.
- [Naming audiences](audience-naming.md) — choose resource identifiers.
- [Audience selection](audience-selection.md) — request the configured scopes.
- [Keycloak introspection](audience-for-token-introspection-on-keycloak.md) — configure introspection clients.
- [Migrating existing resource access to audience validation](audience-introduce-for-existing-resources.md) — follow a process to enable Keycloak introspection audience compatibility, strict audience validation, or both.
