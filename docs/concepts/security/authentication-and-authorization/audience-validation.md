# Audience validation

Use this page when you need to understand audience validation and choose the applicable configuration
or migration guide.

An access token should be usable only at its intended resource servers. Audience restriction on access tokens
limits possible damage from a stolen token and prevents a token recipient from using the token at an unintended API.
See [OAuth 2.0 Security Best Current Practice, RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.3).

A matching audience does not itself grant access. Signature, issuer and time validation, followed
by role and data authorization, remain necessary.

## How it works

The calling **OAuth client** obtains an access token from an authorization server. The server puts
the permitted recipients in its `aud` claim. Each **resource server** checks whether its expected
resource identifier is among those recipients before accepting the token.

For example, a client with ID `shop-worker` obtains a token for the Orders API identified by the resource id
`https://resources.example.org/shop/orders`. The client ID identifies the caller; the resource ID identifies the
recipient. An `aud` token claim in an access token would then look like this:

```json
{
  "aud": ["https://resources.example.org/shop/orders"]
}
```
The Orders resource server must then check that its resource ID `https://resources.example.org/shop/orders`
is present in the `aud` claim before accepting the token.

For details see [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519.html#section-4.1.3) and [RFC 9068](https://www.rfc-editor.org/rfc/rfc9068.html#section-2.2).

## What jEAP validates

The jEAP Security Starter validates that the `aud` claim contains the `jeap.security.oauth2.resourceserver.resource-id`
value, which defaults to `spring.application.name`. Matching is exact: there is no URL normalization, wildcard matching
or path-prefix authorization.

Validation is governed by the `strict-audience-validation` configuration option. For otherwise valid `USER` and `SYS`
access tokens, the configuration option has these effects:

| Token audience | `off` | `warn` | `on` |
|---|---|---|---|
| Missing or empty | Accept | Accept and log a warning | Reject |
| Contains `resource-id` | Accept | Accept | Accept |
| Nonempty, without `resource-id` | Reject | Reject | Reject |

Thus `off` permits missing or empty audiences while still validating nonempty audiences. `B2B` tokens bypass
the jEAP audience validator in every mode; other token checks remain.

The current default is `off`; `on` will become the default in a future release. Therefore, existing applications
should migrate to support the strict mode. Follow the
[migration guide](audience-introduce-for-existing-resources.md#goal-require-audience-restriction-throughout-the-system)
to assess a whole system and enable strict validation incrementally.

For new applications, configure the intended audience and enable strict validation:

```yaml
jeap:
  security:
    oauth2:
      resourceserver:
        resource-id: https://resources.example.org/shop/orders
        strict-audience-validation: "on"
```

## Keycloak introspection client validation

Starting with version 26.6.2, Keycloak performs a separate audience check on token introspection: it requires the
introspection client's id to be in the introspected token's `aud` claim. This means two independent audience
checks happen for introspected access tokens:

| Check | Expected member of `aud` |
|---|---|
| Local jEAP resource-server validation | The configured `resource-id` |
| Keycloak introspection | The authenticated introspection client's ID |

Using the resource ID as the introspection client ID satisfies both checks with one audience entry.

Keycloak currently provides options to disable this additional introspection client audience check, but
those are already marked as deprecated. Therefore, existing applications that use token introspection
should migrate to support the additional introspection audience check. Follow the
[introspection goal in the migration guide](audience-introduce-for-existing-resources.md#goal-support-keycloaks-introspection-audience-check)
to assess a whole system and to satisfy Keycloak's introspection client validation.

## Migrating an existing system

The [migration guide](audience-introduce-for-existing-resources.md) provides one rollout procedure for
both goals, the strict audience validation in resource servers and the support of Keycloak's introspection
client audience validation. Start by choosing the scope: the introspection goal covers the inspected token
flows and any other recipients affected by their new audiences; system-wide strict validation requires assessing all
clients and resources. The guide then takes you through preparation, audience issuance and enforcement steps.

Introducing audiences for introspection already restricts affected tokens at jEAP resource servers. Enabling strict
validation at jEAP resource servers additionally makes audiences mandatory, including for tokens that are
not introspected. A migration to support Keycloak's introspection client audience validation can finish before the
remaining callers are ready for the strict audience validation at resource servers. Teams pursuing both goals can
reuse the same identifiers, mappings and verified token flows for both migrations.

## Related

- [Naming audiences](audience-naming.md) — choose resource boundaries and stable identifiers.
- [Configuring audiences in Keycloak](audience-configuration-in-keycloak.md) — issue the intended audiences in Keycloak.
- [Selecting audiences](audience-selection.md) — choose scopes through server or client configuration.
- [Token introspection on Keycloak](audience-for-token-introspection-on-keycloak.md) — configure the token introspection client audience check.
- [Migrating existing resource access to audience validation](audience-introduce-for-existing-resources.md) — choose the scope and follow the rollout through to enforcement.
- [Security Starter reference](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-starter#audience-validation) — look up properties and defaults.
