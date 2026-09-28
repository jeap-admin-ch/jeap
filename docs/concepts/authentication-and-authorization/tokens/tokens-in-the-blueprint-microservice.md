# Tokens in the Blueprint Microservice

The processes used in the Blueprint Microservice to authenticate and authorize users work with different kinds of
tokens. The tokens differ in their content and purpose, but not in their structure: all tokens are signed
*JSON Web Tokens* (*JWT*, or, since they are signed, also *JWS*).

The tokens are issued by an authorization server, e.g. a Keycloak server.

The following three kinds of tokens occur in the Blueprint Microservice:

- access token
- refresh token
- identity token (ID token)

After a short description of the common token structure, the different kinds of tokens, their content and their usage
are described in more detail below.

## JSON Web Token

A JSON Web Token (JWT) is a string describing a JSON object that contains claims in the form of key-value pairs.
JWTs in the Blueprint Microservice are signed (JWS) and consist of three parts separated by a dot each:

- **Header** contains metadata
- **Payload** contains the claims
- **Signature** contains the signature of the payload

The individual parts are Base64url-encoded. For debugging purposes, the header and the payload of a JWS can be
decoded locally, for example with a shell one-liner such as
`echo "$TOKEN" | cut -d. -f2 | tr '_-' '/+' | base64 -d 2>/dev/null | jq .`, with an IDE plugin, or with another local tool.

> **Warning:** An access token is a bearer credential: anyone who holds it can use it until it expires. Never
> paste tokens issued by an authorization server of a real environment (including development and test stages)
> into an external website or service such as an online JWT decoder. Only tokens from a local mock server
> may be safe to decode with such tools.

## JWT signature and signature validation

The Blueprint Microservice requires that JWS are signed with the signing algorithm RSA with a strength of RSA-256 or
RSA-512. Microservices must always validate the signature of tokens. The certificates required for this should be
obtained through the [OpenID Connect Discovery interface](https://openid.net/specs/openid-connect-discovery-1_0.html)
of the authorization server.

## Access token

An access token allows a client application to execute a specific operation on a specific resource on behalf of a
user. As a concrete example, a web frontend (or a backend microservice) could be granted the permission by an access
token to change data on a (further) microservice on behalf of a logged-in user. An access token contains all
information (claims) a microservice (resource) needs to decide whether a certain operation may be executed or not.

In the Blueprint Microservice a resource (microservice) can expect the claims described below in an access token.
Additional claims are possible and must be ignored by the resource (microservice).

### Reserved claims

Reserved claims are claims defined by the JWT specification and are a central foundation for the interoperability of
tokens.

| Claim | Description | Example | Remarks |
| --- | --- | --- | --- |
| `jti` | JWT ID | `feb03e79-3e30-4300-9b64-36fbca41d379` | Usually a random UUID |
| `exp` | Expiration Date | `1575440084` | End of the token's validity |
| `nbf` | Not Before | `0` | Start of the token's validity. May be set to zero. |
| `iat` | Issued At | `1575440084` | Time the token was issued |
| `iss` | Issuer | `https://auth.some.domain.ch/realms/my-realm` | Issuer of the token |
| `sub` | Subject | `69368608-D736-43C8-5F76-55B7BF168299` | The subject authorized by the token, e.g. a user ID, a system ID, or a business partner ID. |
| `aud` | Audience | `[ "jme-security-resource-service" ]` | A list of systems and/or microservices. The granularity and the values depend on the business applications. May also be empty or missing if the token is not to be restricted to a specific audience. |

### Private claims

Private claims are claims that are only used within the Blueprint Microservice, i.e. they are specific to it and are
usually ignored by other systems.

| Claim | Description | Example | Remarks |
| --- | --- | --- | --- |
| `ctx` | Context of the user authentication | `SYS` | `USER`, `SYS` or `B2B`. See also [Authentication and authorization](../index.md) |
| `bproles` | Roles the user holds specifically for a business partner. | `{ "12345": ["jme_@thing_#read", "jme_@thing_#write"], "67890": ["jme_@thing_#read"] }` | May be null, in which case the user has no roles specific to a business partner. See also [Role concept in the Blueprint Microservice](../role-concept.md) |
| `userroles` | Roles the user holds independently of a business partner | `[ "jme_@thing_#read", "jme_@thing_#write" ]` | May be null, in which case the user has no roles independent of a business partner. See also [Role concept in the Blueprint Microservice](../role-concept.md) |
| `allowed-origins` | Source systems that may make CORS requests | `[ "https://my.domain.ch" ]` | Only relevant for UIs. May be null, in which case no systems may make CORS requests. |
| `ext_id` | Unique identification of the user in eIAM | `287365` | Ext-Id of the user in eIAM. |
| `admin_dir_uid` | U/X number from the Admin-Dir | `U12345678` / `X12345678` | ID of the user in the Admin-Dir, if known. |
| `login_level` | Kind/strength of the login the user used to log in to the system | `S3` | Examples of levels are: S3, S2, S1, S0, SA. |

### OpenID standard claims

These claims are defined by the OpenID Connect specification and mainly serve to describe (certified) properties of a
user. In the Blueprint Microservice the following OIDC standard claims are part of the access token if it was issued
for the user context, but not if it was issued for the system or B2B context.

| Claim | Description | Example | Remarks |
| --- | --- | --- | --- |
| `name` | User's full name in displayable form including all name parts | `Max Muster` |  |
| `given_name` | Given name(s) or first name(s) of the user. | `Max` |  |
| `family_name` | Surname(s) or last name(s) of the user. | `Muster` |  |
| `locale` | User's locale | `DE` | Language preferred by the user |

OIDC standard claims are typically part of ID tokens. In the Blueprint Microservice, however, the access token also
contains a selected subset of these claims.

### Usage

Access tokens serve authorization. In the Blueprint Microservice they are transmitted as *Bearer* tokens in the HTTP
*Authorization* header of a request to a REST resource, and the resource checks, mainly based on the `bproles` and
`userroles` claims, whether a request can be permitted or not.

Access tokens are typically short-lived to limit the potential for misuse should an access token fall into the wrong
hands.

### Token size

Infrastructure and library components may restrict the maximum supported size of HTTP headers. Up to 8 KB should
normally not be a problem for headers. Assuming a role identifier is 20 characters long on average, this would allow
listing about 300 roles. If more roles are needed, corresponding tests and clarifications would have to be made (what
header sizes Spring allows, the network infrastructure, etc.). Browsers usually already support larger headers.

If tokens become too large, the approaches discussed in
[Minimizing access token sizes](minimizing-access-token-sizes.md) can be considered.

## Refresh token

A refresh token allows a client application to obtain a new access token without having to ask the user again. A
refresh token is only exchanged between the authorization server and the client application, in contrast to access
tokens, which are additionally exchanged between the client application and resources. This allows choosing a long
lifetime for refresh tokens compared to access tokens. A refresh token can, so to speak, bridge the short lifetime of
access tokens.

Typically a refresh token is issued together with an access token. In this case the refresh token (despite its "long"
lifetime) can usually be used only once, to prevent misuse should a refresh token fall into the wrong hands.

The concrete content of a refresh token is generally irrelevant to the client application.

### Usage

A refresh token is obtained together with an access token according to one of the OAuth 2.0 flows, and an access token
is renewed according to the OAuth 2.0 refresh token flow.

In the user context of the Blueprint Microservice, refresh tokens should not be used for web UIs. The browser is not a
good place to store the usually long-lived refresh tokens. At most short-lived access tokens should be used in the
browser. Therefore, in web UIs access tokens should be renewed exclusively by silent refresh, i.e. with renewed
authentication requests with the parameter `prompt=none`.

The use of refresh tokens can, however, make sense in mobile apps, as such apps can protect secrets more reliably.

As of Keycloak version 14, the generation of refresh tokens can be disabled. The corresponding configuration option is
configured per client and can be found on a client under "Settings / OpenID Connect Compatibility Modes / Use Refresh
Tokens". In older Keycloak versions the generation of refresh tokens cannot be disabled yet. However, the maximum
validity of refresh tokens can be configured per client ("Client Session Idle" and "Client Session Max" under
"Advanced Settings" of the Keycloak client configuration).


## ID token

An identity token (ID token) describes identity properties of an authenticated user. The OpenID Connect standard
claims standardize the description of certain user properties such as last name, first name, e-mail address, etc.

In the Blueprint Microservice the ID token currently contains no OIDC standard claims that are not already contained
in the access token. Except for a few rather technical claims, the content of an ID token in the Blueprint Microservice
is therefore identical to the content of the access token.

### Usage

In the Blueprint Microservice, on an authentication for the user context the authorization server issues an identity
token (ID token) in addition to the access and refresh token. The authorization server also provides a *UserInfo*
endpoint (according to OpenID Connect) through which the same user information can additionally be queried.

In the Blueprint Microservice the ID token also contains the `bproles` and `userroles` claims. The information from
these two claims can be used, e.g. in a browser frontend, to improve usability. However, the ID token must never be
used to actually check a user's permissions for accessing a resource. For this, the resource server must use the
access token exclusively.

## Integration

In the Blueprint Microservice, tokens are typically issued by the authorization server [Keycloak](../authorization-servers/keycloak.md) or, for
B2B purposes by a B2B gateway. In addition, the [OpenID Connect / OAuth2 mock server](../testing/oauth2-mock-server.md)
is available, which is mainly used in local development or on the DEV environment.

The authorization of accesses to REST resources based on access tokens is supported by the jEAP Security Starter
library (see [Authentication and authorization for REST APIs](../protecting-rest-apis/rest-api-authentication-and-authorization.md)).

## Example tokens

Example access token, user context:

```json
{
  "jti": "83aa82d5-a3d6-4b2c-9935-c4b8a865d50c",
  "exp": 1575638090,
  "nbf": 0,
  "iat": 1575637790,
  "iss": "https://auth.our.domain.ch/realms/jme",
  "sub": "69368608-D736-43C8-5F76-55B7BF168299",
  "typ": "Bearer",
  "nonce": "8109d2ce431d294b51d0a390ec99e82849SeqmO8J",
  "auth_time": 1575637787,
  "session_state": "49a21728-811c-49e6-b161-64cad3f94132",
  "allowed-origins": [
    "https://jme.our.domain.ch"
  ],
  "scope": "openid profile",
  "ext_id": "287365",
  "bproles": {
    "1000063457": [
      "jme_@partner_#read",
      "jme_@thing_#read",
      "jme_@thing_#write"
    ]
  },
  "ctx": "USER",
  "userroles": [],
  "name": "Max Muster",
  "preferred_username": "69368608-d736-43c8-5f76-55b7bf168299",
  "locale": "DE",
  "given_name": "Max",
  "family_name": "Muster",
  "login_level": "S3OK"
}
```

Example access token, system context:

```json
{
   "jti":"dd8576f2-740a-4387-9262-786dce40a10b",
   "exp":1575639806,
   "nbf":0,
   "iat":1575639506,
   "iss":"https://identity.example.ch/auth/realms/jme",
   "sub":"006ff33f-b249-4314-8e20-f3e6aad40043",
   "typ":"Bearer",
   "auth_time":0,
   "session_state":"b687c134-a111-47e2-8172-174ffb57a83d",
   "scope":"profile",
   "clientHost":"172.17.0.1",
   "clientId":"jme-security-client-service",
   "ctx": "SYS",
   "userroles":[
      "jme_@partner_#read",
      "jme_@partner_#write"
   ],
   "clientAddress":"172.17.0.1"
}
```

## Further documentation

- [RFC 7519: JSON Web Token (JWT)](https://tools.ietf.org/html/rfc7519)
- [RFC 7515: JSON Web Signature (JWS)](https://tools.ietf.org/html/rfc7515)
- [OpenID Connect Core 1.0 Specification](https://openid.net/specs/openid-connect-core-1_0.html)
- [OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749)
- [JSON Web Token Best Current Practices, OAuth Working Group](https://tools.ietf.org/html/draft-ietf-oauth-jwt-bcp-07)

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Authentication and authorization for REST APIs](../protecting-rest-apis/rest-api-authentication-and-authorization.md) — validating access tokens and authorizing requests with the jEAP Security Starter.
- [Role concept in the Blueprint Microservice](../role-concept.md) — the roles carried in the `userroles` and `bproles` claims.
- [Integrating different authorization servers](../authorization-servers/integrating-different-authorization-servers.md) — transforming tokens with other claims into the expected format.
- [Minimizing access token sizes](minimizing-access-token-sizes.md) — approaches when tokens become too large.
- [Audience validation](../audience-restriction/audience-validation.md) — how the `aud` claim is validated.
- [Keycloak](../authorization-servers/keycloak.md) — the authorization server issuing the tokens.
- [OpenID Connect / OAuth2 mock server](../testing/oauth2-mock-server.md) — issuing tokens in local development.
