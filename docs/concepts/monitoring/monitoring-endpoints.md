# Monitoring Endpoints

> To integrate an application into the Prometheus / Grafana environment, the application, including the
> Prometheus password, must be registered in the Promregator configuration.

## Overview

For [technical monitoring](index.md), every microservice must provide an API. This should provide
information about the current state of the service. The following endpoints must be defined:

| Endpoint | Path | Description | Access |
| --- | --- | --- | --- |
| Index | `/actuator` | Overview of interfaces | Public |
| Health | `/actuator/health` | General state of the application. | Public, only basic information |
| Info | `/actuator/info` | General information about the application (name, version, etc., see also [Information](information.md)) | Public |
| Prometheus | `/actuator/prometheus` | (Technical) application metrics (see also [Metrics](metrics.md)) | Restricted to Prometheus via Basic-Auth |

The Prometheus endpoint uses the Prometheus format; all other endpoints must return JSON.

**Example: index endpoint response**

```js
{
   "_links":{
      "self":{
         "href":"https://jeap-microservice-examples-monitoring.app.cfap01.atlantica.admin.ch/actuator",
         "templated":false
      },
      "health":{
         "href":"https://jeap-microservice-examples-monitoring.app.cfap01.atlantica.admin.ch/actuator/health",
         "templated":false
      },
      "info":{
         "href":"https://jeap-microservice-examples-monitoring.app.cfap01.atlantica.admin.ch/actuator/info",
         "templated":false
      },
      "prometheus":{
         "href":"https://jeap-microservice-examples-monitoring.app.cfap01.atlantica.admin.ch/actuator/prometheus",
         "templated":false
      }
   }
}
```

**Example: health endpoint response**

```js
{
   "status":"UP"
}
```

**Example: info endpoint response**

```js
{
   "build":{
      "version":"0.0.1-SNAPSHOT",
      "artifact":"jeap-microservice-examples-monitoring",
      "name":"jeap-microservice-examples-monitoring",
      "group":"ch.admin.bit.jeap",
      "time":"2019-09-30T11:44:03.448Z"
   }
}
```

**Example: Prometheus endpoint response**

```
# HELP jvm_memory_used_bytes The amount of used memory
# TYPE jvm_memory_used_bytes gauge
jvm_memory_used_bytes{area="heap",id="Tenured Gen",} 2.9090168E7
jvm_memory_used_bytes{area="heap",id="Eden Space",} 1.4170312E7
jvm_memory_used_bytes{area="nonheap",id="Metaspace",} 5.2093288E7
jvm_memory_used_bytes{area="nonheap",id="Code Cache",} 2.6602304E7
jvm_memory_used_bytes{area="heap",id="Survivor Space",} 986800.0
jvm_memory_used_bytes{area="nonheap",id="Compressed Class Space",} 645851
...
```

## Integration

For Spring, **Spring Actuator** provides an implementation that can provide the health and info endpoints.
In addition, **micrometer-registry-prometheus** is a library that can collect the most important metrics and
provide the Prometheus endpoint. **Spring Security** can also secure the Prometheus endpoint with Basic-Auth.
These dependencies can most easily be pulled in with the Spring Boot Starter
**jeap-spring-boot-monitoring-starter**. This configures the endpoints, including Basic-Auth.

**Dependency for jeap-spring-boot-monitoring-starter**

```xml
<dependency>
    <groupId>ch.admin.bit.jeap</groupId>
    <artifactId>jeap-spring-boot-monitoring-starter</artifactId>
</dependency>
```

### Password

In addition, the password for the Prometheus endpoint (and optionally for the health endpoint) must be
defined. The username defaults to "prometheus" but can also be overridden with the property
`jeap.monitor.prometheus.user` (respectively "actuator" for `jeap.monitor.actuator.user`). As additional
protection, the password can e.g. be encrypted with bcrypt:

**Password for the Prometheus endpoint**

```yaml
jeap:
  monitor:
    prometheus:
      password: "{bcrypt}${vcap.services.prometheus.credentials.prometheusPwd}"
    actuator:
      password:"{bcrypt}${vcap.services.actuator.credentials.actuatorPwd}" 
```

The BCrypt password hash can be generated as follows:

```bash
$ sudo apt-get install apache2-utils
$ htpasswd -nBC 10 ""  | tr -d ':'
New password: 
Re-type new password: 
$2y$10$fNLaT95EZyYZeU2Xb5zR.Oes8U.ykPJXiQXj.q/a.WZ.FgeDLks/u
```

### Build Info

Finally, the build information must be stored at compile time so that it can be retrieved via the info
endpoint. This can be done with the **spring-boot-maven-plugin** in `pom.xml`:

**Generating build information in pom.xml**

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <executions>
                <execution>
                    <goals>
                        <goal>build-info</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

With Spring Actuator, further endpoints can also be defined (see the Spring Boot Actuator API
documentation). In addition, custom metrics for the Prometheus endpoint (see [Metrics](metrics.md)) and
additional info (e.g. feature flags) for the info endpoint (see [Information](information.md)) can also be
defined.

### Spring Security Configuration

The `jeap-spring-boot-monitoring-starter` comes with its own Spring Security configuration to protect the
Prometheus endpoint. This only applies to the path `/actuator/prometheus` and overrides other configurations
for that path. This can be overridden by setting the property `jeap.monitor.prometheus.secure` to `false` or
by activating the `disableprometheussecurity` profile.

## Example

An example of how the monitoring endpoints can be integrated is the `jme-prometheus-service` service in the
example [jme-monitor-example](https://github.com/jme-admin-ch/jme-monitor-example).

## Health Indicator for Kafka

`jeap-messaging` automatically registers a Spring Boot health indicator for each configured Kafka cluster.
This is active by default and is exposed under two endpoints:

- `/actuator/health/jeapKafka` – detailed status per cluster
- `/actuator/health` – integrated into the general application status

See also [Jeap Messaging Library](../messaging/jeap-messaging-library/index.md#health-indicators).

## Further documentation

- [Spring boot actuator: Production-ready features, Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready.html)
- [Micrometer Prometheus](https://micrometer.io/docs/registry/prometheus)
- [Spring und Micrometer, baeldung.com](https://www.baeldung.com/micrometer)
- [Custom Health Check in Spring Boot Actuator, amithp.com](https://www.amitph.com/custom-health-check-spring-boot-actuator/)
