---
title: Why jEAP?
description: Why developers and architects choose jEAP — the reusable, cross-functional aspects of an enterprise application are already solved, tested and maintained.
sidebar_position: 1
---

# Why jEAP?

jEAP solves the recurring cross-functional concerns of enterprise applications —
messaging, security, persistence, observability, encryption, and more — once and in a
reusable way, so that application teams can focus on their business logic. Teams compose
their service from [building blocks](/docs/building-blocks) and inherit a curated,
version-aligned dependency tree instead of assembling and maintaining the plumbing
themselves.

jEAP follows a principle of **standardization without restriction**: rather than hiding
Spring Boot behind its own abstraction, it complements it — teams keep the full power of
the underlying framework while gaining aligned defaults for the mandatory and technically
demanding non-functional requirements. It builds on established open-source solutions and
adds building blocks only where they are missing.

The value extends well beyond initial development, where most of an application's effort
is actually spent:

- **Faster, safer delivery.** Opinionated CI/CD, automated regression testing and
  [feature-flag-based releases](/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-featureflag-starter)
  shorten the path from commit to production.
- **AI-ready development.** The
  [jEAP MCP server](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-mcp-service/usage)
  gives AI coding assistants access to jEAP documentation, source-code examples and
  current platform versions, grounding their answers and generated code in actual
  jEAP components and conventions rather than potentially outdated model knowledge.
- **Secure and compliant by default.**
  [OAuth2/OIDC resource-server security](/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-starter)
  validates access tokens and supports role-based authorization, while
  [zero-trust messaging](/docs/building-blocks/libraries/jeap-messaging) and
  [data-at-rest encryption](/docs/building-blocks/libraries/jeap-crypto) help protect
  communication and stored data.
- **Self-documenting applications.**
  [OpenAPI specs](/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-swagger-starter),
  message and consumer contracts,
  [DB schemas](/docs/building-blocks/libraries/jeap-db-schema-publisher) and deployments
  are published automatically to the architecture repository.
- **Automates Governance.**
  [jEAP governance service](/docs/building-blocks/libraries/jeap-governance) automatically checks for compliance with predefined rules.
- **Cloud portability.** Business logic stays platform-agnostic, providing a proven
  cloud-exit strategy and low-effort migration between cloud and on-premises platforms.
- **Developer mobility.** Shared conventions and tooling let developers move between teams;
  jEAP is used by different organizations across several Swiss federal administrations.

## Next steps

- [What is jEAP?](what-is-jeap.md) — read the platform overview and core principles.
- [Using jEAP](using-jeap/index.md) — learn about the parent POMs and dependency management.
- [App Building Blocks](building-blocks/index.md) — explore the libraries, starters and microservices.
