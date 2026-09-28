# Keycloak

**Keycloak** is an open-source identity and access management (IAM) software by Red Hat. Keycloak can reliably
protect applications and services with as little additional code as possible. It can perform authentication itself
or integrate existing identity providers. Out of the box it supports OAuth2/OpenID Connect and SAML, both
towards applications and towards identity providers. In the Blueprint Microservice, Keycloak is used for
authentication. Technical users in the system context are managed directly in
Keycloak. To use Keycloak, a realm must be created on a Keycloak instance.

The following table lists some important Keycloak terms and concepts:

| Name | Description |
| --- | --- |
| Realm | A separate configuration. Several realms can run on the same Keycloak instance but are otherwise completely separated. |
| Client | An application in a realm. This can be an application that wants to access another one, an application the user logs in to, or an application that is only accessed. |
| User | A user who can log in and access applications. |
| Service Account | A special user that a client can use to access another application without an actual user. It is fixed to one client. → technical user |
| Role | A role that can be assigned to a user. Describes what the user may do on a system. There are realm roles that are valid on all clients, and there are client-specific roles. A client-specific role may only be used on that client. |
| Identity Provider | An external system that can perform authentication and confirm the identity of users. |
| Authentication Flows and States | Authentication in Keycloak is carried out by means of authentication states, which are grouped into authentication flows. For example, there is an authentication flow for the login with a browser, one for a logout, etc. More specialized login procedures can be integrated by means of custom flows. The [Keycloak documentation](https://www.keycloak.org/docs/latest/server_admin/#_authentication-flows) describes how authentication flows are configured. |
| Token Mapper | Token mappers can be defined to determine which information is stored in the issued access token. They map user information to token claims. |

## Security notes

### Do not use the wildcard "*"

In the configuration options "Valid Redirect URIs", "Valid post logout redirect URIs" and "Web origins", the
wildcard character "*" should not be used, in particular not in place of a subdomain. In the CORS configuration,
"+" can be used, because this automatically configures the origins from "Valid Redirect URIs", which is generally
sensible.

### Limit the blast radius

The clients should be configured such that they only issue tokens for a specific *audience*. An audience can be,
for example, one or more microservices. A microservice must reject tokens that do not contain it as an audience.
This way, the token of a client can only be used to access the resources the client needs, and not also to access
other resources the user would additionally be authorized for.

See [Audience validation](../audience-restriction/audience-validation.md) for the configuration of the audience of a client.

## Troubleshooting with the event log

Keycloak logs all important events (e.g. successful or failed logins) in an event log, independently of the
technical logging. The event log of a realm can be viewed via the Keycloak web UI. To do this, event logging must
first be switched on under "Events/Config". In addition to the login events, admin events can also be stored, but
these are usually not relevant.

When the event log is switched on, the events can be viewed and searched under "Events/Login Events". Further
information can be found in the
[Keycloak documentation](https://www.keycloak.org/docs/latest/server_admin/#auditing-and-events).

## Keycloak from a local Docker image

Keycloak can be started locally using its [Docker image](https://hub.docker.com/r/keycloak/keycloak).

## Further documentation

- [Keycloak website](https://www.keycloak.org/)

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Minimizing access token sizes](../tokens/minimizing-access-token-sizes.md) — keep tokens issued by Keycloak lean.
- [Audience validation](../audience-restriction/audience-validation.md) — restrict the audience of a client's tokens.
- [Configuring audiences in Keycloak](../audience-restriction/audience-configuration-in-keycloak.md) — client scopes and audience mappers for resource audiences.
- [Authorizing Keycloak clients for consuming application resources](authorizing-keycloak-clients-for-consuming-applications-resources.md) — how consuming applications obtain Keycloak clients.
- [Tokens in the Blueprint Microservice](../tokens/tokens-in-the-blueprint-microservice.md) — the claims Keycloak puts into tokens.
- [Role concept in the Blueprint Microservice](../role-concept.md) — user roles and business partner roles.
- [OpenID Connect / OAuth2 mock server](../testing/oauth2-mock-server.md) — the local replacement for Keycloak on DEV.
