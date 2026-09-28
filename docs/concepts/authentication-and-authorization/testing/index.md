# Testing

It should be possible to develop and test a secured microservice independently of the authorization servers of the
actual environments, and without real users. There are several reasons for this:

- **Ease of use**: a developer can run and test the microservice locally right away, without access to a Keycloak
  server and without an account for every role the application distinguishes.
- **Isolation of what is tested**: the tests verify the authorization logic of the application, not the
  configuration of an authorization server. When a test fails, the cause lies in the application.
- **Independence from environments in CI/CD**: the pipeline needs neither network access to an environment nor
  credentials of real users or systems, and it does not depend on the state of a shared server. The tests are
  reproducible and can run anywhere.
- **Full control over the test data**: any combination of user, roles and business partners can be produced on
  demand, including cases no real account offers, such as a missing role or an expired token.
- **No real identities in tests**: no personal data and no production credentials end up in test code, test data or
  build logs.

jEAP supports this with two means, which this section describes: the OpenID Connect / OAuth2 mock server, which
replaces Keycloak for local development and in test environments and issues tokens for any configured user and role
set, and the test support of the jEAP Security Starter for writing unit and integration tests of secured REST APIs
without any authorization server at all.

**Start with** [OpenID Connect / OAuth2 mock server](oauth2-mock-server.md) to run a secured microservice locally.
Then read [Testing secured REST APIs](testing-secured-rest-apis.md) for automated tests.

## Contents

| Page | Description |
|---|---|
| [OpenID Connect / OAuth2 mock server](oauth2-mock-server.md) | The OAuth2 mock server for local development and test environments |
| [Testing secured REST APIs](testing-secured-rest-apis.md) | Unit and integration testing of secured REST APIs with the jEAP security test support |

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Protecting REST APIs](../protecting-rest-apis/index.md) — the REST APIs being tested.
- [Authorization servers](../authorization-servers/index.md) — Keycloak, which the mock server stands in for.
