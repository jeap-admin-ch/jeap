# How-Tos: Platform & Tooling

Parent POMs, Spring Boot starters, the jEAP CLI, and build/release tooling.

- [Use the jEAP Spring Boot parent](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-parent/getting-started) — add it as parent, use managed dependencies and plugins without versions.
  - [Select or override the default Pact broker URL](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-internal-spring-boot-parent/pact-broker) for Maven projects using the internal parent.
- [Wire up a new jEAP service with the core starters](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/getting-started) (security, monitoring, logging).
- [Import AppConfig configuration and Secrets Manager secrets](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-config-aws-starter/getting-started) via the AWS config starter.
- [Generate environment-specific truststores](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-truststore-maven-plugin/getting-started) from a certificate repository, including offline builds.
- [Build the jEAP CLI from source](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-cli/building) — Hotspot JAR or native GraalVM binary.
- Keep frontend licenses in order ([jeap-frontend-license-checker](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-frontend-license-checker/getting-started)) — install, wire up scripts, run it, declare exceptions.
  - [Migrate from the legacy license checker](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-frontend-license-checker/migration).
  - [Set up npm trusted publishing](https://jeap-admin-ch.github.io/docs/building-blocks/tooling/jeap-frontend-license-checker/npm-publishing-setup) for this package (one-time maintainer setup).
- [Set up npm trusted publishing for jeap-jwe-client](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-jwe-client/npm-publishing-setup) (one-time maintainer setup).
- [Add a custom project contributor to jeap-initializer](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-initializer/extending) — including via auto-configuration for packages outside component scanning.
- [Use feature flags](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-featureflag-starter) — add the Togglz-based starter, define and check flags, write a custom activation strategy.
