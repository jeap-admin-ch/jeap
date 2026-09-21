# Information

## Overview

With the help of the info endpoint (see [Monitoring Endpoints](monitoring-endpoints.md)), information about
the current instance can be provided. In addition to the base information (application name, version,
etc.), further information can also be returned via the endpoint (e.g. feature flags).

## Integration

For information to be returned, the info endpoint must be activated (see
[Monitoring Endpoints](monitoring-endpoints.md)). There are two ways to return additional information: via
additional properties or via an `InfoContributor` (see examples).

## Example

The `jme-prometheus-service` service in the example
[jme-monitor-example](https://github.com/jme-admin-ch/jme-monitor-example) uses an `InfoContributor` and
additional information via properties.

**ExampleInfoContributor.java**
([source on GitHub](https://github.com/jme-admin-ch/jme-monitor-example/blob/main/jme-prometheus-service/src/main/java/ch/admin/bit/jeap/jme/prometheus/ExampleInfoContributor.java))

```java
package ch.admin.bit.jeap.jme.prometheus;

import org.springframework.boot.actuate.info.Info;
import org.springframework.boot.actuate.info.InfoContributor;
import org.springframework.stereotype.Component;

import java.util.Collections;

@Component
public class ExampleInfoContributor implements InfoContributor {
    @Override
    public void contribute(Info.Builder builder) {
        builder.withDetail("exampleWithChild", Collections.singletonMap("key1", "value1"));
        builder.withDetail("exampleWithoutChild", "value");
    }
}
```

**application.yml**
([source on GitHub](https://github.com/jme-admin-ch/jme-monitor-example/blob/main/jme-prometheus-service/src/main/resources/application.yml))

```yaml
spring:
  application:
    name: jme-prometheus-service
server:
  servlet:
    context-path: /jme-prometheus-service
# Configuring a static key value pair to be added to the info actuator output.
info:
  staticInfo: value
# Spring Boot supports configuring the percentiles of metrics externally, e.g. here for the metric "jobs.add".
# We could also configure the percentiles on the "jobs" level and have the configuration applied to all metrics having
# a name starting with "jobs", so we would not have to repeat the same percentiles configuration on every "jobs" metric.
management:
  metrics:
    distribution:
      percentiles:
        jobs:
          add: "0.5,0.8,0.9"
jeap:
  web:
    tls:
      enabled: false
  health:
    metric:
      contributor-metrics:
        enabled: true
```

The info endpoint can be reached at
[jme-prometheus-service/actuator/info](https://server/jme-prometheus-service/actuator/info).

**Example: info endpoint response**

```js
{
   "build":{
      "version":"0.0.1-SNAPSHOT",
      "artifact":"jeap-microservice-examples-monitoring",
      "name":"jeap-microservice-examples-monitoring",
      "group":"ch.admin.bit.jeap",
      "time":"2019-10-01T06:27:18.456Z"
   },
   "staticInfo":"value",
   "exampleWithChild":{
      "key1":"value1"
   },
   "exampleWithoutChild":"value"
}
```

## Further documentation

- [Custom Information in Spring Boot Info Endpoint, baeldung.com](https://www.baeldung.com/spring-boot-info-actuator-custom)
- [Application Information, Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-endpoints.html#production-ready-application-info)
