# Styleguide and Naming Convention for REST-APIs

## 1. Overview

REST APIs should follow a consistent structure to simplify onboarding and communication, guarantee a basic minimum standard, and avoid every feature team having to define its own API design guidelines.

This style guide does not apply to partner APIs / B2B APIs; those are defined separately.

This style guide follows the very detailed [RESTful Swiss API Guidelines](https://github.com/swiss/api-guidelines/blob/main/README.md) (based on the [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/)), but it has been simplified and reduced to what is essential to improve readability. It also takes Spring Boot compatibility into account so that no unnecessary configuration is needed to comply with the guide. For details, refer to the Swiss API Guidelines, which often contain valuable additional information.


## 2. REST

Compared with, for example, SOA or RPC interfaces, [REST](https://de.wikipedia.org/wiki/Representational_State_Transfer) interfaces focus much less on use-case-specific and specialized operations (for example `ListBusinessPartnersByCountry`). Instead, REST focuses on business data entities that are exposed as **resources**, identified via URIs, and manipulated through standardized CRUD-like methods using different representations and hypermedia. Standard HTTP methods are used for this.

RESTful APIs are generally less use-case-specific, have weaker client/server coupling, and are better suited for an ecosystem of services in which a platform exposes APIs for building different business services. We apply RESTful web service principles to all microservices. This applies to **synchronous service communication via REST/HTTP**, not to asynchronous, event-driven communication via [Domain Events](todo).

For synchronous communication, we prefer REST-based APIs with JSON payloads; see the Swiss API Guidelines section on [JSON as a payload format](https://github.com/swiss/api-guidelines/blob/main/README.md#must-use-json-preferred-or-xml-as-payload-data-interchange-format-for-structured-data-167).

Synchronous means that the expected response time for a request is typically under 1 second.

## 3. General

- Security: see [Authentication for REST APIs](./todo)
- Versioning and evolution: see [Versioning for REST APIs](evolution-versioning.md)

## 4. REST Maturity Levels

The original Confluence page contained a screenshot illustrating the REST maturity levels at this point.

## 5. HTTP

### 5.1. Methods

**Idempotent** means here that the operation has the same effect on the server state whether it is executed once or multiple times, unless the resource has changed in the meantime. The main goal is to make APIs safe for retries. For a retry of an idempotent operation, the same response body and the same status code class (`2xx`, `4xx`, and so on) are expected. A slight variation in status codes that clients still must handle is acceptable, for example `200 OK` versus `201 Created` when retrying a `PUT` or `PATCH`.

Legend:

| Recommended | Limited | Usually not recommended |
| --- | --- | --- |
| Yes | Limited, see details below | Usually not in normal cases, but potentially useful for specific use cases |

| Method | Semantics | Recommended use | No state change or side effects allowed on the server side | Idempotent implementation required |
| --- | --- | --- | --- | --- |
| **`GET`** | Read resource | Yes | Yes | Yes |
| **`POST` as GET-with-body** | Read resource (for complex requests whose query is sent in the body because `GET` has no body; document this in the interface's OpenAPI documentation) | Yes | Yes | Yes |
| **`PUT`** | Replace or create a resource (*complete resource in the body*). Use create when the client determines the resource ID (for example a UUID). | Yes | No | Yes |
| **`DELETE`** | Delete resource | Yes | No | Yes |
| **`POST`** | Create resource (when the server determines the resource ID or when explicit create semantics are desired) | Limited, see [Post](#511-post) | No | No, but recommended |
| **`PATCH`** | Update *parts* of a resource | Limited, see [Patch](#512-patch) | No | Yes |
| **`HEAD`** | Like `GET`, but returns headers only | Usually not recommended | Yes | Yes |
| **`OPTIONS`** | Inspect available methods | For [CORS](https://developer.mozilla.org/de/docs/Web/HTTP/CORS) | Yes | Yes |

See also the Swiss API Guidelines section on [HTTP requests](https://github.com/swiss/api-guidelines/blob/main/README.md#7-rest-basics---http-requests).

#### 5.1.1. Post

For creating resources, `PUT` is recommended because idempotency is easier to implement. A `PUT` is sent to the resource path itself, for example `/orders/{id}`, which means it can only be used for create operations when the client can provide the resource ID. `POST` should only be used when:

- The server assigns the resource ID or the resource has no natural ID.
- Pure create semantics are explicitly desired and idempotency is not needed.
- Idempotency is also implemented with `POST`; in that case it should be documented.

#### 5.1.2. Patch

`PATCH` is used to modify parts of a resource, for example individual properties. For JSON payloads there are two RFC-defined variants, JSON Patch and JSON Merge Patch. If `PATCH` is needed for a resource, we recommend using one of these variants:

- [JSON Patch](https://tools.ietf.org/html/rfc6902)
- [JSON Merge Patch](https://tools.ietf.org/html/rfc7396)

Within one API, use one `PATCH` variant as consistently as possible, meaning either JSON Patch or JSON Merge Patch.

[Using HTTP PATCH in Spring](https://cassiomolin.com/2019/06/10/using-http-patch-in-spring/)

The complexity of `PATCH` can often be avoided by offering a `POST` or `PUT` on a sub-resource instead.

- Blog post about JSON Patch with Spring: [Using HTTP PATCH in Spring](https://cassiomolin.com/2019/06/10/using-http-patch-in-spring/)
- Library for using JSON Patch with Jackson: [java-json-tools/json-patch](https://github.com/java-json-tools/json-patch)
- Details about JSON Patch versus JSON Merge Patch: [JSON Patch vs. JSON Merge Patch](http://erosb.github.io/post/json-patch-vs-merge-patch/)

### 5.2. Implementing Idempotency

Methods that are **purely read-only** (`GET`, `HEAD`, `POST` as GET-with-body, `OPTIONS`) should be implemented as read-only operations **without side effects** or any persistent modification on the server side. They then already satisfy the idempotency requirement.

Idempotency can be implemented as follows:

| Method | Primary implementation: idempotency per resource | Possible implementation if needed: idempotency per request | Possible success status codes |
| --- | --- | --- | --- |
| `POST` | Use only when the resource ID is assigned on the server side | `Idempotency-Key` header with a request ID (for example a UUID) | `201 Created` |
| `PUT` | Resource ID in the request path | `Idempotency-Key` header with a request ID (for example a UUID) | `200 OK`, `201 Created` |
| `PATCH` | Resource ID in the request path | `Idempotency-Key` header with a request ID (for example a UUID) | `200 OK`, `204 No Content` |
| `DELETE` | `200 OK` even if the resource has already been deleted or does not exist | – | `200 OK`, `204 No Content` |

**Note:** To avoid concurrent updates or to ensure the expected initial state before an update, the [ETag header together with `If-Match` / `If-None-Match`](https://github.com/swiss/api-guidelines?tab=readme-ov-file#may-support-etag-together-with-if-matchif-none-match-header-182) can be used. See also [Optimistic locking in RESTful APIs](https://opensource.zalando.com/restful-api-guidelines/#optimistic-locking) for details and options.

### 5.3. Headers Always Required When a Response Body Is Present

| Header | Value | Description |
| --- | --- | --- |
| `Content-Type` | `application/json`, or a more specific MIME type if needed | Use `application/json` for JSON payloads and other payload types as needed, for example `text/plain`. To ensure correct processing on the client side, for example in browsers, the correct MIME type must be used. |

### 5.4. Status Codes

Responses should return specific status codes and document them in the interface documentation. This applies both to success cases (`200 OK`, `201 Created`, and so on) and to error cases (`401 Unauthorized`, `503 Unavailable`, and so on).

- When authentication and authorization are implemented with the jEAP library as described in [Authentication for REST APIs](todo), secured APIs already return correct response status codes for security-related exceptions (`401`, `403`, and so on).
- See the Swiss API Guidelines section on [common HTTP status codes](https://github.com/swiss/api-guidelines?tab=readme-ov-file#should-only-use-most-common-http-status-codes-150) for a list of status codes and the HTTP methods to which they apply.
- For bulk requests (`207 Multi-Status`), see the Swiss API Guidelines section on [batch or bulk requests](https://github.com/swiss/api-guidelines?tab=readme-ov-file#must-use-code-207-for-batch-or-bulk-requests-152).
- The official [IANA HTTP status code registry](https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml) lists all status codes and links to the corresponding RFCs.

#### 5.4.1. Status Code Categories

| Range | Meaning |
| --- | --- |
| `2xx` | Successfully processed |
| `3xx` | Redirects (less important for APIs, more relevant for websites) |
| `4xx` | The server classified the error as a client-side error; a retry is usually not appropriate |
| `5xx` | An error occurred on the server side; a retry may succeed |

#### 5.4.2. Most Important Status Codes

| Code | Meaning | Method |
| --- | --- | --- |
| `200` | OK | `*` |
| `201` | Created | `POST`, `PUT` |
| `202` | Accepted (asynchronous processing) | `POST`, `PUT`, `PATCH`, `DELETE` |
| `204` | No Content (OK, no response body) | `PUT`, `PATCH`, `DELETE` |
| `301` | Moved Permanently (redirect via `Location` header) | `*` |
| `400` | Bad Request | `*` |
| `401` | Unauthorized (usually means authentication is required) | `*` |
| `403` | Forbidden (usually missing authorization for the resource) | `*` |
| `404` | Not Found | `*` |
| `409` | Conflict — the request cannot be completed because of a conflict, for example when two clients try to create the same resource or when concurrent, conflicting updates occur | `POST`, `PUT`, `PATCH`, `DELETE` |
| `500` | Internal Server Error | `*` |

### 5.5. Compression

Compression must be enabled in Spring Boot via `server.compression.enable`.

- The remaining compression properties can stay at the Spring defaults.
- If custom MIME types are used, check whether `server.compression.mime-types` must also be adjusted so that all desired responses are compressed.
- See also [HTTP Compression with Spring Boot](./http-compression.md).

**application.yaml**

```yaml
server.compression.enable: true
```

### 5.6. Caching

Caching API requests is generally a very complex topic, especially for authenticated and authorized APIs. For that reason, using caching is generally discouraged.

Caching in REST APIs is complex because:

- Protected resources would have to be cached only in the context of authentication and authorization, including appropriate access protection.
- Cache invalidation and cache updates must be considered very carefully.
- Other mechanisms such as replication or asynchronous integration via events may also be suitable for performance optimization.

For REST APIs, caching should therefore generally not be used. Discuss any use of caching with the system architecture team and document it.

This does not affect caching of static resources, for example for frontends or single-page applications; in those cases caching should absolutely be used.

For protected resources, **spring-security** already sets the `Cache-Control: no-cache, no-store, max-age=0, must-revalidate` header **by default**, which satisfies this guideline when Spring Security is used.

## 6. Structure and Naming of Resources

See also the Swiss API Guidelines section on [REST basics - URLs](https://github.com/swiss/api-guidelines/blob/main/README.md#5-rest-basics---urls).

### 6.1. Structure & Naming

- APIs are fundamentally built around **resources** on which actions are performed using HTTP methods, for example `GET /customers/1/addresses`.
- APIs typically provide collections of resource instances. Accordingly, resource paths are named in the **plural**, for example `/customers` for the customer collection and `/customers/1` for one instance. See also the Swiss API Guidelines section on [plural resource names](https://github.com/swiss/api-guidelines/blob/main/README.md#should-pluralize-resource-names-134).
- There are **no** requests on resources that model **actions**, for example no `POST /StartBusinessProcess`. See also the Swiss API Guidelines section on [thinking in resources instead of actions](https://github.com/swiss/api-guidelines/blob/main/README.md#must-avoid-actions--think-about-resources-138).
- URLs therefore contain **no verbs**, only nouns that name the resources. See also the Swiss API Guidelines section on [verb-free URLs](https://github.com/swiss/api-guidelines/blob/main/README.md#must-keep-urls-verb-free-141).
- Resources and sub-resources are modeled as **path segments**, for example `/customers/1/addresses`. See also the Swiss API Guidelines section on [path segments](https://github.com/swiss/api-guidelines/blob/main/README.md#must-identify-resources-and-sub-resources-via-path-segments-143).
- Resource naming convention: **[Kebab-Case](http://wiki.c2.com/?KebabCase)**, meaning lowercase words separated by hyphens, for example `/tree-huggers`.
- Resource IDs must be **URL-friendly**: ASCII strings containing letters, digits, underscore, hyphen, dot, and colon.

#### 6.1.1. Examples of a Resource-Oriented API Structure

| Path | Resource | Use-case examples | Negative example |
| --- | --- | --- | --- |
| `/customers` | Collection of all customers | Read with filtering: `GET /customers?name=Meier`<br/>Read all customers with paging: `GET /customers?page=2&size=10` |  |
| `/customers/{id}` | One customer instance | Create or replace: `PUT /customers/{id}` |  |
| `/customers/{id}/preferences` | Collection of all preferences of a specific customer |  |  |
| `/process-instances/{id}` | One process instance | Start a process: `PUT /process-instances/{id}` | Starting a process via `POST /process-instances/start` is closer to RPC style than to a resource-oriented style |
| `/error-events/{id}` |  | Create: `PUT /error-events/{id}`<br/>Retry (= state change): `PUT /error-events/{id}/status` or `PATCH /error-events/{id}` with JSON Patch for the status attribute | Retrying via `POST /error-events/{id}/retry` is closer to RPC style than to a resource-oriented style.<br/>Exception: if `/retries` is a collection of all retries that is extended, then `PUT /error-events/{event-id}/retries/{retry-id}` is preferable |
| `/addresses` | Collection of all addresses |  |  |
| `/addresses/{addr}` | One address instance | Delete: `DELETE /addresses/{addr}` |  |
| `/border-crossings/{id}` | One border crossing instance |  |  |
| `/refunds/123`<br/>`/refunds/123/status` |  | Read refund request: `GET /refunds/123`<br/>Read status: `GET /refunds/123/status`<br/>Write state transition: `POST /refunds/123/status` | A state transition via `POST /error-events/{id}/retry` is closer to RPC style than to a resource-oriented style |

### 6.2. Granularity

The granularity with which resources and sub-resources are exposed depends primarily on the requirements of the API consumers.

For example, it often makes sense to provide a sub-resource to optimize the amount of transferred data, or to avoid complex patching by allowing direct access to a sub-resource. See also [Embedding & Filtering](#75-embedding-and-filtering).

## 7. Data Format (JSON, Data Types)

### 7.1. Naming

- Property names: `camelCase` (or `snake_case`), starting with a lowercase letter

```json
{
  "a": 1,
  "longerPropertyName": "b",
  "translations": {
    "de": "Farbe",
    "en": "color"
  }
}
```

### 7.2. Date / Time

Date and time values should be formatted according to ISO 8601 / [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt). See also the Swiss API Guidelines section on [standard date and time formats](https://github.com/swiss/api-guidelines/blob/main/README.md#must-use-standard-formats-for-date-and-time-properties-169).

Examples / allowed variants:

- ```text
  2020-04-23T14:50:05+02:00 (without fractional seconds)
  ```
- ```text
  2020-04-23T14:50:05.648291+02:00 (Spring Boot ZonedDateTime to JSON)
  ```
- ```text
  2020-04-29T09:52:30.502Z (UTC, also matches JSON.stringify(new Date()))
  ```
- ```text
  2015-05-28
  ```

Additional notes:

- With the default Spring Boot configuration, this corresponds to the serialization of `ZonedDateTime`.
- Be careful with time zones: to avoid implicit assumptions about the time zone of the client or server, time stamps must always include a time zone.
- In Java, use `ZonedDateTime`. In JavaScript clients, use `new Date(dateString)` or Angular's [DatePipe](https://angular.io/api/common/DatePipe) so that the zone is consumed correctly. `JSON.parse()` does not convert date strings into date objects.

### 7.3. Links

Links to resources should always use complete, absolute URLs. See also the Swiss API Guidelines section on [full, absolute URIs for resource identification](https://github.com/swiss/api-guidelines/blob/main/README.md#must-use-full-absolute-uri-for-resource-identification-217).

In Spring Boot, the external path of a request to a resource can be determined as follows:

```java
@Value("${server.servlet.context-path}")
String contextPath;

@GetMapping(path = "/full-link-example")
public String host(@RequestHeader("host") String host) {
    return "https://" + host + contextPath + "/api/linked-resource/123";
}
```

### 7.4. Paging of Collections

Resource collections that return a list of resources should provide paging whenever possible so that the amount of transferred data can be controlled sensibly. See the Swiss API Guidelines section on [pagination for large result sets](https://github.com/swiss/api-guidelines/blob/main/README.md#must-support-pagination-for-large-result-set-159).

There are:

- Offset-based pagination
- Cursor-based pagination

The latter should generally be preferred. See the Swiss API Guidelines section on [cursor-based pagination](https://github.com/swiss/api-guidelines/blob/main/README.md#should-prefer-cursor-based-pagination-160).

To keep API design consistent, the standard parameters `page`, `size`, and `sort` are recommended, or alternatively `cursor` and `limit`. The API Guidelines recommend `offset` and `limit`, but here the Spring conventions are preferred. See also the Swiss API Guidelines section on [conventional query parameters](https://github.com/swiss/api-guidelines/blob/main/README.md#should-stick-to-conventional-query-parameters-137).

Offset-based example:

```text
http://localhost:8080/people?name=Meier&page=4&size=10&sort=firstname,desc&sort=age,asc
```

Alternatively, the [paging support of Spring Data REST and Spring Data JPA](https://docs.spring.io/spring-data/rest/docs/current/reference/html/#paging-and-sorting) can also be used.

In all cases, paging must be documented in the interface documentation.

```java
// Request: /products?name=Chocolate&page=2&size=20&sort=name,asc

// Example paging with paging support from Spring Data REST
@GetMapping("/products")
public ResponseEntity<Product> findProductsByName(@RequestParam("name") String name, Pageable pageable) {
    Page<Product> products = productRepository.findAllByName(name, pageable);
    return products; // Response formatted as a Spring Data Page according to HAL
}


// Example custom implementation of cursor-based paging
@GetMapping("/products")
public ResponseEntity<Product> findProductsByName(
            @RequestParam(name = "cursor", required = false, defaultValue = "0") String cursor,
            @RequestParam(name = "limit", required = false, defaultValue = "10") int limit) {

        Instant timestamp;
        UUID lastUuid;

        if (cursor != null) {
            String[] parts = new String(Base64.getDecoder().decode(cursor)).split("\\|");
            timestamp = Instant.parse(parts[0]);
            lastUuid = UUID.fromString(parts[1]);
        } else {
            timestamp = Instant.EPOCH;
            lastUuid = new UUID(0, 0);
        }
        Page<Product> products = productRepository.findAfterCursor(timestamp, lastUuid, PageRequest.of(0, limit + 1));

        boolean hasNext = products.size() > limit;

        if (hasNext) {
            products = products.subList(0, limit);
        }

        String nextCursor = products.isEmpty() ? null :
                encodeCompositeCursor(
                        products.get(products.size() - 1).getCreatedAt(),
                        products.get(products.size() - 1).getId()
                );

        return ResponseEntity.ok(new CursorPage<>(products, nextCursor, hasNext));
}
```

Services with special paging needs, for example when `totalElements` is expensive to calculate or when [paging via cursor](https://opensource.zalando.com/restful-api-guidelines/#160) is better suited for browsing streams or NoSQL use cases, are free to implement their own paging model.

### 7.5. Embedding and Filtering

For larger or more complex resources, it can make sense for specific use cases to transfer only part of a resource, or a resource together with sub-resources, in order to optimize payload size. Both options should only be implemented when needed and should then also be documented.

See also:

- The Swiss API Guidelines section on [partial responses via filtering](https://opensource.zalando.com/restful-api-guidelines/#157)
- The Swiss API Guidelines section on [optional embedding of sub-resources](https://opensource.zalando.com/restful-api-guidelines/#158)

## 8. Error Handling

Error responses should return a structured, documented error object as JSON. It must include a correlation ID that makes it possible to find the error in the log files.

Error responses must be signaled with an appropriate HTTP status code (`4xx`, `5xx`) and not only in the response body.

Example format (corresponding to the default format of Spring Boot; see [DefaultErrorAttributes](https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/web/servlet/error/DefaultErrorAttributes.html)):

**Error response**

```javascript
{
    "timestamp": "2020-04-24T07:53:34.412+0000",
    "status": 500,
    "error": "Internal Server Error",
    "message": "bla",
    "correlationId": "2134-1234-1234-1234"
    "path": "/fault",
    // ... custom, specific error attributes ...
}
```

## 9. Queries

- Simple queries should be implemented via the URL query string, for example `GET /customers?name=Meier&age=5`.
  - Naming convention for query parameters: `snake_case` or lowercase with underscores, for example `max_length`.
  - See also the Swiss API Guidelines sections on [simple query languages using query parameters](https://github.com/swiss/api-guidelines/blob/main/README.md#should-design-simple-query-languages-using-query-parameters-236) and [query parameter naming](https://github.com/swiss/api-guidelines/blob/main/README.md#must-use-snake_case-or-camelcase-for-query-parameters-130).
- Complex queries can be transmitted via a JSON payload. There is no fixed structure because it is domain-specific. For ideas, see the Swiss API Guidelines section on [complex query languages using JSON](https://github.com/swiss/api-guidelines/blob/main/README.md#should-design-complex-query-languages-using-json-237).

## 10. GraphQL, RPC, Server-Sent Events, ...

If you want to use these technologies, coordinate it with the system architect / Margun first.

## 11. Further Documentation

- [https://restful-api-design.readthedocs.io/en/latest/](https://restful-api-design.readthedocs.io/en/latest/)
- [api-guidelines/README.md at main · swiss/api-guidelines](https://github.com/swiss/api-guidelines/blob/main/README.md)
- [https://opensource.zalando.com/restful-api-guidelines/](https://opensource.zalando.com/restful-api-guidelines/)
- [https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#3-introduction](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#3-introduction)
- [https://docs.spring.io/spring-data/rest/docs/current/reference/html/#paging-and-sorting](https://docs.spring.io/spring-data/rest/docs/current/reference/html/#paging-and-sorting)
- [https://de.wikipedia.org/wiki/Hypertext_Application_Language](https://de.wikipedia.org/wiki/Hypertext_Application_Language)
