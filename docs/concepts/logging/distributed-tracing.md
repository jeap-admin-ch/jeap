# Distributed Tracing

## Overview

In a distributed system, correlating log entries that belong to a single request requires identifying that
request consistently across all the services that handle it. Distributed tracing achieves this with two
pieces of metadata that travel with each request:

- **Trace id:** generated when a request first enters the system or inherited from an upstream service that
  already generated one. Propagated unchanged on every outbound call to another service.
- **Span id:** generated per unit of work like an incoming HTTP request, an outbound HTTP call, or any
  explicitly instrumented block of code ([custom span](#custom-spans)). A span has a start and an end. A
  span belongs to a trace id, and a span can be started within another span; i.e. spans form a tree under
  the trace id.

Both ids are written into the Mapped Diagnostic Context (MDC) for the duration of the work, so every log
line emitted carries them. The same ids are exported to a tracing backend, where a trace shows up as a tree
of spans with timing, errors and tags. This gives two complementary ways to investigate a request: by
searching the central log store (e.g. Splunk) for the trace id, or by browsing the trace in the tracing
backend UI (e.g. Grafana).

## Instrumentation

[Spring Boot Observability](https://docs.spring.io/spring-boot/reference/actuator/observability.html) is
based on [Micrometer Observation](https://docs.micrometer.io/micrometer/reference/1.16/observation). With
the [OpenTelemetry](https://opentelemetry.io/docs/zero-code/java/spring-boot-starter/) support provided by
Spring Boot, observations can be turned into traces and spans and exported via OTLP to an
OpenTelemetry-compatible tracing backend. jEAP follows this Micrometer/OpenTelemetry approach and does not
use the [OpenTelemetry Java Agent](https://opentelemetry.io/docs/zero-code/java/agent/).

One consequence of this approach is that instrumentation is provided mainly through supported Spring
framework integration points, not through bytecode instrumentation of arbitrary libraries or all application
code. Therefore, applications should use the Spring-provided and auto-configured components for incoming and
outgoing communication whenever possible:

- use the Spring Boot auto-configured `RestClient.Builder` to create HTTP clients or use declarative
  `@HttpExchange` clients
- use the Spring-provided `KafkaTemplate` to send Kafka messages
- use Spring MVC controllers or handlers to process incoming HTTP requests
- use Spring Kafka listener containers, typically via `@KafkaListener`, to process Kafka messages

If code bypasses these Spring-managed components, for example by manually creating HTTP clients or Kafka
clients, automatic trace creation and context propagation may not work. In such cases, custom instrumentation
should be added using Micrometer's `ObservationRegistry`, `@Observed`, etc.

## Integration and Configuration

**See [How to: enable distributed tracing](../../how-tos/architecture-and-observability/enable-distributed-tracing.md)**
for adding the jEAP monitoring starter, declaring the service name, activating trace export and configuring
sampling.

## Custom Spans

Two ways to add custom spans are demonstrated in the example:

- **Tracer API:** inject the Micrometer `Tracer` bean and create a child of the current span around a block
  of code. Best when the span scope is a block (not a whole method), or when the span name or tags are
  dynamic, or when high-cardinality tags should be attached only to the span.
- **@Observed annotation:** instrument a whole method with a single annotation. Note that `@Observed`
  produces both a span for tracing *and* a Timer metric; use the `Tracer` API when the metric isn't wanted,
  or finer control is needed.

See `RestExample.span()` and `RestExample.observed()` in
[jme-tracing-service](https://github.com/jme-admin-ch/jme-monitor-example/tree/main/jme-tracing-service) and
its javadoc and comments for details.

## Trace ids in log lines for unhandled exceptions

If an exception escapes a `@Controller` annotation, the servlet container logs it after the tracing filter
has already cleared the MDC, so the log line ends up without a trace id. Catching and handling the exception
in a `@ControllerAdvice` processes the log statement while the request scope is still open and the trace id
is still in the MDC. So if you are missing the trace id on a log statement for an exception, make sure the
exception is handled by your code and does not bubble up to the servlet container.

If this is not an option, you can enable the `UnhandledExceptionLoggingFilter` provided by jEAP in the
`jeap-spring-boot-logging-starter` by adding the following configuration property to your service:

```yaml
jeap.logging.rest.unhandled-exception-logging.enabled: true
```

This will add a request filter to your filter chain that logs exceptions right before the traces in the MDC
context get removed from the MDC in the filter chain.

## Example

The [jme-monitor-example](https://github.com/jme-admin-ch/jme-monitor-example) contains the
[jme-tracing-service](https://github.com/jme-admin-ch/jme-monitor-example/tree/main/jme-tracing-service)
which demonstrates tracing with the `jeap-spring-boot-monitor-starter`. The example shows:

- How to integrate and configure the tracing using the `jeap-spring-boot-monitor-starter`.
- How to create a custom span around a code block and attach a tag to the span.
- How to create a custom span around a method execution.
- How to test tracing locally using a local otel-lgtm container.

Please consult the section *Tracing Example* in the project's
[readme](https://github.com/jme-admin-ch/jme-monitor-example/blob/main/README.md) and the documentation on
the example code for details.

## Related

- [How to: enable distributed tracing](../../how-tos/architecture-and-observability/enable-distributed-tracing.md) — add the monitoring starter and configure trace export and sampling.
