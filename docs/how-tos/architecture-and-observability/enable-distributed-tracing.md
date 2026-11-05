# How to: enable distributed tracing

Enable distributed tracing for a service by adding the jEAP monitoring starter and configuring trace
export and sampling, so request flows across services become visible as traces in a tracing backend
and as trace/span ids in the service's logs.

## Steps

1. Add the jEAP monitoring starter to the service:

   ```xml
   <dependency>
       <groupId>ch.admin.bit.jeap</groupId>
       <artifactId>jeap-spring-boot-monitoring-starter</artifactId>
   </dependency>
   ```

   With the starter on the classpath the service is instrumented end to end for tracing:

   - Incoming HTTP requests open a *server span*, picking up an existing trace id from the `traceparent`
     (or `B3`) header or generating a new one if there is none.
   - Outbound HTTP calls open a *client span* and propagate the trace context (`traceparent`/`B3`) to the
     next service.
   - Incoming Kafka messages open a consumer span, adopting the trace context carried in the record
     headers (`traceparent`/`B3`), or starting a new trace if none is present.
   - Outgoing Kafka messages open a producer span and inject the trace context (`traceparent`/`B3`) into
     the record headers so the consuming service continues the same trace.
   - Trace and span ids are added to the MDC for the duration of the active span scope (for an HTTP
     request or while a Kafka message is being processed) so every log line written in scope carries them.
   - A Micrometer `Tracer` bean is exposed for creating custom spans.

2. Declare the service's name, which is the name shown in the tracing backend:

   ```yaml
   spring:
     application:
       name: my-service
   ```

3. Activate trace export by pointing Spring Boot at an OTLP HTTP endpoint:

   ```yaml
   management:
     opentelemetry:
       tracing:
         export:
           otlp:
             endpoint: http://localhost:4318/v1/traces
   ```

   Without this property, traces are still produced and visible as `traceId`/`spanId` in MDC, but no
   spans leave the service. The configured URL must point to an OpenTelemetry collector.

4. Optionally, adjust the sampling rate. Spring Boot exposes a single probability property, decided at the
   root of a trace and propagated downstream so a trace is sampled in or out consistently across every
   service hop:

   ```yaml
   management:
     tracing:
       sampling:
         probability: 0.1   # default — keep 10% of traces
   ```

   Pick the probability so the resulting trace volume fits the tracing backend's capacity; production
   services typically keep the default or sample lower. For request flows that must always be
   investigable (errors, slow paths, business-critical operations), prefer always-on instrumentation in
   the service itself over raising the sample rate globally. The jEAP example services use
   `probability: 1.0` so every demo call shows up in Grafana — appropriate only for demos and debugging,
   not for production.

## Related

- [Distributed Tracing](../../concepts/logging/distributed-tracing.md) — how tracing works and how to
  instrument code that bypasses Spring-managed HTTP/Kafka clients, including custom spans.
- [jme-tracing-service](https://github.com/jme-admin-ch/jme-monitor-example/tree/main/jme-tracing-service)
  — example demonstrating this integration together with custom spans.
