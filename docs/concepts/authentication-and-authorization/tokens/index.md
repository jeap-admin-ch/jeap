# Tokens

Access to a jEAP microservice is authorized with JSON Web Tokens (JWT) issued by an authorization server. This
section describes the tokens themselves and how jEAP deals with them: the format and claims of the access, refresh
and ID tokens used in the Blueprint Microservice and how they are validated, how a resource can transparently
introspect an access token on the authorization server to check its validity or to fetch data that is kept out of
the token, and how the size of access tokens is kept within the limits of the platforms they pass through.

**Start with** [Tokens in the Blueprint Microservice](tokens-in-the-blueprint-microservice.md), which defines the
token format every other page builds on. Read the other two pages when a resource needs more than the token itself
carries, or when access tokens grow too large.

## Contents

| Page | Description |
|---|---|
| [Tokens in the Blueprint Microservice](tokens-in-the-blueprint-microservice.md) | JSON Web Tokens: access, refresh and ID tokens, their claims and their validation |
| [Minimizing access token sizes](minimizing-access-token-sizes.md) | Dynamic scopes, lightweight access tokens, roles pruning and token compression |
| [Token introspection](token-introspection.md) | Transparent access token introspection in jEAP, caching of introspection results, and the configuration in jEAP and Keycloak |

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Audience restriction](../audience-restriction/index.md) — restricting the use of an access token to intended resources with its audience claim.
- [Protecting REST APIs](../protecting-rest-apis/index.md) — validating and authorizing the tokens on a resource server.
- [Authorization servers](../authorization-servers/index.md) — the servers issuing and introspecting the tokens.
