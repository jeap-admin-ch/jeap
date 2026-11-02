# How-Tos: Security

Authentication, tokens, roles, TLS, encryption, signing, and testing security.

- [Configure Keycloak scopes/mappers for a resource audience](../../concepts/authentication-and-authorization/audience-restriction/audience-configuration-in-keycloak.md) — add an audience to an existing resource's access tokens on Keycloak, for a calling client that already exists.
- [Sign and verify messages without jEAP](../../concepts/messaging/jeap-messaging-library/signing-messages-and-checking-signatures-without-jeap.md) — implement jEAP's message-signing protocol yourself, for a publisher or subscriber that cannot use the jEAP Messaging library.
- Encrypt data with jEAP-Crypto ([jeap-crypto](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-crypto/getting-started)) — encrypt/decrypt arbitrary data with a KMS-backed `CryptoService`.
  - [Encrypt a JPA entity column](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-crypto/database-columns) transparently with `JeapCryptoStringConverter`.
  - [Encrypt/decrypt S3 objects](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-crypto/s3-object-storage) with `JeapCryptoS3Template`.
  - [Encrypt a Kafka message type](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-messaging/encrypting-messages) via jeap-messaging's integration with jeap-crypto.
- Add TLS to a service ([jeap-spring-boot-tls-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-tls-starter/getting-started)) — add the starter and tune the self-signed certificate.
  - [Expose actuator endpoints over plain HTTP on a separate port](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-tls-starter/actuator-endpoints) when the main port requires mutual TLS.
- [Authenticate to AWS with IAM Roles Anywhere](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-roles-anywhere-starter/getting-started) — add the starter, configure ARNs/certificate/key, use the credentials provider.
- [Test JWE-protected endpoints without a real Vault instance](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-jwe-starter/testing) — static test mode and test keys for `jeap-spring-boot-jwe-starter`.
- Run the OAuth2 mock server for local dev and tests ([jeap-oauth-mock-server](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-oauth-mock-server/getting-started)) — create an instance, configure clients/users, reach the login form.
  - [Add custom token claims](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-oauth-mock-server/custom-token-claims) via a token customizer bean.
  - [Point an Angular/Spring client or resource server at the mock server](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-oauth-mock-server/client-integration-examples).
  - [Upgrade the underlying Spring Security Authorization Server version](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-oauth-mock-server/upgrading) safely.

## Known gaps — no how-to exists yet

See [`doc-refactoring-plan.md`](https://github.com/jeap-admin-ch/jeap/blob/main/doc-refactoring-plan.md)
for the full list and status. Notably missing: an end-to-end "secure a brand-new microservice with
jEAP Security" guide, an "add audience restriction to a brand-new service" quick-start, and key/cert
rotation how-tos for jeap-crypto, message signing, IAM Roles Anywhere, and the JWE Vault transit key.
