# jEAP and Maven Dependencies FAQ

Common questions about jEAP versions and how Maven dependency management works in a
jEAP application. For the underlying model — the parent hierarchy and BOM-style
dependency management — see [Using jEAP](using-jeap.md).

## How do I find out the latest jEAP versions?

The [jEAP version overview](jeap-version-overview.md) lists the current versions of:

- the jEAP parent
- the jEAP libraries
- the jEAP products (reusable microservices)

It also lists the managed versions of Spring and selected third-party libraries
(Flyway, the AWS SDK, and others).

## How can I find out about the latest releases?

Two options:

- Check the [jEAP version overview](jeap-version-overview.md) regularly.
- Subscribe to the [jEAP blog](https://jeap-admin-ch.github.io/blog) — you also get the
  rest of the platform news.

## How are jEAP dependencies structured?

[Using jEAP](using-jeap.md) explains the two-level Maven parent chain and the
dependency-management model.

## How does my project benefit from this structure?

Inheriting from `jeap-spring-boot-parent` gives you:

- simple project `pom.xml` files
- out-of-the-box dependency management for jEAP and third-party libraries, including a
  fast path for security fixes coming from Spring and other libraries
- pre-configured common Maven plugins (Surefire, JaCoCo, Pact, Spring Boot, …)
- Pact configuration
- Maven profiles and repository configuration
- support from the jEAP team

## Should I mirror this parent structure in my own project?

**Short answer:** no, with few exceptions.

**Long answer:** only a handful of projects need such a layered parent structure. The
jEAP libraries and configuration are meant to be consumed by many teams and projects,
so they have to be flexible, consistent and developer-friendly. That flexibility has a
cost: actions that are trivial in a single project take more effort across this
structure.

For example, bumping one third-party library version (say a Togglz bug that affects the
Process Context Service) means:

1. releasing `jeap-internal-spring-boot-parent`
2. releasing `jeap-spring-boot-starters` against the new `jeap-internal-spring-boot-parent`
3. releasing `jeap-spring-boot-parent` against 1. and 2.
4. releasing the Process Context Service against 3.

Recommendations:

- Start simple; add structure only when a concrete need appears.
- Share libraries within a feature team only if actually required.
- Be cautious with shared parent POMs.

## Do you provide tooling to upgrade jEAP dependencies automatically?

No. Use a general-purpose dependency-update tool such as
[Renovate](https://docs.renovatebot.com/) or
[Dependabot](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/dependabot-quickstart).

## How should I manage dependency versions?

- **Do not** declare versions for libraries that are already managed by jEAP or Spring
  Boot — let the parent align them.
- For the versions you do manage, extract them to `<properties>` in your top-level
  `pom.xml` for a single overview.

## Why does dependency X with version Y end up in my project?

Print the resolved dependency tree:

```shell
mvn dependency:tree
```

IntelliJ IDEA offers the same information graphically: open a `pom.xml` and use
**Show Diagram…**, or install the **Maven Helper** plugin, which adds a dependency-tree
tab to the `pom.xml` editor.

## General recommendation for services built on a reusable microservice

Each reusable microservice (Error Handling Service, Process Context Service, Process
Archive Service, …) is published with its own `<service>-instance` Maven parent (for
example `jeap-error-handling-service-instance`). Use that instance parent for your
service instance: it brings in a compatible `jeap-spring-boot-parent` and manages the
required dependency versions for you, so you no longer have to track the matching jEAP
parent version by hand. See the getting-started guide of the respective
[reusable microservice](building-blocks/reusable-microservices/index.md).

## See also

- [Using jEAP](using-jeap.md) — the Maven parents and the dependency-management model.
- [jEAP version overview](jeap-version-overview.md) — current versions of the parent,
  libraries and products.
- [App Building Blocks](building-blocks/index.md) — the libraries, starters and
  microservices you compose from.
