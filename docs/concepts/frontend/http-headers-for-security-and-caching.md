# HTTP Headers for Security and Caching

## Overview

For frontend applications running in a web browser, setting the appropriate **HTTP headers** on resources delivered by the webserver is essential for **security and performance**. This helps prevent the risk of attacks via external scripts and injection, as well as reduce load time, especially for single-page applications.

Examples of this are:

- `Content-Security-Policy`: controls from which URLs, e.g., scripts may be loaded, iframes embedded, or APIs called.
- `Cache-Control`: tells the browser whether and for how long resources should be cached.

The page Http Headers (TODO Link) in the Frontend Development area contains a very good overview and documentation of the headers to be set.

In Spring Boot, by default only Spring Security sets some corresponding headers (e.g. no caching for secured resources). See the Spring Security reference documentation at [https://docs.spring.io/spring-security/reference/features/exploits/headers.html](https://docs.spring.io/spring-security/reference/features/exploits/headers.html).

To give Spring Boot backends an easy way to get secure, configurable defaults for HTTP headers, the **`jeap-spring-boot-web-config-starter`** is available starting with jeap-parent 17.3.0. It uses web filters to set headers for security (TODO Link) and caching (TODO Link), and supports both servlet containers.

:::warning
The starter makes certain assumptions about the structure of the API in its defaults (e.g. the headers are added for everything that isn't located under `/api`). It's primarily intended for SCS based on the jEAP Blueprint Microservice (a microservice with a frontend).

We do not recommend using the starter in apps structured differently, e.g. **not for Spring Boot Admin UIs**.
:::

## HTTP Headers in jeap-spring-boot-web-config-starter

### Patterns / Resources Considered

By default, headers are only added for the following HTTP responses:

- The HTTP method is `GET` or `HEAD`.
- The resource path (after the context root) does not start with the prefix `/api`.
- The resource path (after the context root) does not end with the suffix `-api`.

See the "Configuration" section for documentation on configuring this behavior.

### Security

:::warning
The default value for `Content-Security-Policy` is very restrictive. Many frontend apps won't work with it because, for example, they load resources from *.admin.ch or use the ePortal.

It's recommended to adjust the value by setting the `jeap.web.headers.content-security-policy` property to the desired value (see "Configuration" below).

The best approach is to start the UI with the restrictive Content-Security-Policy and fix the issues reported in the browser console by changing the application or the value of the header.
:::

| Header | Description | Default value |
| --- | --- | --- |
| [`Content-Security-Policy`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy) | Allows control over which resources the browser is allowed to load for a given page. The policies usually specify the server origin and script endpoints. This helps protect against cross-site scripting attacks.<br/><br/>Note: `connect-src` and `frame-src` are automatically extended with the source for `${jeap.security.oauth2.resourceserver.authorization-server.issuer}` so that API requests to the OAuth2 endpoint and the silent refresh in an iframe work. | `default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self'; connect-src 'self' (+OAuth2 endpoint host); frame-src 'self' (+OAuth2 endpoint host); frame-ancestors 'self'` |
| [`Referrer-Policy`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy) | Controls how much referrer information (sent with the Referer header) is included in requests. | `strict-origin-when-cross-origin` |
| [`Feature-Policy`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Feature-Policy) | The HTTP Feature-Policy header provides a mechanism to allow or deny the use of browser features in its own frame and in content within `<iframe>` elements in the document. | `microphone 'none'; payment 'none'; camera 'none'` |
| [`Strict-Transport-Security`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security) | Forces HTTPS.<br/><br/>Per [Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security), this configuration is ignored as long as the website has only been used over HTTP. So for local tests with localhost, this configuration is ignored. | `max-age=16070400; includeSubDomains` |
| [`X-Content-Type-Options`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options) | A marker used by the server to indicate that the MIME types specified in the Content-Type headers should be followed and not changed. | `nosniff` |
| [`X-Frame-Options`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options) | Indicates whether a browser is allowed to render a page in a `<frame>`, `<iframe>`, `<embed>`, or `<object>`. Protects against clickjacking attacks. | `sameorigin` |
| [`X-XSS-Protection`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection) | Legacy header that is not emitted by `jeap-spring-boot-web-config-starter`; for current browsers, Content-Security-Policy is recommended instead. | *(not set by the starter)* |

### Caching

| Header | Description | Default value |
| --- | --- | --- |
| [`Cache-Control`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control) | The HTML file is the entry point into a single-page app and must not be cached. It contains references to the cacheable resources with a hash in the file name. | .html / .json: `no-cache`<br/>.js / .css: `public, max-age=15778476, must-revalidate`<br/>other: `public, max-age=604800, must-revalidate` |
| [`Expires`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Expires) | Legacy header for older browsers, replaced by Cache-Control. | .html / .json: `0`<br/>.js / .css: `6 months`<br/>other: `public, max-age=604800, must-revalidate` |
| [`ETag`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag) | The ETag (or entity tag) HTTP response header is an identifier for a specific version of a resource. It enables more efficient use of caches and saves bandwidth, since a webserver doesn't have to resend a full response if the content hasn't changed. | Computed based on the response body, using [ShallowEtagHeaderFilter](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/filter/ShallowEtagHeaderFilter.html) |

### Integration

The `jeap-spring-boot-web-config-starter` can simply be added as a dependency (starting with jeap-parent 17.3.0):

```xml
<dependency>
    <groupId>ch.admin.bit.jeap</groupId>
    <artifactId>jeap-spring-boot-web-config-starter</artifactId>
    <version><!-- use latest version / managed by jEAP Parent --></version>
</dependency>
```

The starter then activates itself automatically if it's running in a Spring Boot webapp with a servlet container.

The technical implementation is based on a filter (servlet), i.e. HTTP requests are routed through a filter that adds the documented headers.

### Configuration

In general:

- The filter's default is to add headers (secure by default). I.e. if no `accept-path-prefixes` or `accept-path-pattern` is set, headers are added by default.
- If an `accept` property matches, the filter is activated. The `skip` properties are then processed: i.e. if a skip property matches, the headers are not added.
- HTTP request paths are always without the servlet context root.
  - I.e. for example for `/my-micro-service/api`, `/api` is used as the path in the property, assuming `server.servlet.context-path` is set accordingly.

| Property | Description | Default | Example |
| --- | --- | --- | --- |
| `jeap.web.headers.skip-path-prefixes` | For which HTTP request path prefixes the security/caching headers should NOT be added. | /api | |
| `jeap.web.headers.skip-path-suffixes` | For which HTTP request path suffixes the security/caching headers should NOT be added. | -api | |
| `jeap.web.headers.skip-path-pattern` | For which HTTP request path pattern the security/caching headers should NOT be added. | *(empty)* | |
| `jeap.web.headers.accept-path-prefixes` | For which HTTP request path prefixes the security/caching headers should be added (unless a skip property matches).<br/><br/>**If not set, headers are added for all request paths (unless a skip property matches).** | *(empty)* → all paths accepted | |
| `jeap.web.headers.accept-path-pattern` | For which HTTP request path pattern the security/caching headers should be added (unless a skip property matches). | *(empty)* | |
| `jeap.web.headers.additional-content-sources` | Sources that are added to the `connect-src` and `frame-src` lists in `Content-Security-Policy`. | `${jeap.security.oauth2.resourceserver.authorization-server.issuer}` if present, otherwise empty | `https://my-host` |
| `jeap.web.headers.content-security-policy` | Value for the Content-Security-Policy header. If empty, the default value documented above is used. | *(empty)* | `default-src: 'self'` |
| `jeap.web.headers.feature-policy` | Value for the Feature-Policy header. If empty, the default value documented above is used. Available starting with jeap-spring-boot-starters 17.40.1. | *(empty)* | `microphone 'none'; payment 'none'; camera 'none'` |
| `jeap.web.headers.http-methods` | HTTP methods for which the filter is activated, i.e. for which headers may potentially be added. | `GET, HEAD` | |

#### Dynamic Header Configuration (Computed Values, Removing Headers, Custom Headers)

Headers added by the filter can be modified or removed with a post-processor. It's also possible to add your own headers.

To do this, a bean must be provided that implements the following interface and modifies the given map:

```java
/**
 * Allows for applications to customize the HTTP headers added by a jEAP header filter. Simply provide a bean
 * implementing this interface, which will be invoked for all requests matched by the jEAP header filter.
 */
public interface HttpHeaderFilterPostProcessor {

    HttpHeaderFilterPostProcessor NO_OP = new HttpHeaderFilterPostProcessor() {
    };

    default void postProcessHeaders(Map<String, String> headers, String method, String path) {
    }
}
```
