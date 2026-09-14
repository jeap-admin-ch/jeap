# HTTP Compression with Spring Boot

## Overview

Microservices that generate large HTTP responses should compress the response data to save network bandwidth and improve response times for their clients. For compression to work, it must be supported by both the HTTP server and the HTTP clients accessing the server. The following sections explain how to enable HTTP compression in Spring Boot-based microservices.

## HTTP Server

To enable compression on the server, set the following Spring Boot property:

```yaml
server.compression.enabled: true
```

[Additional configuration options](https://docs.spring.io/spring-boot/appendix/application-properties/index.html#appendix.application-properties.server) are available for specific use cases, such as:

- `server.compression.mime-types`: specify which MIME types to compress
- `server.compression.min-response-size`: set the minimum response size for compression
- `server.compression.excluded-user-agents`: exclude certain user agents from compression

## HTTP Clients

There are many Java HTTP clients available, and Spring Boot supports several of them. However, unlike for HTTP servers, there are no general Spring Boot configuration properties or mechanisms to enable compression on HTTP clients. Additionally, not all HTTP clients directly support HTTP compression.

The easiest way to enable compression for HTTP clients in Spring Boot is to use a client that natively supports compression and is supported by Spring Boot.

### Spring WebMVC

#### HTTP Client for RestClient

When using Spring's `RestClient` for HTTP calls, you can enable compression by adding the following dependency to your project:

```xml
<dependency>
    <groupId>org.apache.httpcomponents.client5</groupId>
    <artifactId>httpclient5</artifactId>
</dependency>
```

This dependency provides the Apache HTTP client, which is the preferred HTTP client implementation for the `RestClient.Builder`. Compression is enabled by default in the Apache HTTP client.

To customize the HTTP client or disable compression, you must explicitly create the HTTP client and configure a request factory, as shown below:

```java
CloseableHttpClient httpClient = HttpClients.custom().
		// disableContentCompression(). // Uncomment to disable compression
        // additional http client customizations
        build();
HttpComponentsClientHttpRequestFactory requestFactory =  new HttpComponentsClientHttpRequestFactory(httpClient);
RestClient restClient = jeapOAuth2RestClientBuilderFactory.createForClientRegistryId(id).
        requestFactory(requestFactory).
        build();
```

## Examples

For a `RestClient` instance with compression support enabled, see [`HttpClientTestController.java`](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-client-service/src/main/java/ch/admin/bit/jeap/jme/security/oauth/client/HttpClientTestController.java) in the `jme-security-example` repository:

```java
private RestClient createDefaultRestClient() {
    return jeapOAuth2RestClientBuilderFactory.createForClientRegistryId(clientProperties.getClientRegistrationId()).
            baseUrl(clientProperties.getResourceUrl()).
            build();
}

private RestClient createCustomRestClient() {
    // Create and customize an Apache HTTP client
    CloseableHttpClient httpClient = HttpClients.custom().
            // disableContentCompression().
            // additional http client customizations
                    build();
    HttpComponentsClientHttpRequestFactory requestFactory = new HttpComponentsClientHttpRequestFactory(httpClient);
    return jeapOAuth2RestClientBuilderFactory.createForClientRegistryId(clientProperties.getClientRegistrationId()).
            baseUrl(clientProperties.getResourceUrl()).
            requestFactory(requestFactory).
            build();
}

private RestClient createCustomRestClientHttp2() {
    CloseableHttpClient httpClient = HttpClients.custom().
            // check that the response is an HTTP/2 response
                    addResponseInterceptorFirst(this::checkHttp2).
            build();
    HttpComponentsClientHttpRequestFactory requestFactory = new HttpComponentsClientHttpRequestFactory(httpClient);
    return jeapOAuth2RestClientBuilderFactory.createForClientRegistryId(clientProperties.getClientRegistrationId()).
            baseUrl(clientProperties.getResourceUrl()).
            requestFactory(requestFactory).
            build();
}

private void checkHttp2(HttpResponse response, EntityDetails details, HttpContext context) throws HttpException {
    final ProtocolVersion responseProtocolVersion = context.getProtocolVersion();
    final ProtocolVersion http2 = new ProtocolVersion("HTTP", 2, 0);
    log.info("Response protocol version is {}", responseProtocolVersion);
    if (!responseProtocolVersion.greaterEquals(http2)) {
        String notHttp2Message = "Expected response protocol version equal or greater than " + http2 + " but got " + responseProtocolVersion;
        log.error(notHttp2Message);
        throw new HttpException(notHttp2Message);
    }
}
```

For enabling compression support in a Spring Boot HTTP server, see [`application.yml`](https://github.com/jme-admin-ch/jme-security-example/blob/main/jme-security-resource-service/src/main/resources/application.yml) in the `jme-security-example` repository:

```yaml
server:
  servlet:
    context-path: /${spring.application.name}
  compression:
    enabled: true
    # Enable compression even on the very small responses of this example
    min-response-size: 10
```
