# Defining Custom Metrics with Micrometer

## Overview

[Spring Boot](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.metrics)
and [jEAP](metrics.md) already define a number of mostly technical metrics themselves. For operating an
application, however, it is often useful to define additional, more business-oriented metrics. These
metrics can then, for example, also serve as a basis for alerting on detected problems.

## Integration

Spring Boot (and jEAP) use [Micrometer](https://micrometer.io/) to define metrics. Micrometer acts as a
facade abstracting over different common systems for generating and collecting metrics. jEAP configures
Micrometer in the
[jeap-spring-boot-monitoring-starter](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-monitoring-starter/pom.xml)
to work together with the monitoring system [Prometheus](https://prometheus.io/).

To activate this preconfiguration for a custom microservice, the following dependency must be added to the
microservice.

```xml
<dependency>
    <groupId>ch.admin.bit.jeap</groupId>
    <artifactId>jeap-spring-boot-monitoring-starter</artifactId>
</dependency>
```

## Micrometer

In Micrometer, so-called *Meters* can be defined and managed in a *Meter Registry*. Meters ultimately
produce metrics, which can e.g. be picked up via Prometheus and visualized in Grafana. The following code,
for example, defines a meter named `messages.sent` of type `Counter` in the Micrometer meter registry:

```java
@Autowired
MeterRegistry meterRegistry;
...
Counter messagesSentCounter = registry.counter("messages.sent");
```

For more detailed configuration of meters, their builders can be used:

```java
@Autowired
MeterRegistry meterRegistry;
...
Counter messagesSentCounter = Counter.builder("messages.sent")
			   	                         .description("Number of sent messages.")
				                         .register(meterRegistry);
```

### Meters

Among others, Micrometer supports the following types of meters:

- **Counter**: A counter is used to count events. It can only be incremented (by one or another positive
  number).
- **Gauge**: A gauge is used to record the current state value of something. A gauge can be incremented
  *and* decremented.
- **Timer**: A timer is used to measure the duration and frequency of events.
- **DistributionSummary**: Used to determine the distribution of events and can produce a histogram.

> Both Timer and DistributionSummary also count the observed events, i.e. it does not make sense here to
> additionally define a counter for the events.

> The value of a gauge must be bounded from above. For continuously growing values, a counter must be used.

### Dimensions / Tags

Metrics can be enriched with additional information in the form of key-value pairs (with key = tag/dimension):

```java
Counter messagesSentCounter = registry.counter("messages.sent",
                                               "type", "SayHelloMessage",
                                               "priority", "high");
```

For tags whose names or values must be created dynamically from the context, see
[Dimensions/Tags dynamically defined](#dimensionstags-dynamically-defined).

Dimensions/tags enable drill-downs into specific aspects during analysis. Suppose a validation service that
validates records of different types has a counter that counts the number of records validated so far. From
the number of validations, one could e.g. drill down to the number of records that failed validation, and if
needed further down to the number of records of a specific type that failed validation. In Prometheus, the
corresponding queries for a metric named `data.validations` with the dimensions `type` and `result` would
look something like this:

- `data_validations_total`
- `data_validations_total{result="invalid}`
- `data_validations_total{type="some_type",result="invalid"}`

> **Warning**: Every combination of a metric name and an observed tag value results in a separate timeline
> of measured values. Prometheus can only handle a limited number of timelines efficiently. It is therefore
> essential to ensure that the practical cardinality of dimensions/tags, as well as the number of
> dimensions/tags on a metric, is kept limited. This applies especially to metrics that are defined across
> all microservices of a business application, since the technical infrastructure will typically already
> add dimensions/tags to the metrics for the execution instance, environment, etc., which further multiplies
> the number of resulting timelines.

### Dimensions/Tags dynamically defined

Sometimes the dimensions of a metric can only be determined at runtime from the context. In this case, the
corresponding meters cannot be defined in advance in the meter registry, but must be created the first time
a combination of metric name and tag dimensions occurs. Micrometer, however, makes this very easy. Indeed,
registering a new meter in the meter registry checks whether the corresponding combination already exists,
and if so, does not create a new meter but returns the already registered meter. The observed event can then
be recorded on the returned meter, as in the example below with "increment()" on the counter.

```java
@Autowired
MeterRegistry meterRegistry;
...
public void validateData(...) {
    ...
    Counter.builder("data.validations")
            .tags("type", type, "result", result)
            .register(meterRegistry)
            .increment();
    ...
}
```

### Percentiles

Percentiles can optionally be defined on Timer and DistributionSummary metrics. If, for example, the
percentiles 0.5, 0.9 and 0.95 are defined on a metric, Micrometer adds the dimension `percentile` to the
metric with the value variants `0.5`, `0.9` and `0.95`. The corresponding timelines then reflect the value
below which 50%, 90% or 95% of the observed metric values lie, respectively.

```java
Timer.builder("some.timer").publishPercentiles(0.5, 0.9, 0.95).register(meterRegistry);
```

Spring Boot allows this configuration for a metric to also be made or changed via properties. This makes it
easy to externalize this configuration of a metric if needed.

```java
management.metrics.distribution.percentiles.some.timer="0.5,0.8,0.9"
```

> This configuration affects all metrics whose name begins with `some.timer`, i.e. it can, for example, also
> be used to define percentile configurations for an entire "namespace" of metrics at once.

> Through this mechanism, a metric that may be produced by a library without percentiles can also be
> configured to produce the desired percentiles.

Behind the above configuration via Spring Boot properties lies the more general
[Meter Filter](#meter-filters) mechanism of Micrometer, through which the metrics produced by an application
can be influenced programmatically. Besides percentiles,
[further](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.metrics.customizing.per-meter-properties)
properties of metrics can also be configured with Spring Boot configuration properties.

### Metric Names

Micrometer expects metric names (and tags) to be lowercase, with dots as separators for name parts.
Micrometer then automatically translates these names for the specific monitoring system in use according to
its naming conventions.

For example, if a timer named `http.server.requests` with the time unit seconds is defined in Micrometer,
Micrometer produces the metric `http_server_requests_duration_seconds` for Prometheus from it.

### Meter Filters

A meter registry can be configured with
[meter filters](https://micrometer.io/docs/concepts#_meter_filters). Through these,

- meters can be excluded
- meters can be transformed (e.g. renamed, tags added/removed, etc.)
- percentiles and histograms of meters can be configured

> Meter filters can be used to exclude or adjust predefined metrics from libraries when an excess of metrics
> threatens to overload the monitoring system.

> Meter filters can be used to apply cross-cutting configurations to custom (or third-party) meters, e.g. for
> the desired percentiles of Timer and DistributionSummary meters.

## Example

The jEAP example project [jme-monitor-example](https://github.com/jme-admin-ch/jme-monitor-example) gives an
example of different
[custom metric definitions](https://github.com/jme-admin-ch/jme-monitor-example/blob/main/jme-prometheus-service/src/main/java/ch/admin/bit/jeap/jme/prometheus/JobController.java)
in the service
[jme-prometheus-example](https://github.com/jme-admin-ch/jme-monitor-example/tree/main/jme-prometheus-service).
The comments in the code explain the defined metrics.

## Further documentation

- [Micrometer Concepts](https://micrometer.io/docs/concepts)
- [Spring Boot Custom Metrics](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.metrics.registering-custom)
