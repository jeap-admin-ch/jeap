# Direct Frontend Route Navigation Redirect in Spring Boot SCS

## Context

**Single-Page Application** JavaScript frontends route between views entirely in the browser once loaded from `index.html` - except when a **user navigates directly to a frontend route**, e.g. from an external link or a bookmark. That request goes to the webserver, which must serve the content of `index.html` so the browser can start the SPA and show the targeted view.

## The Problem

**Since Spring 6.1 / Spring Boot 3.2**, a `NoResourceFoundException` is thrown when no request mapping and no static resource matches a request (see this [commit](https://github.com/spring-projects/spring-framework/commit/c00508d6cf2408d06a0447ed193ad96466d0d7b4)). This broke the common workaround of returning `index.html` for any 404 response: navigating directly to a frontend route such as `/some-route` now returns an error response instead of the SPA shell:

```json
{"timestamp":"2024-02-02T15:13:41.460+00:00","status":404,"error":"Not Found","path":"/my-app/some-route"}
```

## Fixing It

**See [How to: handle direct frontend route navigation in Spring Boot SCS](../../how-tos/rest-apis-and-web/handle-direct-frontend-route-navigation.md)**
for two ways to fix this: serving `index.html` via an exception handler, or prefixing frontend routes and forwarding requests.
