# Application Logs

## Overview

Every application generates its own record (*log*) for recording and tracing error conditions. This page
describes creating the log of a single microservice. For logging an application consisting of multiple
microservices, see also [Logging](index.md). Logging should be complemented with
[Distributed Tracing](distributed-tracing.md).

## Framework

All logging should go through [SLF4j](http://www.slf4j.org/) as a logging facade. This makes the actual
logging infrastructure interchangeable. If [Lombok](https://projectlombok.org/) is used, a logger can be
added to any class via an annotation.

**Slf4j Logger with Lombok**

```java
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class RestExample {
    public void main() {
	//The annotation generates a field "log" that can be used for logging
        log.info("Log Message");
    }
}
```

The format of the log output can be configured via the `logback-spring.xml` file.

## StructuredArguments

To generate log entries, the StructuredArguments API from logstash can be used. It provides functions that
add additional key-value pairs to a log entry. In particular, the `keyValue` and `value` functions are
useful. When logs are generated as JSON, the key-value pairs are also added directly into the JSON structure.

**Logging with Structured Arguments**

```java
import lombok.extern.slf4j.Slf4j;
import static net.logstash.logback.argument.StructuredArguments.keyValue;
import static net.logstash.logback.argument.StructuredArguments.value;

@Slf4j
public class Example{
    public void main() {
	//Generates the log message "Log a KeyValue-Pair  key=importantValue"
        log.info("Log a KeyValue-Pair {}", keyValue("key", "importantValue"));

	 //Generates the log message "Log only a value importantValue"
        log.info("Log only a value {}", value("key", "importantValue"));
    }
}
```

With Structured Arguments, project-specific functions or even project-specific classes can be defined
directly.

**Project-specific function with Structured Arguments**

```java
/**
 * This function can be used like
 * <p>
 *
 * <pre>
 * logger.info("Current user is {}", user(user));
 * </pre>
 * <p>
 * results in the following log event output:
 *
 * <pre>
 * {
 *     "message" : "Current user is user=1234",
 *     "user"    : 1234
 * }
 * <p>
 */
public static StructuredArgument user(User user) {
 return keyValue("user", user.getUserId());
}
```

**Project-specific class with Structured Arguments**

```java
package ch.admin.jeap.example.log.receiver;

import com.fasterxml.jackson.core.JsonGenerator;
import net.logstash.logback.argument.StructuredArgument;
import net.logstash.logback.marker.SingleFieldAppendingMarker;
import java.io.IOException;

public class UserAppendingMarker extends SingleFieldAppendingMarker {
    private final static String FIELD_NAME = "user";
    private static final String MARKER_NAME = SingleFieldAppendingMarker.MARKER_NAME_PREFIX + "USER";
    private static final String VALUE_ONLY_MESSAGE_FORMAT_PATTERN = "{1}";
    private final User user;

    private UserAppendingMarker(User user) {
        super(MARKER_NAME, FIELD_NAME, VALUE_ONLY_MESSAGE_FORMAT_PATTERN);
        this.user = user;
    }

    /**
     * This function can be used like
     * <p>
     *
     * <pre>
     * logger.info("Current user is {}", user(user));
     * </pre>
     * <p>
     * results in the following log event output:
     *
     * <pre>
     * {
     *     "message" : "Current user is USERNAME",
     *     "user"     : {"id":1234, "name":"USERNAME"}
     * }
     * <p>
     */
    public static StructuredArgument user(User user) {
        return new UserAppendingMarker(user);
    }

    /**
     * This function will be used to write the JSON value
     */
    @Override
    protected void writeFieldValue(JsonGenerator jsonGenerator) throws IOException {
        jsonGenerator.writeStartObject();
        jsonGenerator.writeObjectField("id", user.getId());
        jsonGenerator.writeObjectField("name", user.getUsername());
        jsonGenerator.writeEndObject();
    }

    /**
     * This function will be used to write the part of the message
     */
    @Override
    protected Object getFieldValue() {
        return user.getUsername();
    }
}
```

### Format

So that log entries can be optimally searched and analyzed in Splunk, they should all follow the same
format. Log entries should be a single-line JSON string containing at least the following information:

| Name | Data type | Example | Description |
| --- | --- | --- | --- |
| `app` | String | `eets-manualtask-service` | Name of the application. The name should start with the system name (e.g. `eets-XXX`). |
| `@timestamp` | Date and time in ISO 8601 format | `2019-09-06T08:23:59.432+02:00` | Time when the log entry was generated |
| `logger` | String | `s.d.s.w.r.o.CachingOperationNameGenerator` | Name of the logger, usually the name of the class |
| `thread_name` | String | `main` | The name of the thread |
| `level` | `TRACE`, `DEBUG`, `INFO`, `WARN` or `ERROR` | `INFO` | The log level |
| `message` | String | `test` | The log message |

**Example output (minimal)**

```js
{"app":"eets-manualtask-service","@timestamp":"2019-09-06T08:23:59.432+02:00", "logger":"s.d.s.w.r.o.CachingOperationNameGenerator", "level":"INFO",  "thread_name":"main",  "message":"test"}
```

Additional fields can be added by Spring Cloud Sleuth (see [Distributed Tracing](distributed-tracing.md)) or
with StructuredArguments:

**Example output (with Spring Cloud Sleuth)**

```js
{"@timestamp":"2019-09-19T09:58:39.152+00:00","app":"jeap-example-log-receiver","logger":"c.a.j.e.l.r.RestExample","level":"INFO","thread_name":"http-nio-8080-exec-8","traceId":"4c22a312eddf78bc","spanId":"9947870202d65e02","spanExportable":"false","X-Span-Export":"false","X-B3-SpanId":"9947870202d65e02","X-B3-ParentSpanId":"4c22a312eddf78bc","X-B3-TraceId":"4c22a312eddf78bc","parentId":"4c22a312eddf78bc","message":"Received a rest call"}
```

## Application-specific IDs

A log entry should, where possible, include the ID(s) of the objects being processed. This makes it possible
to search for these IDs and thus, especially in case of errors, quickly find out what the different systems
have done. Such IDs can easily be integrated with StructuredArguments.

**Application-specific IDs with Structured Arguments**

```java
logger.info("declaration {} has failed plausibility check", keyValue("declarationId", declaration.getId())
```

This generates a message:

**Example output (application-specific IDs)**

```js
...,"message":"declaration 123e4567-e89b-12d3-a456-426655440000 has failed plausibility check", "declarationID": "123e4567-e89b-12d3-a456-426655440000"}
```

To unify and simplify this, functions and classes as described under StructuredArguments can be used.

## Levels

The following log levels should be used:

| Name | Meaning | Examples |
| --- | --- | --- |
| `TRACE` | Automated tracing information. Should be disabled by default. | Method calls |
| `DEBUG` | Information relevant only for development; disabled by default in production. | Additional information for troubleshooting |
| `INFO` | Relevant information for understanding the status of the program. This information can e.g. be used to create analyses and dashboards in Splunk. Note: especially for frequently occurring events, it should be critically questioned whether the `DEBUG` level would not be sufficient, for example for the repeated successful processing (= normal behavior) of a frequent input. | Processing of events, changing a business object, security-relevant events with expected result |
| `WARN` | Exceptional situations that can be handled by the application itself. | Processing of events, changing a business object, security-relevant events with unexpected result |
| `ERROR` | Unexpected situations that endanger the functionality of the application. Should be used when a user should intervene to ensure the functionality of the program. Usually leads to an incident. | Input data is invalid and cannot be processed, and the calling system could be informed |

## Integration

A Spring Boot Starter **jeap-spring-boot-logging-starter** is available. It includes the following:

- Dependencies for [Distributed Tracing](distributed-tracing.md)
- Generates JSON logs for the `rhos` profile
- Generates normal (more readable) log output when the `rhos` profile is not active

The starter can easily be integrated using:

**Dependency for jeap-spring-boot-logging-starter**

```xml
<dependency>
    <groupId>ch.admin.bit.jeap</groupId>
    <artifactId>jeap-spring-boot-logging-starter</artifactId>
</dependency>
```

## Example

An example of how logging can be integrated into a Spring Boot application can be found in
[jme-monitor-example](https://github.com/jme-admin-ch/jme-monitor-example).

## Further documentation

- [Slf4j annotation in Lombok](https://projectlombok.org/api/lombok/extern/slf4j/Slf4j.html)
- [Slf4j documentation](https://www.slf4j.org/docs.html)
- [Structured Logging with Structured Arguments](https://www.innoq.com/en/blog/structured-logging/#structuredarguments)
