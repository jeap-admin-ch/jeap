# Metrics

## Overview

With the help of the Prometheus endpoint (see [Monitoring Endpoints](monitoring-endpoints.md)), metrics of
the current instance can be returned. In addition to the base information (CPU, memory, etc.), custom
metrics can also be returned via the endpoint.

## Integration

Custom metrics can be added using the **MeterRegistry** (see example).

## jEAP Metrics

The `jeap-spring-boot-monitoring-starter` defines special metrics that are enabled for all jEAP applications.
All of these metrics are displayed in Prometheus.

### Dependency

To be able to check dependencies and their versions centrally, they are also made available in Prometheus.
At microservice startup, all dependencies are listed (class `DependencyMetricsInitializer`) and displayed in
Prometheus as **jeap_dependency_version** like this:

```
# HELP jeap_dependency_version Dependency Versions
# TYPE jeap_dependency_version gauge
jeap_dependency_version{name="spring.security.oauth2.resource.server",version="5.3.3.RELEASE",} 1.0
jeap_dependency_version{name="java.persistence",version="2.2.3",} 1.0
jeap_dependency_version{name="spring.security.oauth2.core",version="5.3.3.RELEASE",} 1.0
jeap_dependency_version{name="spring.security.oauth2.client",version="5.3.3.RELEASE",} 1.0
jeap_dependency_version{name="spring.security.config",version="5.3.3.RELEASE",} 1.0
...
```

### Health

Health is also provided as code (**health**) in Prometheus (class `HealthMetricsConfig`).

Using the property `jeap.health.metric.update-rate-seconds`, the rate at which the metric's value is updated
can be adjusted; the default is 120 seconds. The metric reflects the value of the Spring Boot health
endpoint. If `jeap.health.metric.update-rate-seconds` = -1 is set, updating of the metric is disabled.

```
# HELP health
# TYPE health gauge
health 1.0
```

Using the property `jeap.health.metric.contributor-metrics.enabled`, it can be controlled whether the
individual health contributors are exported as separate Prometheus metrics under `health_indicator_status`.
If the property is set to `true`, the status values of the individual components are output as their own
metrics. With `false`, these detail metrics are not output. The default value is `false`. Example with
contributor metrics enabled:

```
# HELP health_indicator_status  
# TYPE health_indicator_status gauge
health_indicator_status{component="diskSpace"} 1.0
health_indicator_status{component="livenessState"} 1.0
health_indicator_status{component="db"} 1.0
health_indicator_status{component="ping"} 1.0
health_indicator_status{component="readinessState"} 1.0
health_indicator_status{component="refreshScope"} 1.0
health_indicator_status{component="ssl"} 1.0
```

### App Name

The app name is exposed as a metric to correlate the CF app name with the Spring Boot app name:

```
jeap_spring_app{name="my-app"}
```

### Rest-Tracing

The goal of Rest-Tracing is to document the relations between microservices. The class `RestTracingMetrics`
increments a counter for every incoming REST request.

These counters are uniquely defined per consumer, datapoint, technology and method, and are displayed in
Prometheus as **jeap_relation_total** like this:

```
# HELP jeap_relation_total 
# TYPE jeap_relation_total counter
jeap_relation_total{consumer="jme-tracing-service",datapoint="/document/{id}/content/{type}",method="GET",technology="http",} 6.0
jeap_relation_total{consumer="jme-tracing-service",datapoint="/document/{id}",method="GET",technology="http",} 6.0
jeap_relation_total{consumer="jme-tracing-service",datapoint="/document/{id}/content/{type}",method="POST",technology="http",} 6.0
jeap_relation_total{consumer="jme-tracing-service",datapoint="/callback4",method="GET",technology="http",} 1.0
...
```

To limit the number of counters, the maximum can be configured (default is 2000):

```
jeap.monitor.metrics.rest.maximum-allowable-jeap-relation-metrics=2000
```

### Messaging-Tracing

The goal of Messaging-Tracing is to document the messages exchanged between microservices. The class
`KafkaMeterRegistryMetrics` of the `jeap-messaging` library increments a counter for every incoming and
outgoing message (event or command).

These counters are uniquely defined per application, message, topic and type (producer or consumer), and are
displayed in Prometheus as **jeap_messaging_total** like this:

```
# HELP jeap_messaging_total
# TYPE jeap_messaging_totalcounter
jeap_messaging_total{application="jme-messaging-sender-service",message="JmeCreateDeclarationCommand",topic="jme-messaging-create-declaration",type="producer",bootstrapservers="bootstrap.server.kafka.admin.ch:9092"} 47.0
jeap_messaging_total{application="jme-messaging-sender-service",message="JmeDeclarationDeletedEvent",topic="jme-messaging-declaration-deleted",type="consumer",bootstrapservers="bootstrap.server.kafka.admin.ch:9092"} 47.0
...
```

## Example

The `jme-prometheus-service` service in the example
[jme-monitor-example](https://github.com/jme-admin-ch/jme-monitor-example) uses custom metrics. See
[Defining Custom Metrics with Micrometer](custom-metrics-with-micrometer.md) for details on custom metrics.

**JobController.java**
([source on GitHub](https://github.com/jme-admin-ch/jme-monitor-example/blob/main/jme-prometheus-service/src/main/java/ch/admin/bit/jeap/jme/prometheus/JobController.java))

```java
package ch.admin.bit.jeap.jme.prometheus;

import io.micrometer.core.annotation.Timed;
import io.micrometer.core.instrument.*;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Collection;
import java.util.Map;
import java.util.Random;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;

@RestController
@RequestMapping(path = "/api/jobs")
public class JobController {

    private final Map<String, Job> jobs = new ConcurrentHashMap<>();
    private final Random random = new Random();

    private final MeterRegistry meterRegistry;
    private final Counter jobValidationErrorCounter;
    @SuppressWarnings({"FieldCanBeLocal", "unused"})
    private final Gauge  availableJobsGauge; // keep a hard reference to the gauge in order to protect it from being garbage collected
    private final DistributionSummary jobDescriptionSizeSummary;
    private final Timer jobListTimer;

    public JobController(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        // Counters are used to count events and can only be incremented.
        jobValidationErrorCounter = Counter.builder("jobs.validation.error")
                .description("Number of invalid jobs received.")
                .register(meterRegistry);
        // Gauges are used to record the current value of something.
        availableJobsGauge = Gauge.builder("jobs.available", jobs, Map::size)
                .description("Number of jobs available.")
                .register(meterRegistry);
        // Distribution summaries are used to track the distribution of events and can be used to create histograms.
        jobDescriptionSizeSummary = DistributionSummary
                .builder("jobs.description.size")
                .description("Job description sizes")
                .baseUnit("characters")
                .publishPercentiles(0.5, 0.9, 0.95)
                .register(meterRegistry);
        // Timers are used to record the duration and frequency of events.
        jobListTimer = Timer
                .builder("jobs.list")
                .description("Timing job listings")
                .publishPercentiles(0.5, 0.9, 0.95)
                .register(meterRegistry);
    }

    @GetMapping
    public Collection<Job> listJobs() {
        // programmatically timing a method call
        return jobListTimer.record( () -> {
            simulateWork(); // let some time pass
            return jobs.values();
        });
    }

    // Convenient micrometer defined annotation for timing methods. The annotation also supports configuring percentiles,
    // but in this case, for demonstration purposes we configure the percentiles with a property in the application.yml.
    @Timed(value = "jobs.add", description = "Timing job additions")
    @PutMapping
    public ResponseEntity<Void> addJob(Job job) {
        if (job.checkValid()) {
            simulateWork(); // let some time pass
            jobs.put(job.getId(), job);
            jobDescriptionSizeSummary.record(job.getDescription().length());
            return new ResponseEntity<>(HttpStatus.OK);
        } else {
            jobValidationErrorCounter.increment();
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        }
    }

    @DeleteMapping("/{id}")
    public void removeJob(@PathVariable String id) {
        Job job = jobs.remove(id);
        // Record a metric with a tag/dimension that depends on the local execution context.
        // Note: if a meter with the given name already exists in the registry, 'register' will use it and not create a new one.
        // Attention: Mind the cardinality of a tag as a separate timeline will be created for every tag value and if you are
        // adding multiple tags then for every combination of the tags' values.
        Counter.builder("jobs.remove")
                .description("Number of jobs removed.")
                .tag("priority", job.getPriority().name()) // count the jobs separately by priority
                .register(meterRegistry)
                .increment();
    }

    private void simulateWork() {
        try {
            TimeUnit.SECONDS.sleep(Math.round(2.5 * random.nextDouble()));
        } catch (InterruptedException ie) {
            Thread.currentThread().interrupt();
        }
    }

}
```

The Prometheus endpoint can be reached at
[jme-prometheus-service/actuator/prometheus](https://server/jme-prometheus-service/actuator/prometheus)
(username: prometheus, password: thisisverysecret).

## Further documentation

- [Metrics with Spring, Anleitung IBM Cloud](https://cloud.ibm.com/docs/java?topic=java-spring-metrics)
- [Metrics, Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-metrics.html)
- [Micrometer Concepts, Micrometer Documentation](https://micrometer.io/docs/concepts)
