# Java SDK and Versions

## Overview

The microservices blueprint uses Java with Spring Boot to build backends. This page
defines the most important libraries used for that.

## Java

Since Java 9, a new Java feature release has been published every six months.
Since Java 17, LTS releases have followed a two-year cadence. Support lifetimes
and security-update periods depend on the JDK distribution and vendor, so applications
should either track feature releases every six months or select an LTS distribution
whose vendor support window meets their requirements.

### Java Styleguide

jEAP does not define custom code style guidelines; the Oracle/Sun code conventions apply, see
[https://www.oracle.com/java/technologies/javase/codeconventions-contents.html](https://www.oracle.com/java/technologies/javase/codeconventions-contents.html).
These conventions are also applied by default by IntelliJ's formatter.

## Java 25

Java 25 is the latest LTS version of Java. The jEAP Spring Boot starters, the jEAP
pipelines on all supported CI servers, and the Java runtime images provided on the
platforms already support Java 25.

### Automated Migration Using the jEAP CLI

The jEAP CLI automates the Java 25 migration across the jEAP ecosystem. See
[https://github.com/jeap-admin-ch/jeap-cli](https://github.com/jeap-admin-ch/jeap-cli)
for installation instructions.

After installation, the Java 25 migration can be started as follows in a locally
checked-out repository:

```bash
jeap migrate java-25
```

### Known Migration Issues in Projects

| # | Description | Solution |
| - | ----------- | ------- |
| 1 | Annotation processors such as Lombok are no longer run automatically | The jEAP parent now sets `proc:full` as a parameter for the Maven Compiler Plugin, so annotation processors on the classpath continue to run automatically unless a project defines them explicitly. If a project overrides the compiler configuration from the parent, make sure `proc:full` is also set in that project's `maven-compiler-plugin` configuration. |

### Optional: `.sdkmanrc` in Projects

A project can create a file named `.sdkmanrc` in the project root using
`sdk env init`, which specifies the Java version for the project. IntelliJ recognizes
this file and automatically switches the project SDK to that version.

### Maven

`jeap-spring-boot-parent` supports Java 25 starting with version `29.2.0`.

Set the following property in `pom.xml`:

```xml
<properties>
  <java.version>25</java.version>
  <maven.compiler.release>25</maven.compiler.release>
</properties>
```

## Spring, Spring Boot and Spring Cloud

We use Spring Boot to build microservices. Spring Boot does not follow Long-Term or
Short-Term Support release cycles. For this reason, the latest Spring Boot version
should always be used — see the [jEAP version overview](../jeap-version-overview.md).
Each Spring Boot version defines a compatible Spring Framework and Spring Cloud
version; the matching Spring versions must always be used.

If possible, libraries from the Spring ecosystem should be used, since Spring ensures
their compatibility. To use compatible versions, Spring Boot uses a so-called
**Bill of Materials** (BOM) — a Maven feature for defining the versions of transitive
and direct dependencies in separate POM files. Wherever possible, versions should be
taken from the Spring Boot BOMs instead of defining custom versions in project POMs.

## Integration

With `jeap-spring-boot-parent`, a starter is available that already defines the
necessary dependencies and versions:

- Defines the current Java version
- Defines the versions of the most important dependencies (Spring, Spring Boot,
  Spring Cloud, Lombok, jEAP starters, jEAP libraries)
- Dependency on the most important jEAP starters (logging and monitoring)
- Dependency on `spring-boot-starter-test` including JUnit 5. The Vintage engine is
  excluded.
- Spring Boot Maven Plugin including build information.

This project can be used as a parent for your own projects (see the
[jEAP version overview](../jeap-version-overview.md)):

```xml
<parent>
    <groupId>ch.admin.bit.jeap</groupId>
    <artifactId>jeap-spring-boot-parent</artifactId>
    <version>USE-LATEST-VERSION</version>
</parent>
```

## Further Reading

- [Spring Boot documentation, including the current version](https://spring.io/projects/spring-boot#learn)
- [Spring Boot managed dependency versions](https://docs.spring.io/spring-boot/docs/current/reference/html/appendix-dependency-versions.html#appendix-dependency-versions)
- [Introduction to JUnit 5](https://junit.org/junit5/)
- [What's new in JUnit 5](https://blog.codecentric.de/2017/10/junit5-junit-5/)
- [Spring Cloud documentation](https://spring.io/projects/spring-cloud)
