# Token introspection

jEAP Security can transparently introspect access tokens on the authorization server, either to verify that a
token is still valid or to fetch authorization data that is not contained in the token itself. This page describes
the token introspection support of jEAP Security, its introspection modes, the required configuration in jEAP and
in Keycloak, and how to enable and debug it.

## OAuth 2.0 token introspection

Token introspection allows a resource server (e.g. a microservice) to query an authorization server (e.g. Keycloak)
about a token presented to it by a client. The authorization server's response states whether the
token is currently active and which access rights it carries. Token introspection is an OAuth 2 extension
specified in [RFC 7662](https://datatracker.ietf.org/doc/html/rfc7662).

The two main purposes for a token introspection are

- **checking the validity of a token**<br/>
  The authorization server is the final authority on the validity of the tokens it issued. A token might become
  invalid before its declared lifetime has expired, e.g., when the authentication session it belongs to is
  terminated or when the token is explicitly revoked. If a resource needs to make absolutely sure a token is currently
  valid, it must introspect the token.
- **determining the authorizations associated with a token**<br/>
  A token might be opaque or not contain all the data required by a resource to check the authorization of a client.
  In such cases a resource has to introspect the token to determine whether the client is allowed to access the
  resource.

Token introspection is restricted to authorized resources, i.e., resources known to the authorization server and
allowed to access its [introspection endpoint](https://datatracker.ietf.org/doc/html/rfc7662#section-2). Typically,
this means that such a resource must also be registered as a confidential client.

Practical use cases for token introspection include:

- Making sure that a token is valid and hasn't been revoked before performing a sensitive operation
- Keeping sensitive information out of JWTs by making such information only available via introspection
- Keeping JWTs small by providing potentially large information only via introspection (e.g. extensive authorization
  lists)

## Transparent access token introspection in jEAP

The jEAP Security library provides built-in support for the introspection of an access token. Depending on a
configured *introspection mode*, the library will transparently introspect an access token if needed. If
introspection takes place, the library will enrich the Spring Security `Authentication` with the authentication data
provided by the introspection endpoint, if the authorization server reported the introspected token as
active. If the authorization server reports the token as inactive, the jEAP Security library throws an
authentication exception and the request to the resource server is denied.

![Token introspection flow: the client accesses a resource of the microservice (resource server) with an access token as Bearer; jEAP Security inside Spring Security, in introspection mode, sends the access token to Keycloak (authorization server) for introspection, receives the introspection result (active? authentication data), builds the Authentication that @PreAuthorize checks, and returns the resource response (resource data or auth error) to the client](images/token-introspection-jeap-token-introspection.svg)

Please note that the introspection of a token will

- add latency to the requests addressed to a resource
- add load to the authorization server and network
- decrease the availability of a resource because of the additional runtime dependency on the authorization server

### Introspection modes

The jEAP Security library supports five different *introspection modes*:

| Mode | Description | Default |
| --- | --- | --- |
| **none** | No access token will be introspected. | yes |
| **lightweight** | Only lightweight access tokens will be introspected, i.e. tokens that don't contain all the data. | |
| **always** | All access tokens will be introspected. | |
| **custom** | Access tokens will be introspected depending on a developer-defined custom condition. | |
| **explicit** | An access token will only be introspected when explicitly required. | |

The following sections detail when to use which introspection mode.

#### none

The introspection mode *none* should be used when access tokens issued by an authorization server always contain all
needed data and it is sufficient to check the validity of an access token based on just the token's content alone.
In such cases, the jEAP Security library will check

1. that the token has been issued by the configured authorization server
2. that the token has been signed by the configured authorization server
3. that the token signature is strong enough
4. that the token is valid in respect to its `exp` (expiration time) claim and its `nbf` (not before) claim
5. that the resource server is listed in the audience of the token if the `audience` claim is defined
6. that the issuer is allowed to issue tokens in the declared authentication context (`ctx` claim)

These basic validity checks also apply to all other introspection modes.

#### lightweight

The introspection mode *lightweight* should be used when access tokens issued by an authorization server *cannot*
or *should not* contain all the data needed by a resource.

A typical use case would be that access tokens get too big to be passed as bearer tokens in the HTTP authorization
header. This might happen if a user has a large number of roles that should be embedded in their access tokens. For such
cases, the jEAP Keycloak plugin provides the [Jeap Roles Pruning Token Mapper](#roles-pruning) that will replace
the jEAP roles claims in an access token with a claim that indicates that the roles are missing from the token. For
such tokens, the jEAP Security library (in the introspection mode *lightweight*) will transparently fetch the missing
roles from the introspection endpoint. This approach keeps access tokens self-contained as long as all the
roles granted to a user don't take up too much space in the token. The additional HTTP request to the token
introspection endpoint is only required for users with many roles. Therefore, using the introspection mode
*lightweight* in combination with the Jeap Roles Pruning Token Mapper is a good fit for situations where only a small
percentage of users has more roles than the access token size limit of a platform allows. In such
situations only a small percentage of the requests to a resource need their tokens introspected on the
authorization server, and the negative impacts of the introspection requests are limited to this small
percentage of the requests.

Another use case would be that some sensitive information should be provided to a resource server but should not be
included in the access tokens that are visible to the client. For such cases, the Keycloak feature
[lightweight tokens](minimizing-access-token-sizes.md#opaquelightweight-access-tokens) can be used. If an access token
includes the scope `lightweight`, the jEAP Security library (in the introspection mode *lightweight*) will
transparently fetch the missing information from the introspection endpoint. If *all* access tokens issued by an
authorization server are lightweight, the introspection mode *always* could be used as well.

#### always

The introspection mode *always* should be used when all access tokens of an authorization server should be
introspected.

A typical use case would be that the validity of all access tokens must be checked every time on the authorization
server in order to reject access tokens that have been revoked or that belong to a closed authorization session. For
such cases it is important to know the expected number of requests to the resource, as every request to the resource
will also result in an additional request to the token introspection endpoint on the authorization server. Therefore,
the sizing of the authorization server must reflect the expected load caused by the token introspection requests. In
addition, keep in mind that the latency of requests to a resource increases by the latency
of the query to the authorization server's token introspection endpoint.

#### custom

The introspection mode *custom* should be used when the introspection of an access token should depend on aspects not
covered by the other pre-defined introspection modes. For such cases, the jEAP Security library allows developers to
provide their own introspection condition by implementing the interface `JeapJwtIntrospectionCondition`.

#### explicit

The introspection mode *explicit* should be used when only some access tokens of an authorization server need to be
introspected and the introspection is only required by certain functionalities of a resource.

A typical use case would be that only some functionality of a resource is especially sensitive and requires that the
validity of a token is checked on the authorization server every time before the functionality is executed. For such
cases, the jEAP Security library provides an annotation for methods that should only be executed
after the validity of the provided access token has been successfully checked on the authorization server.

## Configuration of the token introspection in jEAP

The introspection mode to be used by a microservice (resource server) can be configured using the following
property:

| Property | Optional | Value |
| --- | --- | --- |
| **`jeap.security.oauth2.resourceserver.introspection.mode`** | yes | **`none`** → No access token will be introspected<br/>**`lightweight`** → Only lightweight access tokens will be introspected, i.e. tokens that don't contain all the data<br/>**`always`** → All access tokens will be introspected<br/>**`custom`** → Access tokens will be introspected depending on a developer-defined custom condition<br/>**`explicit`** → An access token will only be introspected when explicitly required |

Setting this property to `none` is the same as not configuring the property at all. In both cases no introspection
takes place and no additional introspection-related configuration is needed.

For all other cases, additional introspection configuration must be provided for all configured authorization
servers. The jEAP Security library will verify at startup that the appropriate configurations are in place.

In jEAP Security, there are three configuration roots that can configure authorization servers:

| Configuration root | Optional | Purpose |
| --- | --- | --- |
| **`jeap.security.oauth2.resourceserver.authorization-server`** | yes | Configuring the standard authorization server for the authentication contexts `USER` and `SYS` |
| **`jeap.security.oauth2.resourceserver.b2b-gateway`** | yes | Configuring the standard authorization server for the authentication context `B2B` |
| **`jeap.security.oauth2.resourceserver.auth-servers`** | yes | Configuring a list of additional authorization servers with their authentication contexts |

For every authorization server the following introspection properties can be configured:

| Property | Optional | Value |
| --- | --- | --- |
| **`introspection.client-id`** | no | ID of a confidential client configured on the authorization server (required to access the introspection endpoint)<br/>(see [Introspection clients](#introspection-clients)) |
| **`introspection.client-secret`** | no | Secret of the client (required to access the introspection endpoint) |
| **`introspection.uri`** | yes | URI of the token introspection endpoint on the authorization server.<br/>If not configured, it is derived from the issuer URL. |
| **`introspection.connect-timeout-in-millis`** | yes | Connection timeout on token introspection requests in milliseconds. Defaults to 8000. |
| **`introspection.read-timeout-in-millis`** | yes | Read timeout on token introspection requests in milliseconds. Defaults to 8000. |
| **`introspection.mode`** | yes | Specify mode `none` to disable the introspection of the authorization server's tokens. Other introspection modes *cannot* be configured here. |

An example configuration with introspection mode *lightweight*, three trusted authorization servers, and token
introspection explicitly disabled on the b2b-gateway:

```yaml
jeap:
  security:
    oauth2:
      resourceserver:
        introspection.mode: lightweight
        authorization-server:
          issuer: "https://keycloak/auth/realm"
          introspection:
            client-id: "some-client-id-1"
            client-secret: "some-secret-1"
        b2b-gateway:
          issuer: "https://b2b/auth"
          introspection.mode: none
        auth-servers:
          - issuer: "https://other-issuer"
            introspection:
              uri: "https://other-issuer/protocol/openid-connect/token/introspect"
              client-id: "some-client-id-3"
              client-secret: "some-secret-3"
              authentication-contexts: user
```

### Custom introspection condition

If (and only if) the introspection mode is configured to `custom`, jEAP Security will introspect a token depending on
a developer-defined custom condition. The custom condition must implement the interface
`JeapJwtIntrospectionCondition` and must be provided to jEAP Security as a Spring bean.

```java
public interface JeapJwtIntrospectionCondition {

    boolean needsIntrospection(Jwt jwt);

}
```

## Caching of introspection results

The costs of token introspection like latency, load, runtime dependency, etc. are incurred for every introspected
request. Many of these introspections are redundant: a client typically presents the same access token to a resource
many times during the token's lifetime, e.g. a UI issuing a series of requests on behalf of a user, and the
authorization server answers each of these introspections with the same result. To avoid this redundancy, the jEAP
Security library can cache introspection results locally in a resource instance. With the cache enabled, an access
token presented repeatedly to a resource is typically introspected only once per resource instance, and subsequent
requests with the same token are served from the cached result until it expires. A cached result never outlives its
token: it expires at the latest when the token expires, and earlier if a configured time to live has passed. Only
results reporting a token active are cached. The cache is disabled by default and is configured per authorization
server, independently of the introspection mode.

Whether caching is appropriate depends on the *purpose* of the introspection, which is for the resource to judge:

- **Introspection to load data that is deliberately kept out of the token.** This is the purpose of the introspection
  modes *lightweight* and *custom*, and of the mode *always* if all tokens of an authorization server are
  lightweight. Here caching is a good fit: the data fetched for a token, e.g. the roles of the user, is normally
  stable for the lifetime of the token, and serving it from the cache puts a lightweight token almost on par with a
  self-contained token. Caching removes most of the costs of introspection while retaining the benefits of small
  or opaque tokens.
- **Introspection to check that a token is still valid.** This is the typical purpose of the introspection mode
  *always* with self-contained tokens: rejecting tokens that have been revoked or belong to a closed authorization
  session. A cached result cannot answer this question, as it reflects the state of the token at the time of its
  introspection, not the current state. For this purpose the cache should stay disabled. Explicit validity checks
  (introspection mode *explicit*) always query the authorization server regardless of the cache, as they are about
  the current state of a token by definition.

Two further aspects are relevant when deciding on caching:

- **Scope of the cache.** The cache is local to a resource instance. With several instances of a resource, every
  instance introspects a token itself, so the reduction of the introspection load is by a factor of the number of
  requests per token and instance, not the total number of requests per token. A distributed cache can be provided
  by the resource if this is not sufficient.
- **Consistency of the cached data.** Changes on the authorization server, e.g. a role revoked from a user, reach a
  resource with a cached result only after the cached result has expired. The configured time to live for cached 
  introspection results bounds this delay; it should be chosen according to how quickly such changes must take effect
  in the resource server (keeping in mind that a self-contained token would carry the stale data until the token
  expires as well).

For the configuration of the token introspection cache, its exact expiry and cache key semantics, the replacement of
the default local cache by a distributed one, its metrics and how to analyze its behavior in the logs, see
[Caching introspection
responses](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-starter#caching-introspection-responses)
in the jEAP Security starter documentation.

## Explicit token validity check

Will be added with JEAP-5472.

## Metrics

jEAP Security provides the following Micrometer metrics regarding its token introspection functionality:

| Name | Type | Description | Dimensions |
| --- | --- | --- | --- |
| `jeap.security.token.introspection.conditional.introspections` | counter | Counts the number of conditional token introspections executed by jEAP Security, the actual execution of a token introspection depending on the configured introspection mode / condition. | issuer, active, introspected |
| `jeap.security.token.introspection.validity.checks` | counter | Counts the number of validity checks executed by jEAP Security. | issuer, active |
| `jeap.security.token.introspection.endpoint.requests` | timer | Times the requests to a token introspection endpoint executed by jEAP Security. | issuer, active,<br/>percentiles (0.5, 0.75, 0.9, 0.99) |
| `jeap.security.token.introspection.cache.lookups` | counter | Counts the lookups in the introspection result cache executed by jEAP Security. | issuer, result |

The metrics may provide the following dimensions:

| Name | Description | Values |
| --- | --- | --- |
| issuer | The issuer of an introspected token | `{issuer name}`<br/>unknown |
| active | Has an introspected token been reported active by the authorization server? | true<br/>false<br/>unknown |
| introspected | Has a token been introspected depending on the configured introspection mode / condition? | true<br/>false |
| result | The result of a lookup in the introspection result cache | hit<br/>miss<br/>skipped (token not cacheable) |

"unknown" values for "active" may result if a token has not been introspected or if the introspection failed.
"unknown" values for "issuer" may result if a token doesn't have an "iss" claim.

## Configuration of the token introspection in Keycloak

### Introspection clients

Token introspection is restricted to authorized resources, i.e., resources known to the authorization server and
allowed to access its introspection endpoint. Typically, this means that such a resource must also be registered as a
confidential client on the authorization server.

In Keycloak, such a client doesn't need special scopes or roles. The client just has to be an OIDC/OAuth2 client
configured with "Client authentication" set to "on"; there is no need to enable any authentication flow for the client.
"Client Authenticator" must be configured as "Client Id and Secret". Keycloak will then generate a secret which can be
copied from the "Client Secret" field.

As an introspection client needs no authorization other than access to the token introspection
endpoint, one client can be used for all resources of a system on an authorization server. Still, to
decouple the resources, it might make sense to use different introspection clients for different resources of a
system.

Since Keycloak 26.6.2, the introspection client's ID must additionally be present in the audience of the introspected
access token. See [Audience for token introspection on Keycloak](../audience-restriction/audience-for-token-introspection-on-keycloak.md) for
the recommended naming of introspection clients and the required audience configuration.

### Roles pruning

Roles pruning helps limit the size of access tokens, which is usually dominated by the number of roles a
user has. jEAP provides a custom Keycloak token mapper, the
[jEAP Roles Pruning Token Mapper](minimizing-access-token-sizes.md#jeap-roles-pruning-token-mapper), that can be used
to prune roles from a token if a user has more roles than should fit in an access token.

To enable roles pruning on a client, the "jEAP Roles Pruning Token Mapper" must be added to the client. The mapper
has a configuration option to set the maximum allowed roles size. The option is named "Maximum allowed accumulated
roles characters" and defaults to 8000.

The jEAP Roles Pruning Token Mapper must be activated as follows:

- Add to access token: **true**
- Add to userinfo: **false**
- Add to ID token: **false**
- Add to lightweight access token: **false**
- Add to token introspection: **false**

There are two main options to add the mapper to a client:

- Add the mapper to the client-specific scope `<client>-dedicated` (which Keycloak creates by default).<br/>
  With this option, the maximum roles size can be set differently for each client as needed.
- Define a new optional scope named `roles-pruning` and add the mapper to that scope. Then, on each client, add the
  `roles-pruning` scope as a default scope. This option only supports a realm-wide configuration of the maximum roles
  size. (Otherwise, you would need to define separate scopes for different configurations.)

### Lightweight scope

Will be added with JEAP-5473.

## How to enable jEAP token introspection

Follow these general steps to enable jEAP token introspection on a resource server (microservice):

1. Select the jEAP Security library [introspection mode](#introspection-modes) that supports your resource server's
   use case
2. [Configure your Keycloak](#configuration-of-the-token-introspection-in-keycloak) realm to support the selected
   introspection mode
3. [Configure your resource server](#configuration-of-the-token-introspection-in-jeap) with the selected
   introspection mode and the required introspection client configuration parameters

## Example

The [jme-security-example](https://github.com/jme-admin-ch/jme-security-example)
demonstrates how to configure lightweight access token introspection in a project. It uses the
[jeap-oauth-mock-server](https://github.com/jeap-admin-ch/jeap-oauth-mock-server) (see
[OpenID Connect / OAuth2 mock server](../testing/oauth2-mock-server.md)) as authorization server. The
[jme-security-example-resource-service](https://github.com/jme-admin-ch/jme-security-example/tree/main/jme-security-resource-service)
implements an endpoint `/api/introspected-roles` which expects to be called with a Bearer token and then returns the
roles that were not directly included in the token but have been transparently fetched by the
`jeap-spring-boot-security-starter` library from the authorization server's token introspection endpoint. The
[jme-security-example-client-service](https://github.com/jme-admin-ch/jme-security-example/tree/main/jme-security-client-service)
provides the same endpoint, but as a public endpoint that calls the protected endpoint with a Bearer token using a
selected OAuth2 client configuration.

## How to debug the authorizations of users with introspected tokens

A lightweight access token created by roles pruning will not list a user's roles. Therefore, the user's
authorizations can no longer be debugged by just decoding the access token (JWT). How can the
authorizations associated with a lightweight access token be debugged then?

- You can decode the ID token instead of the access token, if you have access to the user's ID token. Both tokens are
  returned together in Keycloak's response to the token request. The user's roles are only pruned from the
  access token, not from the ID token.
- You can call the token introspection endpoint with a user's access token and the credentials of the introspection
  client. The response is a JSON document that includes the user's roles as assigned by Keycloak.
- You can enable the [jEAP current-user endpoint](../../frontend/current-user-endpoint.md) in your microservice and
  call this endpoint with a user's access token. The response is a JSON document that includes the user's roles as assigned in
  the microservice's Spring Security authentication built by jEAP Security (roles are fetched from the access token
  or by introspection from Keycloak).
- You can enable `jeap.security.oauth2.resourceserver.log.access-denied.debug` in addition to
  `jeap.security.oauth2.resourceserver.log.access-denied.enabled` (see
  [Authentication and authorization for REST APIs](../protecting-rest-apis/rest-api-authentication-and-authorization.md#configuration)).
  This will log a user's roles at debug level if access to a resource is denied by jEAP Security.

## Further documentation

- [OAuth 2.0 Token Introspection (RFC 7662)](https://datatracker.ietf.org/doc/html/rfc7662)
- [Token introspection in the jEAP Security starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-starter#token-introspection) — configuration reference of the introspection and its result cache.

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Minimizing access token sizes](minimizing-access-token-sizes.md) — roles pruning and lightweight access tokens in Keycloak.
- [Audience for token introspection on Keycloak](../audience-restriction/audience-for-token-introspection-on-keycloak.md) — configure the token introspection client audience check.
- [Authentication and authorization for REST APIs](../protecting-rest-apis/rest-api-authentication-and-authorization.md) — configuration of jEAP Security in a resource server.
- [OpenID Connect / OAuth2 mock server](../testing/oauth2-mock-server.md) — authorization server for local development and testing.
- [Current-user endpoint](../../frontend/current-user-endpoint.md) — inspect the roles jEAP Security assigned to a user.
