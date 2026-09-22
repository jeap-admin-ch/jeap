# Authentication and authorization

Authentication establishes the identity of users and services. Authorization determines which resources
they may access and which operations they may perform. This section collects concepts and practical
guidance for authentication and authorization in jEAP applications.

| Topic | Description |
|---|---|
| [Audience validation](audience-validation.md) | How access-token audiences restrict token use to intended resource servers, and how jEAP and Keycloak validate them |
| [Naming audiences](audience-naming.md) | Recommendations for choosing audience identifiers and the resource boundaries they represent |
| [Token introspection on Keycloak](audience-for-token-introspection-on-keycloak.md) | Keycloak's requirement for introspection client IDs to appear in token audiences, with client configuration and compatibility options |
| [Configuring audiences in Keycloak](audience-configuration-in-keycloak.md) | Configuring Keycloak client scopes and audience mappers to include intended resource servers in access-token audiences |
| [Selecting audiences](audience-selection.md) | How to select audiences in access tokens for the resources a client needs to access |
| [Migrating existing resource access to audience validation](audience-introduce-for-existing-resources.md) | Step-by-step introduction of access-token audiences in existing systems, supporting Keycloak introspection checks and strict jEAP resource-server validation |

## Related

- [Security](../index.md) — navigate the parent topic.
