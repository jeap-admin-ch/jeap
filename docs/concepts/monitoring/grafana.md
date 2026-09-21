# Grafana

## Overview

With Grafana, metrics collected by Prometheus can be displayed graphically. Grafana makes it possible to
query, visualize, alert on and understand metrics regardless of where they are stored. Dashboards can be
created and shared with a team.

## Integration

For Grafana to be used, a Prometheus infrastructure must be available. No further changes or configuration
are necessary.

## Example

Grafana can be tried out locally. If Prometheus was started as described under Prometheus, Grafana can be
started locally as follows:

**Starting Grafana locally**

```bash
sudo docker run --detach --name=grafana --rm --link=prometheus --publish=3000:3000 grafana/grafana
```

Grafana can now be reached at `localhost:3000`. The username and password are `admin`. First, a data source
of type Prometheus with the URL `http://prometheus:9090` must be added. After that, dashboards can be
created with the metrics. If, for example, `process_cpu_usage` is searched for, the CPU load of all systems
is displayed.

## PromQL

The query language of Prometheus, used in Grafana's dashboard queries, offers many ways to analyze, filter
and aggregate metric time series. Here is a starting point to learn the basics of PromQL:

- [https://prometheus.io/docs/prometheus/latest/querying/basics/](https://prometheus.io/docs/prometheus/latest/querying/basics/)

## Further documentation

- [Build A Monitoring Dashboard by Prometheus + Grafana, medium.com](https://medium.com/htc-research-engineering-blog/build-a-monitoring-dashboard-by-prometheus-grafana-741a7d949ec2)
- [grafana.com](https://grafana.com/)
