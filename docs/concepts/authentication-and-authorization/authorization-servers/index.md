# Authorization servers

An authorization server issues the access tokens with which clients authenticate towards jEAP microservices, and
thereby controls the access to the resources of a system. In the Blueprint Microservice this is Keycloak, an
open-source identity and access management server that makes users, technical users and their roles available to
the microservices through OpenID Connect / OAuth2. Because jEAP Security builds on these standards rather than on a
specific product, other standard-compliant authorization servers can be integrated as well. This section describes
Keycloak and how it is configured securely for jEAP, how a provider authorizes the applications consuming its
resources through Keycloak clients, how the access tokens of another authorization server are adapted to the format
jEAP expects, and how authentication works when the microservices of a system run on more than one platform.

**Start with** [Keycloak](keycloak.md), the authorization server of the Blueprint Microservice. The other pages
cover specific situations: authorizing consuming applications in the system context, integrating an authorization
server whose tokens differ from the jEAP format, and authentication across platforms.

## Contents

| Page | Description |
|---|---|
| [Keycloak](keycloak.md) | Keycloak as the authorization server of the Blueprint Microservice: terms and concepts, security notes on redirect URIs and audiences, the event log for troubleshooting, and running Keycloak locally with Docker |
| [Authorizing Keycloak clients for consuming application resources](authorizing-keycloak-clients-for-consuming-applications-resources.md) | How a provider authorizes consuming business applications in the system context through Keycloak clients and their service account roles |
| [Integrating different authorization servers](integrating-different-authorization-servers.md) | Transforming the access tokens of an authorization server into the format jEAP Security expects with claim set converters |
| [Cross-platform authentication](cross-platform-authentication.md) | Authentication across platforms with one or two authorization servers, and moving resources between platforms |

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Tokens](../tokens/index.md) — the tokens the authorization server issues, introspects and keeps small.
- [Audience restriction](../audience-restriction/index.md) — configuring the audiences of the issued tokens in Keycloak.
- [Testing](../testing/index.md) — the OAuth2 mock server replacing Keycloak for local development and testing.
