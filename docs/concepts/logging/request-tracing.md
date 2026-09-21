# Request Tracing

## Overview

**Request Tracing** helps to understand what is happening on a system. For this purpose, every call to a
service logs who called what and how the service reacted.

## Integration

### Rest-Tracing

The `jeap-spring-boot-logging-starter` supports request tracing for HTTP calls. For every call, the
following log statements are generated:

> The structured JSON attributes are only logged if JSON logs are activated by having the Spring profile
> "cloud" active. During local development, usually only the "message" attribute is logged.

**Rest-Request Tracing**

```js
{"@timestamp":"2020-06-04T08:22:32.418+02:00","app":"jme-security-resource-service","logger":"c.a.b.j.l.RestRequestTracer","level":"DEBUG","thread_name":"http-nio-8070-exec-4","traceId":"a50f9e5204d49db3","spanId":"a4f83bef37617183","spanExportable":"false","X-Span-Export":"false","X-B3-SpanId":"a4f83bef37617183","X-B3-ParentSpanId":"a50f9e5204d49db3","X-B3-TraceId":"a50f9e5204d49db3","parentId":"a50f9e5204d49db3","method":"GET","uri":"http://localhost:8070/jme-security-resource-service/api/partners","message":"Incoming GET Request to http://localhost:8070/jme-security-resource-service/api/partners"}

{"@timestamp":"2020-06-04T08:22:32.516+02:00","app":"jme-security-resource-service","logger":"c.a.b.j.l.RestRequestTracer","level":"INFO","thread_name":"http-nio-8070-exec-4","traceId":"a50f9e5204d49db3","spanId":"a4f83bef37617183","spanExportable":"false","X-Span-Export":"false","X-B3-SpanId":"a4f83bef37617183","X-B3-ParentSpanId":"a50f9e5204d49db3","X-B3-TraceId":"a50f9e5204d49db3","parentId":"a50f9e5204d49db3","method":"GET","uri":"http://localhost:8070/jme-security-resource-service/api/partners","result":200,"caller":"jme-security-client-service","user":"13e26074-acfb-4041-ba6c-96a50a4ddd5a","dt":97,"remoteAddr":"/127.0.0.1:38302","requestHeaders":{"authorization":["***"],"x-b3-parentspanid":["a50f9e5204d49db3"],"x-b3-traceid":["a50f9e5204d49db3"],"x-b3-spanid":["a4f83bef37617183"],"x-b3-sampled":["0"],"host":["localhost:8070"],"jeap_application_name":["jme-security-client-service"],"accept-encoding":["gzip"],"user-agent":["ReactorNetty/0.9.4.RELEASE"],"accept":["*/*"]},"responseHeaders":{"X-Frame-Options":["DENY"],"Cache-Control":["no-cache, no-store, max-age=0, must-revalidate"],"X-Content-Type-Options":["nosniff"],"Vary":["Origin","Access-Control-Request-Method","Access-Control-Request-Headers"],"Set-Cookie":["XSRF-TOKEN=89e20e57-0388-4097-a2a9-1e6a7a0fef3f; Path=/jme-security-resource-service"],"Pragma":["no-cache"],"Expires":["0"],"X-XSS-Protection":["1; mode=block"],"Content-Length":["24"],"Date":["Thu, 04 Jun 2020 06:22:32 GMT"],"Content-Type":["text/plain;charset=UTF-8"]},"attributes":{"org.springframework.web.servlet.HandlerMapping.bestMatchingHandler":"ch.admin.bit.jeap.jme.security.oauth.resource.RolesProtectedOAuth2RestResource#listPartners()","org.springframework.web.servlet.HandlerMapping.bestMatchingPattern":"/api/partners","org.springframework.web.servlet.HandlerMapping.pathWithinHandlerMapping":"/api/partners","org.springframework.web.servlet.HandlerMapping.lookupPath":"/api/partners","org.springframework.web.servlet.HandlerMapping.uriTemplateVariables":"{}"},"message":"GET http://localhost:8070/jme-security-resource-service/api/partners result=200 caller=jme-security-client-service user=13e26074-acfb-4041-ba6c-96a50a4ddd5a"}
```

After the request has been answered, the following data is output:

| Field | Description | Example |
| --- | --- | --- |
| `method` | HTTP method used | `GET` |
| `uri` | Called URL incl. host and context path | `http://localhost:8070/jme-security-resource-service/api/info` |
| `result` | Returned HTTP status code | `200` |
| `caller` | Service that made the call, or `null` e.g. for calls from outside | `jme-security-client-service` |
| `user` | PAMS ID of the user, or `null` if no user is logged in | `13e26074-acfb-4041-ba6c-96a50a4ddd5a` |
| `dt` | Time in milliseconds needed to answer the request. Measured from receiving the first data until sending the response | `97` |
| `remoteAddr` | Address of the caller. In the CF currently always a load balancer | `/127.0.0.1:38302` |
| `requestHeaders` | The HTTP request headers. It can be configured which headers are logged and which are masked (see below) | |
| `responseHeaders` | The HTTP response headers. It can be configured which headers are logged and which are masked (see below) | |
| `attributes` | The Spring request attributes. It can be configured which attributes are logged. By default, which mapping was used | |

Whether an application generates tracing logs can be controlled using the log level for
`ch.admin.bit.jeap.log.RestRequestTracer`. At `DEBUG`, a log statement is generated after answering the
request, and at `TRACE`, an additional log statement is generated when each request is received. In
addition, the following properties can be set:

```java
logging.level:
  ch.admin.bit.jeap.log.RestRequestTracer: DEBUG # or TRACE
```

| Property | Description | Default |
| --- | --- | --- |
| `jeap.rest.tracing.headerMasked` | A list of headers for which the value should be masked (replaced by "***") because they contain sensitive information that should not be logged, e.g. passwords in the Authorization header. Applies to request and response headers. | `Authorization`, `Cookie`, `Set-Cookie`, `Set-Cookie2` |
| `jeap.rest.tracing.headerBlacklist` | Headers that should not be logged at all, e.g. because too much log output would be generated. Applies to request and response headers. | (empty) |
| `jeap.rest.tracing.attributesWhitelist` | Prefix of request attribute names that should be logged | `org.springframework.web.reactive.HandlerMapping`, `org.springframework.web.servlet.HandlerMapping` |
| `jeap.rest.tracing.applicationName` | The application name that is sent with a request to another system. | `${spring.application.name}` |

### Event-Tracing

The [Jeap Messaging Library](../messaging/jeap-messaging-library/index.md) supports request tracing for
Kafka events. For every event, the following log statements are generated:

> The structured JSON attributes are only logged if JSON logs are activated by having the Spring profile
> "cloud" active. During local development, usually only the "message" attribute is logged.

**Event Request-Tracing**

```js
{"@timestamp":"2020-06-04T08:55:36.676+02:00","app":"jme-event-receiver-service","logger":"c.a.b.j.d.k.l.ConsumerLoggingInterceptor","level":"INFO","thread_name":"org.springframework.kafka.KafkaListenerEndpointContainer#0-0-C-1","eventType":"JmeDeclarationCreatedEvent","eventVersion":"1.0.0","eventId":"caf30b40-85f2-48ae-b3b8-bbd504b1a312","eventIdempotenceId":"9baf43b0-472e-4c0d-ba93-e6f076d5f932","eventCreated":"2020-06-04T06:55:36.534Z","eventPublisherSystem":"JME","eventPublisherService":"jeap-microservice-examples-kafka","topic":"jme-event-jmedeclaration-created","partition":0,"message":"Received JmeDeclarationCreatedEvent (caf30b40-85f2-48ae-b3b8-bbd504b1a312) from jme-event-jmedeclaration-created (0) with offset 2"}

{"@timestamp":"2020-06-04T08:55:36.691+02:00","app":"jme-event-receiver-service","logger":"c.a.b.j.d.k.l.ConsumerLoggingInterceptor","level":"DEBUG","thread_name":"org.springframework.kafka.KafkaListenerEndpointContainer#0-0-C-1","offset":3,"topic":"jme-event-jmedeclaration-created","partition":0,"metadata":"","message":"Commit offset 3 on jme-event-jmedeclaration-created (0) with "}
```

The following data is output:

| Field | Description | Example |
| --- | --- | --- |
| `eventType` | Attributes from the [Message Types](../messaging/message-types.md) | `JmeDeclarationCreatedEvent` |
| `eventVersion` | Attributes from the [Message Types](../messaging/message-types.md) | `1.0.0` |
| `eventId` | Attributes from the [Message Types](../messaging/message-types.md) | `caf30b40-85f2-48ae-b3b8-bbd504b1a312` |
| `eventIdempotenceId` | Attributes from the [Message Types](../messaging/message-types.md) | `9baf43b0-472e-4c0d-ba93-e6f076d5f932` |
| `eventCreated` | Attributes from the [Message Types](../messaging/message-types.md) | `2020-06-04T06:55:36.534Z` |
| `eventPublisherSystem` | Attributes from the [Message Types](../messaging/message-types.md) | `JME` |
| `eventPublisherService` | Attributes from the [Message Types](../messaging/message-types.md) | `jeap-microservice-examples-kafka` |
| `topic` | Topic, partition and offset from which the event was read | `jme-event-jmedeclaration-created` |
| `partition` | Topic, partition and offset from which the event was read | `0` |
| `offset` | Topic, partition and offset from which the event was read | `2` |

Whether an application generates tracing logs can be controlled using the log level for
`ch.admin.bit.jeap.domainevent.kafka.log.ConsumerLoggingInterceptor`. At `INFO`, a log statement is generated
on receiving, and at `DEBUG`, an additional log statement is generated after processing each event.

## Example

All JME examples use request tracing. For Rest-Tracing, see e.g.
[jme-monitor-example](https://github.com/jme-admin-ch/jme-monitor-example); for Messaging-Tracing, see
[jme-messaging-example](https://github.com/jme-admin-ch/jme-messaging-example).
