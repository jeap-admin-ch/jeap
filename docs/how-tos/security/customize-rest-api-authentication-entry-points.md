# How to: customize REST API authentication entry points, access-denied handling and method security

`jeap-spring-boot-security-starter` lets an application override how authentication failures and access-denied
errors on OAuth2-protected REST APIs are handled, and how method security expressions are evaluated, without
replacing the starter's OAuth2 resource server configuration.

## Override the AuthenticationEntryPoint or the AccessDeniedHandler

Available as of version 12.6.0 of jeap-spring-boot-security-starter.

1. Define a custom Spring bean of type `JeapOauth2ResourceAuthenticationEntryPoint` and/or
   `JeapOauth2ResourceAccessDeniedHandler` to override the AuthenticationEntryPoint and/or the AccessDeniedHandler
   of the OAuth2 resource server configuration. As a rule, these beans should follow the default behavior otherwise
   configured by Spring Boot (see `BearerTokenAuthenticationEntryPoint` and `BearerTokenAccessDeniedHandler`).

   Example AuthenticationEntryPoint (WebMvc), see
   [LoggingBearerTokenAuthenticationEntryPoint.java](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter/src/main/java/ch/admin/bit/jeap/security/resource/log/LoggingBearerTokenAuthenticationEntryPoint.java):

   ```java
   package ch.admin.bit.jeap.security.resource.log;

   import ch.admin.bit.jeap.security.resource.configuration.JeapOauth2ResourceAuthenticationEntryPoint;
   import jakarta.servlet.http.HttpServletRequest;
   import jakarta.servlet.http.HttpServletResponse;
   import lombok.extern.slf4j.Slf4j;
   import org.springframework.security.core.AuthenticationException;
   import org.springframework.security.oauth2.server.resource.web.BearerTokenAuthenticationEntryPoint;

   @Slf4j
   public class LoggingBearerTokenAuthenticationEntryPoint implements JeapOauth2ResourceAuthenticationEntryPoint {

       private final BearerTokenAuthenticationEntryPoint bearerTokenAuthenticationEntryPoint = new BearerTokenAuthenticationEntryPoint();

       @Override
       public void commence(HttpServletRequest request, HttpServletResponse response, AuthenticationException authException) {
           log.info("Authentication failure on request path '{}' : '{}'.", request.getRequestURI(), authException.getMessage());
           bearerTokenAuthenticationEntryPoint.commence(request, response, authException);
       }

   }
   ```

   Example AccessDeniedHandler (WebMvc), see
   [LoggingBearerTokenAccessDeniedHandler.java](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter/src/main/java/ch/admin/bit/jeap/security/resource/log/LoggingBearerTokenAccessDeniedHandler.java):

   ```java
   package ch.admin.bit.jeap.security.resource.log;

   import ch.admin.bit.jeap.security.resource.configuration.JeapOauth2ResourceAccessDeniedHandler;
   import lombok.RequiredArgsConstructor;
   import lombok.extern.slf4j.Slf4j;
   import org.springframework.security.access.AccessDeniedException;
   import org.springframework.security.oauth2.server.resource.web.access.BearerTokenAccessDeniedHandler;

   import jakarta.servlet.http.HttpServletRequest;
   import jakarta.servlet.http.HttpServletResponse;

   @RequiredArgsConstructor
   @Slf4j
   public class LoggingBearerTokenAccessDeniedHandler implements JeapOauth2ResourceAccessDeniedHandler {

       private final BearerTokenAccessDeniedHandler bearerTokenAccessDeniedHandler = new BearerTokenAccessDeniedHandler();
       private final boolean debugEnabled;

       @Override
       public void handle(HttpServletRequest request, HttpServletResponse response, AccessDeniedException accessDeniedException) {
           if (!debugEnabled) {
               log.info("Access denied to request path '{}': '{}'.", request.getRequestURI(), accessDeniedException.getMessage());
           }
           else {
               log.debug("Access denied to request path '{}': '{}'. Authentication: '{}'.",
                       request.getRequestURI(), accessDeniedException.getMessage(), AuthenticationLogInfo.from(request.getUserPrincipal()));
           }
           bearerTokenAccessDeniedHandler.handle(request, response, accessDeniedException);
       }

   }
   ```

## Customize the MethodSecurityExpressionHandler

`jeap-spring-boot-security-starter` configures its own instance of the `MethodSecurityExpressionHandler`.

1. Provide a Spring bean implementing `JeapMethodSecurityExpressionHandlerCustomizer`. It is used by
   `jeap-spring-boot-security-starter` to customize its `MethodSecurityExpressionHandler` instance further, e.g. to
   register a custom permission evaluator.

   Example, see
   [MethodSecurityExpressionHandlerCustomizer.java](https://github.com/jme-admin-ch/jme-security-oauth2-example/blob/main/jme-security-oauth2-resource-authorities-service/src/main/java/ch/admin/bit/jeap/jme/security/oauth/resource/MethodSecurityExpressionHandlerCustomizer.java):

   ```java
   package ch.admin.bit.jeap.jme.security.oauth.resource;

   import ch.admin.bit.jeap.security.resource.configuration.JeapMethodSecurityExpressionHandlerCustomizer;
   import org.springframework.security.access.expression.method.DefaultMethodSecurityExpressionHandler;
   import org.springframework.security.access.expression.method.MethodSecurityExpressionHandler;
   import org.springframework.stereotype.Component;

   /**
    * Only needed for special cases when you have to customize the method security expression handler instantiated by
    * the jEAP security starter. Use e.g. to register a custom permission evaluator.
    */
   @Component
   public class MethodSecurityExpressionHandlerCustomizer implements JeapMethodSecurityExpressionHandlerCustomizer {
       @Override
       public MethodSecurityExpressionHandler customize(DefaultMethodSecurityExpressionHandler expressionHandler) {
           expressionHandler.setPermissionEvaluator(new ThingPermissionEvaluator());
           return expressionHandler;
       }
   }
   ```

## Related

- [Authentication and authorization for REST APIs](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authentication-and-authorization.md) — the configuration property reference and where authorization takes place in the REST layer.
- [How to: enable and debug jEAP token introspection](enable-and-debug-token-introspection.md)
