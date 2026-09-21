# Logging

## Overview

Logging refers to the automatic creation of a record (*log*) of software processes. Logging serves to record
and trace error conditions. Logging is to be distinguished from
[monitoring](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-monitoring-starter) (monitoring the status of a service)
and business logging (logging of business events).

In a microservice application, each service generates its own log. Creating such a log is described in more
detail under [Application Logs](application-logs.md). However, since a single process often triggers actions
on different systems, error analysis using individual log files alone is very cumbersome. To be able to
analyze and search all logs in a central location, a central logging infrastructure and
[Distributed Tracing](distributed-tracing.md) are needed.

## Logging on AWS

See [AWS Logging](aws-logging.md).

## Topics

- [Application Logs](application-logs.md)
- [AWS Logging](aws-logging.md)
- [Request Tracing](request-tracing.md)
- [Distributed Tracing](distributed-tracing.md)
