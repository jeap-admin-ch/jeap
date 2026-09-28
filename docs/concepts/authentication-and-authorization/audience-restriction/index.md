# Audience restriction

The audience claim of an access token names the resources the token is intended for. Validating it on the resource
server restricts the use of a token to those resources: a token obtained for one resource cannot be replayed against
another. This section describes how audiences work in jEAP and Keycloak, how they are named and configured, how a
client selects the audiences of the tokens it requests, why Keycloak's token introspection requires the introspecting
client in the audience, and how audience validation is introduced into existing systems without interrupting them.

**Start with** [Audience validation](audience-validation.md), which explains the concept and how jEAP and Keycloak
validate audiences. The following pages then go from naming and configuring audiences to the migration of existing
resources.

## Contents

| Page | Description |
|---|---|
| [Audience validation](audience-validation.md) | How access-token audiences restrict token use to intended resource servers, and how jEAP and Keycloak validate them |
| [Naming audiences](audience-naming.md) | Recommendations for choosing audience identifiers and the resource boundaries they represent |
| [Selecting audiences](audience-selection.md) | How to select audiences in access tokens for the resources a client needs to access |
| [Configuring audiences in Keycloak](audience-configuration-in-keycloak.md) | Configuring Keycloak client scopes and audience mappers to include intended resource servers in access-token audiences |
| [Token introspection on Keycloak](audience-for-token-introspection-on-keycloak.md) | Keycloak's requirement for introspection client IDs to appear in token audiences, with client configuration and compatibility options |
| [Migrating existing resource access to audience validation](audience-introduce-for-existing-resources.md) | Step-by-step introduction of access-token audiences in existing systems, supporting Keycloak introspection checks and strict jEAP resource-server validation |

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Tokens](../tokens/index.md) — the access tokens carrying the audience claim, and token introspection.
- [Protecting REST APIs](../protecting-rest-apis/index.md) — the resource server that validates the audience.
- [Authorization servers](../authorization-servers/index.md) — configuring Keycloak, which issues the tokens.
