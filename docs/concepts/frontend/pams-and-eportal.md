# PAMS and ePortal integration

Applications integrated into ePortal need to coordinate navigation and session behavior with their
authentication setup. This page describes the responsibilities and deployment choices involved.
Concrete configuration properties and defaults belong to the component implementing each part.

## Integration responsibilities

| Component | Responsibility | Documentation |
| --- | --- | --- |
| Frontend service navigation | Display portal navigation and reflect portal session state. Applications using Oblique integrate its service-navigation component into their header. | The frontend component and application configuration. |
| Identity provider | Authenticate the user and participate in the configured login/logout flow. | [Keycloak](../authentication-and-authorization/authorization-servers/keycloak.md); when using PAMS as an identity provider, [jeap-keycloak-pams](https://github.com/jeap-admin-ch/jeap-keycloak-pams). |
| Backend API | Authenticate requests and enforce access to resources. | [REST API authentication and authorization](../authentication-and-authorization/protecting-rest-apis/rest-api-authentication-and-authorization.md). |

Configure these parts together: a frontend session indicator does not replace API authentication or
authorization. The backend still validates the credentials presented with each request.

## Environment alignment

The service navigation and the identity provider must use the same target environment. A mismatch
can leave the header's login state inconsistent or send logout and timeout redirects to the wrong
portal environment.

For each deployment, align the portal backend, identity-provider configuration and the application's
login/logout redirect destinations. Obtain the supported environment values and endpoint settings
from the components' configuration references.

## Deployments without portal integration

For an application that must also run outside ePortal, provide an explicit mode without portal
integration. In that mode, the frontend should:

- stop portal service-navigation requests and portal-specific session-timeout handling;
- hide or replace controls that require portal services, such as profile, messages and application navigation;
- provide login/logout behavior appropriate to its standalone authentication flow.

Configure authentication and API authorization for that deployment independently. Mocking the portal
session for development is a separate concern: a mocked session alone does not disable portal requests
or provide a standalone authentication flow.

The enabling switch, mock options and resulting header controls depend on the frontend implementation;
consult the application or component documentation for their precise behavior.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| The header shows a different login state from the application | Compare the portal environment, identity provider and active browser sessions. Inspect failed service-navigation requests in the browser. |
| Logout or session timeout redirects to an unexpected destination | Check the configured portal environment and allowed login/logout redirect destinations together. |
| The user is logged in, but an API returns 401 or 403 | Check the token sent to the API, its issuer and audience, and the roles required by the endpoint. A portal session indicator does not establish backend permissions. |
| A standalone deployment still contacts the portal | Check that the frontend's portal integration is disabled; a mock session setting alone is insufficient. |

Test login, logout and session expiry with the deployment's actual identity provider and portal
configuration. Check API access separately using the application's required roles.

## Related

- [Frontend](index.md)
- [Authentication and authorization](../authentication-and-authorization/index.md)
