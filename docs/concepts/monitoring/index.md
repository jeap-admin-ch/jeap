# Monitoring

## Overview

Technical monitoring observes the availability, performance and general state of technical (executable)
components. Their state can generally be measured directly. Comparing the measured values with "normal"
values can, under some circumstances, enable early detection of problems; it can also help to understand the
behavior of an application and fix problems. Technical monitoring is to be distinguished from business
monitoring and from [Logging](../logging/index.md).

In a microservice application, each service generates metrics about its technical state (e.g. memory usage
and availability, CPU load). Creating these metrics is described under [Metrics](metrics.md). For these
metrics to be monitored by an external system, an interface is required (see
[Monitoring Endpoints](monitoring-endpoints.md)).

## Further documentation

- [Promregator](https://github.com/promregator/promregator)
- [Prometheus](https://prometheus.io/)

## Topics

- [Monitoring Endpoints](monitoring-endpoints.md)
- [Metrics](metrics.md)
- [Defining Custom Metrics with Micrometer](custom-metrics-with-micrometer.md)
- [Information](information.md)
- [Grafana](grafana.md)
- [Spring Boot Admin](spring-boot-admin.md)
  - [Spring Boot Admin and Spring Boot Actuators](spring-boot-admin-actuators.md)
