# Direct Frontend Route Navigation Redirect in Spring Boot SCS

## Context

**Single-Page Application** JavaScript frontends tend to use some sort of **routing** to navigate between different views. This happens entirely in the browser once the frontend application has been loaded from `index.html`.

There is one exception to this: when a **user navigates directly to a frontend route** - for example from an external link or from a bookmark - the **request is sent to the webserver**. The webserver then needs to serve the content of `index.html` as a response. The browser will start the SPA and use its frontend routing logic to show the targeted view.

## The Problem

**Since Spring 6.1 / Spring Boot 3.2**, a `NoResourceFoundException` is thrown when no request mapping matches a request, and no static resource matches either (see this [commit](https://github.com/spring-projects/spring-framework/commit/c00508d6cf2408d06a0447ed193ad96466d0d7b4)).

This **broke the workaround** for direct frontend route navigation present in many Spring Boot apps. This usually involved returning the content of `index.html` for any request that returned a 404 / Not Found response.

SPAs would still work when navigating to `/` or `/index.html`, but not when navigating directly to a frontend route such as `/some-route`. For such requests, an **error response** is now returned:

```json
{"timestamp":"2024-02-02T15:13:41.460+00:00","status":404,"error":"Not Found","path":"/my-app/some-route"}
```

## Possible Solutions

### Option 1) Serve index.html when no matching resource is found

To find out if a request might contain the path to a frontend route, there is always some heuristic involved, as the backend will not know all frontend routes - unless you would configure them explicitly somewhere, which might be fragile and leads to duplication.

A possible solution is to:

- Rely on Spring to apply all request mappings, and then fall back to finding a matching static resource.
- If no static resource is found, try to determine if the request might be a direct frontend route navigation:
  - The request does not contain a dot, otherwise it is probably a file request such as `/my.css`.
  - The first path segment does not contain `api` or `actuator` (the default ignored root-path parts).
- Serve the contents of `index.html` if we can assume a direct frontend route navigation.

This is triggered by a `NoResourceFoundException`, and implemented inside a `@ControllerAdvice` / `ResponseEntityExceptionHandler`. If you have an existing `ResponseEntityExceptionHandler`, you can extend from the `FrontendRouteRedirectExceptionHandler` provided by jEAP. Otherwise, create a new instance of the advice as provided by the `jeap-spring-boot-application-starter`:

```java
// Extend from the controller advice doing frontend route redirects to implement your own controller advice
@ControllerAdvice
public class MyControllerAdvice extends FrontendRouteRedirectExceptionHandler {
    // ... your own exception handlers
}

// - or -
// Create the controller advice as a bean if you don't need an own controller advice
@Bean
public FrontendRouteRedirectExceptionHandler frontendRouteRedirectExceptionHandler() {
    return new FrontendRouteRedirectExceptionHandler();
}
```

Source code of the controller advice (see [`FrontendRouteRedirectExceptionHandler.java`](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-application-starter/src/main/java/ch/admin/bit/jeap/starter/application/web/FrontendRouteRedirectExceptionHandler.java) in the jeap-spring-boot-starters repository):

```java
package ch.admin.bit.jeap.starter.application.web;

import ch.admin.bit.jeap.rest.tracing.FrontendRouteRequestMarker;
import org.springframework.core.io.ClassPathResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;
import org.springframework.web.servlet.resource.NoResourceFoundException;

import java.util.Set;

/**
 * This class can be used as a bean annotated with @ControllerAdvice, or as a base class for custom controller advice
 * handlers. It will forward (possible) frontend route requests to /index.html, serving the contents of index.html
 * and return HTTP 200 OK. This is a desired behaviour for SPAs that serve frontend routes and backend APIs from
 * the same root context.
 */
@ControllerAdvice
public class FrontendRouteRedirectExceptionHandler extends ResponseEntityExceptionHandler {

    private final Set<String> nonFrontendRootPathParts;

    public FrontendRouteRedirectExceptionHandler() {
        nonFrontendRootPathParts = Set.of("api", "actuator");
    }

    public FrontendRouteRedirectExceptionHandler(Set<String> nonFrontendRootPathParts) {
        this.nonFrontendRootPathParts = Set.copyOf(nonFrontendRootPathParts);
    }

    /**
     * This handler makes sure that direct navigation to a route of a single page application is forwarded to index.html.
     * When then navigating inside the SPA in the browser, this handler is not invoked as the SPA code in the browser
     * takes care of route navigation.
     */
    @Override
    protected ResponseEntity<Object> handleNoResourceFoundException(NoResourceFoundException ex, HttpHeaders headers, HttpStatusCode status, WebRequest request) {
        // If the request looks like a frontend route, return index.html
        if (mightBeFrontendRoute(request)) {
            // Mark the request as a frontend route, i.e. as a request not targeting a backend endpoint, to exclude it
            // from the security tracing detecting endpoints being called without a JWT bearer token
            FrontendRouteRequestMarker.markAsFrontendRoute(request);
            return new ResponseEntity<>(new ClassPathResource("/static/index.html"), headers, 200);
        }
        // Otherwise, generate a 404 NOT FOUND response
        return super.handleNoResourceFoundException(ex, headers, status, request);
    }

    public boolean mightBeFrontendRoute(WebRequest webRequest) {
        return FrontendRouteMatcher.mightBeFrontendRouteWithIgnoreList(webRequest, nonFrontendRootPathParts);
    }

}
```

Source code of the frontend route matcher (see [`FrontendRouteMatcher.java`](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-application-starter/src/main/java/ch/admin/bit/jeap/starter/application/web/FrontendRouteMatcher.java) in the jeap-spring-boot-starters repository):

```java
package ch.admin.bit.jeap.starter.application.web;

import org.springframework.web.context.request.ServletWebRequest;
import org.springframework.web.context.request.WebRequest;

import java.util.Set;

public class FrontendRouteMatcher {

    public static boolean mightBeFrontendRouteWithIgnoreList(WebRequest webRequest, Set<String> nonFrontendRootPathParts) {
        if (webRequest instanceof ServletWebRequest servletRequest && servletRequest.getRequest().getServletPath() != null) {
            String path = servletRequest.getRequest().getServletPath();
            return mightBeFrontendPathWithIgnoreList(path, nonFrontendRootPathParts);
        }
        return false;
    }

    private static boolean mightBeFrontendPathWithIgnoreList(String path, Set<String> nonFrontendRootPathParts) {
        // Does the request look like a file with a dot extension?
        boolean hasFileExtension = path.contains(".");
        if (hasFileExtension) {
            return false;
        }

        // Does the request contain a known non-frontend path part such as api, actuator, ...
        String[] pathSegments = path.replaceFirst("^/", "").split("/", 2);
        String rootPath = pathSegments[0].toLowerCase();

        return nonFrontendRootPathParts.stream()
                .noneMatch(rootPath::contains);
    }
}
```

### Option 2) Prefix Routes and Forward Requests

As an alternative approach, you could prefix all frontend routes with a common path such as `/route`. This eliminates the need for any heuristic in the webserver to determine whether a request might be a frontend route. The Spring Boot app can then match route requests by a prefix, and forward such requests to `index.html` internally. This will also simplify security configurations as the request filter for public frontend routes will be more specific.

The only downside is that the URL in the browser will include the `/route` prefix for all views.

Example code:

```java
@Controller
public class ClientForwardingController {

    // Note: For this to work, all frontend routes must start with /route
    @GetMapping(path = { "/route/**" })
    public String forwardRoutePaths() {
        return "forward:/index.html";
    }
}
```
