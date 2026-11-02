# How-Tos: Security

Authentication, tokens, roles, TLS, encryption, signing, and testing security.

## Audiences

- [Configure Keycloak scopes/mappers for a resource audience](../../concepts/authentication-and-authorization/audience-restriction/audience-configuration-in-keycloak.md) — add an audience to an existing resource's access tokens on Keycloak, for a calling client that already exists.
- [Create a Keycloak introspection client for a resource](configure-keycloak-introspection-client.md) — the dedicated-client pattern Keycloak 26.6.2+ requires for its introspection audience check.
- [Migrate existing resource access to audience validation](migrate-to-audience-restriction.md) — the full rollout for an existing system: introspection compatibility, strict enforcement, or both.

## Tokens

- [Enable and debug jEAP token introspection](enable-and-debug-token-introspection.md) — pick an introspection mode, configure Keycloak and the resource server, and debug a user's authorizations when they're fetched by introspection.

## Encryption & signing

- [Sign and verify messages without jEAP](../../concepts/messaging/jeap-messaging-library/signing-messages-and-checking-signatures-without-jeap.md) — implement jEAP's message-signing protocol yourself, for a publisher or subscriber that cannot use the jEAP Messaging library.
- Encrypt data with jEAP-Crypto ([jeap-crypto](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-crypto/getting-started)) — encrypt/decrypt arbitrary data with a KMS-backed `CryptoService`.
  - [Encrypt a JPA entity column](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-crypto/database-columns) transparently with `JeapCryptoStringConverter`.
  - [Encrypt/decrypt S3 objects](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-crypto/s3-object-storage) with `JeapCryptoS3Template`.
  - [Encrypt a Kafka message type](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/encrypting-messages) via jeap-messaging's integration with jeap-crypto.

## TLS, mTLS & IAM

- Add TLS to a service ([jeap-spring-boot-tls-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-tls-starter/getting-started)) — add the starter and tune the self-signed certificate.
  - [Expose actuator endpoints over plain HTTP on a separate port](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-tls-starter/actuator-endpoints) when the main port requires mutual TLS.
- [Authenticate to AWS with IAM Roles Anywhere](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-roles-anywhere-starter/getting-started) — add the starter, configure ARNs/certificate/key, use the credentials provider.
- [Test JWE-protected endpoints without a real Vault instance](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-jwe-starter/testing) — static test mode and test keys for `jeap-spring-boot-jwe-starter`.

## Mock authorization server for dev/test

- Run the OAuth2 mock server for local dev and tests ([jeap-oauth-mock-server](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-oauth-mock-server/getting-started)) — create an instance, configure clients/users, reach the login form.
  - [Add custom token claims](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-oauth-mock-server/custom-token-claims) via a token customizer bean.
  - [Point an Angular/Spring client or resource server at the mock server](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-oauth-mock-server/client-integration-examples).
  - [Upgrade the underlying Spring Security Authorization Server version](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-oauth-mock-server/upgrading) safely.
