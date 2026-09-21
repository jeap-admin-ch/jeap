# Spring Boot Admin and Spring Boot Actuators

## Overview

Spring Boot Admin is based on
[Spring Boot Actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-features.html).
The information that the Spring Boot Admin UI can display for a microservice is collected by accessing the
microservice's Actuator endpoints. The different Actuator endpoints of a Spring Boot application can be
individually enabled and protected. Correspondingly, the Spring Boot Admin UI can only display certain
information about a microservice if the microservice has enabled that endpoint and made it accessible.

The following table shows which Actuator endpoints provide the data for commonly used Spring Boot Admin UI
pages:

| Spring Boot Admin UI page | Actuator endpoint(s) |
| --- | --- |
| Details | info, health, metrics |
| Wallboard | info, health |
| Loggers | loggers |
| Logfile | logfile (only useful if actually logging to a file and not stdout - doesn't make sense for containerized apps) |
| Environment | env |
| Beans | beans |
| Configuration Properties | configprops |
| Scheduled Tasks | scheduledtasks |
| Metrics | metrics |
| Threads | threaddump |
| JMX | jolokia |

Depending on the libraries used by the microservice, further interesting Actuator endpoints may also become
relevant, e.g. the one for Flyway (flyway), etc.

Which Actuator endpoints may normally be enabled in which environment is summarized in the section
[Actuator/Environment Permission Matrix](#actuatorenvironment-permission-matrix).

## Security

When using Spring Boot Admin, users of the Spring Boot Admin UI gain access to various information of the
registered microservices via their Actuator endpoints. On one hand, this is metadata about the microservices
and their runtime environment; on the other hand, it may also include data managed by the microservice
itself, e.g. in a requested heap dump or log file. This data must be protected appropriately.

*In principle, the use and configuration of Spring Boot Admin must meet the demonstrated protection needs of
the affected microservices and their data, as well as the ICT baseline protection requirements, and this
must be documented (Schuban, ISDS, ...). This applies especially to systems with production data.*

The following gives requirements for configuring the Spring Boot Admin server and for configuring the
Actuator endpoints of monitored microservices. These requirements must, where necessary, be tightened for a
specific business application to meet its effective protection requirements.

## Spring Boot Admin Configuration

### HTTPS

Access to the Spring Boot Admin Server must be over HTTPS, both by users and by the microservices
registering with it. This is to protect the data from eavesdropping and tampering. To be ensured by teams
through configuration.

### Authenticated and authorized

Access to the Spring Boot Admin Server must be authenticated and authorized, both by users and by the
microservices registering with it. This is to ensure that only authorized users and microservices gain
access. To be ensured by teams through configuration with Spring Security in the Spring Boot Admin Server's
WebSecurity configuration.

In the simplest variant, authentication is done with Basic-Auth or form login, and all authenticated users
and microservices are automatically authorized for everything. This simplest variant is naturally not the
most secure variant. In principle, authentication via OAuth2 and Keycloak would also be possible.

## Microservice Actuator Configuration

The Spring Boot Admin Server obtains all information from the Spring Boot Actuator endpoints of the
registered microservices. Accordingly, the configuration of the Actuator endpoints is central. The following
requirements are therefore given.

### HTTPS

Access to the Actuator endpoints must be over HTTPS. This is to protect the data from eavesdropping and
tampering. To be ensured by teams through configuration.

### Read-only access

On the Acceptance and PROD environments, only read access to the Actuator endpoints may be allowed. From
Acceptance onward, a microservice's behavior should be defined only by its build and configuration, to
ensure reproducible behavior of microservice instances, and not by some setting that someone temporarily
changed on some instance at some point, somehow. Write access also carries the risk that attackers could
manipulate the system into doing things it should not do, whether by changing configurations or by
exploiting vulnerabilities in Actuators during data processing, e.g. when parsing XML data. Read-only access
is to be ensured via Spring Security in the microservice's WebSecurity configuration.

An exception to this rule is changing the log level. This should be allowed on development-adjacent
environments (cf. [Actuator/Environment Permission Matrix](#actuatorenvironment-permission-matrix)), so
developers can work efficiently. On Production and Acceptance, it should not be possible to change log
levels via Spring Boot Admin, since otherwise, for example, someone could turn off logging so that actions
they perform on an application are not logged, which could impair the traceability of those actions.

### Restrict access

Load balancers must be configured so that the Actuator endpoints can be accessed only by as small a circle
as possible, at most from the BV network, and certainly not from the internet.

### Enable/expose only when needed

Only those Actuator endpoints that are actually needed may be enabled and exposed. This reduces the risk
that data could unintentionally leak via Actuators, and that any existing security issues in Actuators could
be exploited. To be ensured via the Actuator configuration.

The following configuration enables the minimally required endpoints:

**Example: enabling and exposing the minimally necessary endpoints**

```java
management.endpoints.enabled-by-default=false
management.endpoint.info.enabled=true
management.endpoint.health.enabled=true
management.endpoint.prometheus.enabled=true
management.endpoints.web.exposure.include=*
management.endpoints.jmx.exposure.exclude=*
```

Depending on need (and protection requirements), additional endpoints can be enabled. Because of differing
protection requirements, enabling endpoints depends on the environment (cf.
[Actuator/Environment Permission Matrix](#actuatorenvironment-permission-matrix)).

### Authenticated, role-based access

Access to a microservice's Actuator endpoints must in principle only be possible if authenticated and
role-based. This is to ensure that only authorized users, according to their role, get access to the
functionality provided by the Actuators. To be ensured via the microservice's Spring Security WebSecurity
configuration.

In the simplest case, the Actuator endpoints are protected with a single role and Basic-Auth. Naturally, the
simplest case is not the most secure case. In principle, authentication via OAuth2 and Keycloak would also be
possible.

The following lists exceptions and clarifications to this rule.

### Simple health check largely public

The simple UP/Down status of the health Actuator should be "largely" publicly accessible. This is to
support meaningful automated health checks by interested parties. "Largely public" is to be understood as
at most the BV network, ideally a smaller circle.

### Detailed health check protected

The detailed status of the health Actuator may only be accessible, protected, to one role. This is meant to
prevent attackers from easily obtaining metadata that might be useful for an attack. To be ensured via the
Actuator configuration *and* the WebSecurity configuration (role). Ensured by the
`jeap-spring-boot-monitoring-starter`.

**health endpoint Actuator configuration**

```java
management.endpoint.health.show-details=when-authorized
management.endpoint.health.show-components=when-authorized
```

This configuration requires that access to the Actuator endpoints is authenticated and role-based.

### Info endpoint largely public

The info Actuator can be "largely" freely accessible. This is to support the analysis of installed
microservices, in particular the specific version of a microservice. "Largely free" is to be understood as
at most the BV network, ideally a smaller circle.

### Do not define sensitive custom info

The info Actuator must not be extended with custom info of a sensitive nature. Since the info endpoint is
largely freely accessible, sensitive data could otherwise leak. To be ensured by the teams.

### Prometheus endpoint with its own role

The prometheus endpoint must be protected with a separate role and Basic-Auth. This enables the operations
monitoring infrastructure to access the microservice's metrics. Ensured by the
`jeap-spring-boot-monitoring-starter`.

### Additional endpoints

Many Actuator endpoints have the potential to expose sensitive data or to help attackers gain access to
sensitive data. Enabling such endpoints on ABN (Acceptance) and PROD must be compatible with the demonstrated
protection needs of the system's data. To be ensured by the teams.

The following Actuators are non-exhaustive examples of Actuators that are interesting but carry certain
security risks: heapdump, jolokia, shutdown, httptrace, configprops, env, logfile, metrics, threaddump, etc.

### Custom endpoints

Self-defined custom Actuator endpoints must, in their implementation and configuration, be adapted to the
protection needs of the microservice's data.

## Actuator/Environment Permission Matrix

The following table summarizes, according to the Actuator endpoint configuration described above, how
access to the Actuator endpoints should be restricted on the different environments.

| Endpoint | Development | Reference | Acceptance | Production |
| --- | --- | --- | --- | --- |
| **info**¹ | public, read-only | public, read-only | public, read-only | public, read-only |
| **health**¹ | public, read-only | public, read-only | public, read-only (²) | public, read-only (²) |
| **prometheus**¹ | protected, read-only | protected, read-only | protected, read-only | protected, read-only |
| **loggers** | protected, read+write | protected, read+write | disabled | disabled |
| **xyz**³ | protected, read-only | protected, read-only | disabled | disabled |

(1) automatically configured by `jeap-spring-boot-monitoring-starter`

(2) only UP/Down status, no details, cf. [Detailed health check protected](#detailed-health-check-protected)

(3) additional Actuator endpoints are typically to be authorized this way (note:
[Additional endpoints](#additional-endpoints), [Custom endpoints](#custom-endpoints))

**Legend**

| Color | Meaning |
| --- | --- |
| green | public, read-only |
| yellow | protected, read-only |
| blue | protected, read and write |
| red | disabled |
