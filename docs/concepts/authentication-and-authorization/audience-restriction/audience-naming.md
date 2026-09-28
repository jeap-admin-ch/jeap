# Naming audiences

Use this page when choosing a resource boundary and an audience identifier for it.

Choose an audience for a deliberate resource boundary, normally one API or microservice. For new
identifiers, we recommend a stable logical HTTPS URL under a domain controlled by your organization:

```text
https://resources.example.org/<system>/<resource>
```

The domain above is an anonymized example. Set the chosen identifier as the resource server's
`resource-id` and issue that exact value in access tokens. This is a recommendation for new names,
not a requirement to rename existing, working audiences.

## Choose the boundary first

An audience identifies an intended token recipient. Several endpoints of one API can share an
audience; permissions for operations and individual records belong in authorization rules.

A shared audience for several services is possible, but deliberately creates a larger trust
boundary: a token for one service also passes the audience check at the others. Prefer separate
audiences where services should be isolated. For a token that legitimately addresses two APIs,
include both identifiers instead of creating a system-wide audience.

The standard jEAP validator checks one `resource-id` per resource server.

## What the standards require

Audience syntax and resource discovery solve related but different problems:

| Standard | Consequence for naming |
|---|---|
| [JWT, RFC 7519](https://www.rfc-editor.org/rfc/rfc7519.html#section-4.1.3) | `aud` contains case-sensitive `StringOrURI` values. A value containing a colon must be a URI. A simple name is otherwise valid. |
| [Resource Indicators, RFC 8707](https://www.rfc-editor.org/rfc/rfc8707.html#section-2) | A requested `resource` must be an absolute URI without a fragment; queries should normally be avoided. It can be a logical identifier and need not resolve to an API. |
| [JWT Access Token Profile, RFC 9068](https://www.rfc-editor.org/rfc/rfc9068.html#section-2.2) | This profile requires `aud` and recommends including the requested `resource` value when resource indicators are used. |
| [Protected Resource Metadata, RFC 9728](https://www.rfc-editor.org/rfc/rfc9728.html#section-1.2) | The resource identifier is an HTTPS URL. Actual metadata publication requires a corresponding metadata endpoint as well. |

RFC 8707 allows the authorization server to map a requested resource URI to another audience identifier.
jEAP recommends using the same value for `resource` and `aud` as a simplifying convention, but this is not a
universal OAuth requirement.

## Compare the naming options

| Option | Strengths | Tradeoffs |
|---|---|---|
| `spring.application.name`, such as `shop-orders-service` | Existing jEAP fallback; no extra resource configuration | Identity changes if the application name changes; a separate resource URI and mapping would be needed for RFC 8707 |
| Explicit logical name, such as `example.shop.orders` | Independent of deployment names; readable | Requires governance; still needs a resource URI mapping for RFC 8707 |
| URN in an appropriate registered namespace | Stable, independent of DNS and already an absolute URI | Must follow that namespace's rules; no direct HTTPS metadata-discovery path |
| Logical HTTPS URL, such as `https://resources.example.org/shop/orders` | Stable across deployments and access paths; fits the recommended convention | Requires control of the domain and a plan if metadata is later published |
| Physical API URL | Directly connects identity to the API the client calls | Internal, external and environment-specific addresses may create several identities for one logical API |

For URNs, you can use an existing suitable registered namespace of your organization under its
assignment rules. Creating a new formal or informal namespace means taking responsibility for its
registration, assignment rules and maintenance; see
[RFC 8141](https://www.rfc-editor.org/rfc/rfc8141.html#section-5). Do not invent an unregistered namespace identifier.

## jEAP recommendation
jEAP recommends the logical HTTPS option for three reasons:

- An absolute URI allows the same value for RFC 8707's `resource` and the token's `aud`, avoiding a
  separate mapping. An application name ties the security identity to deployment naming; a separate
  logical name needs governance too but still lacks the URI's interoperability benefit.
- HTTPS works under an organization-controlled domain when no suitable registered URN namespace is
  available, and leaves RFC 9728 metadata publication open. A URN remains a valid choice under a
  suitable namespace's rules.
- A logical URL keeps one security identity across internal, external and environment-specific API
  addresses. Using physical addresses can create several identities for the same resource.

### Introspection client names

For a token introspection client, use a dedicated confidential client whose ID equals the resource ID.
Note: HTTPS URLs and URNs can be client IDs.

## Keep the identity consistent

Specify exact spelling, including case and trailing slashes. The jEAP audience check does not
normalize URLs. Treat an identifier change as a token-contract change, independent of deployment
renaming.

## Logical vs physical HTTPS URLs

A logical URL decouples the security identity from DNS names used for traffic, ingress routes and
deployments. It is an identifier, not an instruction to send API calls to that address. The same
logical audience can be used across environments, if issuer validation and trust configuration
reliably isolate those environments. Review this explicitly when a resource trusts several issuers
or accepts calls across realms.

A physical API URL makes the relationship between identity and network destination more immediate.
However, an externally accessed frontend and an internally called backend may expose the same
logical API through different addresses.

Neither URL choice implements Protected Resource Metadata by itself. RFC 9728 requires a real
[metadata endpoint](https://www.rfc-editor.org/rfc/rfc9728.html#section-3), derived by inserting
`/.well-known/oauth-protected-resource` before the resource path. For the logical example, that is
`https://resources.example.org/.well-known/oauth-protected-resource/shop/orders`. Later publication
must resolve DNS, TLS, routing, environment separation, and internal versus external reachability.

## Related

- [Audience validation](audience-validation.md) — understand the two checks.
- [Keycloak introspection](audience-for-token-introspection-on-keycloak.md) — configure the resource's introspection client.
- [Keycloak configuration](audience-configuration-in-keycloak.md) — map the chosen audience identifiers into tokens.
- [Audience selection](audience-selection.md) — select the intended resources when obtaining tokens.
