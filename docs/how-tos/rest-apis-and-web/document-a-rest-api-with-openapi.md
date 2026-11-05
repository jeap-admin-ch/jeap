# How to: document a REST API with OpenAPI

With the `jeap-spring-boot-swagger` starter, OpenAPI / Swagger can be integrated into your own application:

- It brings the required dependencies for springdoc-openapi and Swagger UI.
- It configures Spring Security so Swagger UI can be public or protected with Basic Auth.
- It configures Swagger UI so REST APIs with authentication can also be used interactively. Both the [OAuth Mock Server](../../concepts/authentication-and-authorization/testing/oauth2-mock-server.md) and Keycloak can be integrated.

## Steps

1. Add the dependency for `jeap-spring-boot-swagger-starter`:

```xml
<!-- Spring MVC -->
<dependency>
	<groupId>ch.admin.bit.jeap</groupId>
	<artifactId>jeap-spring-boot-swagger-starter</artifactId>
</dependency>
```

2. Configure the starter through the normal application properties. The following settings are available:

| Property                                   | Description                                                                                                                                                                                                                                                                                                                                                            | Default           |
|--------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `jeap.swagger.enforceServerBaseHttps`      | If set to `true`, the base server URL is delivered to Swagger UI using HTTPS. This is typically set when the application runs behind a load balancer that requires HTTPS while the application itself is configured only with HTTP. For `localhost`, HTTPS is disabled automatically by the starter.                                                                   | `true`            |
| `jeap.swagger.status`                      | `OPEN`: access to Swagger without Basic Auth, for example for local or development deployments.<br/>`SECURED`: access to Swagger using Basic Auth if Swagger is needed in production, which is not recommended.<br/>`DISABLED`: Swagger UI is switched off, which is recommended for production environments.                                                          | `DISABLED`        |
| `jeap.swagger.secured.username`            | Basic Auth user name, only relevant when the status is `SECURED`                                                                                                                                                                                                                                                                                                       | `swagger`         |
| `jeap.swagger.secured.password`            | Basic Auth password, only relevant when the status is `SECURED`                                                                                                                                                                                                                                                                                                        | none              |
| `jeap.swagger.oauth.openIdConnectUrl`      | Optional URL of the OpenID configuration endpoint of the authentication server. By default, it is configured for both the mock server and Keycloak. If a dedicated URL is needed, it can be changed; see the example in [`jme-swagger-service`](https://github.com/jme-admin-ch/jme-swagger-example/blob/main/jme-swagger-service/src/main/resources/application.yml). | Mock and Keycloak |
| `springdoc.swagger-ui.oauth.client-id`     | Optional default client ID when [Authentication for REST APIs](../../concepts/authentication-and-authorization/protecting-rest-apis/index.md) is used                                                                                                                                                                                                                                                                           | none              |
| `springdoc.swagger-ui.oauth.client-secret` | Optional default client secret when [Authentication for REST APIs](../../concepts/authentication-and-authorization/protecting-rest-apis/index.md) is used                                                                                                                                                                                                                                                                       | none              |
| `springdoc.swagger-ui.oauth2-redirect-url` | With Spring MVC, the redirect URI does not need to be set.                                                                                                                                                                                                                                                                                                             | none              |

3. To configure Swagger, add an `@OpenAPIDefinition` annotation to a Spring `@Configuration` bean. This annotation defines properties that should apply to all interfaces. Example source: [SwaggerConfig.java](https://github.com/jme-admin-ch/jme-swagger-example/blob/main/jme-swagger-service/src/main/java/ch/admin/bit/jeap/jme/swagger/SwaggerConfig.java) in [jme-swagger-example](https://github.com/jme-admin-ch/jme-swagger-example).

```java
package ch.admin.bit.jeap.jme.swagger;

import io.swagger.v3.oas.annotations.ExternalDocumentation;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import org.springdoc.core.models.GroupedOpenApi;
import org.springframework.context.annotation.Configuration;

/**
 * Every service declares exactly one {@code @OpenAPIDefinition}. It holds the documentation that is common to all APIs
 * of the service: title, description, version, contact and a link to further documentation.
 * <p>
 * The APIs themselves are not declared here. For each API a service offers, a bean of type {@link GroupedOpenApi} is
 * created and Swagger UI then offers one selectable API definition per group. This example defines two of them, see
 * {@link ch.admin.bit.jeap.jme.swagger.messages.InternalApiSwaggerConfig} and
 * {@link ch.admin.bit.jeap.jme.swagger.external.ExternalApiSwaggerConfig}.
 * <p>
 * The security requirement refers to the security scheme named "OIDC" that the jEAP swagger starter registers as soon
 * as an authorization server is configured. Declaring it on the definition marks every operation of this service as
 * protected and makes the "Authorize" button of Swagger UI acquire a token from that authorization server.
 * <p>
 * <b>About {@code version}:</b> the OpenAPI specification requires it in every document, and it means the version of
 * the API this document describes as a whole - not the version of an individual operation. The messages API is at its
 * second major version, which is why {@code 2.0.0} is declared here; that the deprecated first version is still part
 * of the same document is visible in the paths and tags of the operations ({@code /api/messages} for V1,
 * {@code /api/messages/v2} for V2). An API that is versioned on a lifecycle of its own gets its own version through
 * its group, see {@link ch.admin.bit.jeap.jme.swagger.external.ExternalApiSwaggerConfig}.
 * <p>
 * See the <a href="https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-swagger-starter">jEAP
 * Swagger starter documentation</a> for the jEAP specific parts and <a href="https://springdoc.org">springdoc.org</a>
 * for the springdoc reference documentation.
 */
@OpenAPIDefinition(
        info = @Info(
                title = "JME Swagger Example",
                description = "An example of how to document REST APIs of a jEAP microservice with springdoc-openapi",
                version = "2.0.0",
                contact = @Contact(
                        email = "jeap-community@bit.admin.ch",
                        name = "jEAP Community",
                        url = "https://jeap-admin-ch.github.io/"
                )
        ),
        externalDocs = @ExternalDocumentation(
                url = "https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-swagger-starter",
                description = "jEAP Swagger starter documentation"),
        security = {@SecurityRequirement(name = "OIDC")}
)
@Configuration
public class SwaggerConfig {
}
```

4. For each interface that should be documented with OpenAPI, define a Spring bean of type `GroupedOpenApi`. There you can configure which classes or paths belong to the interface. Parts of the general `OpenAPIDefinition` can also be overridden. Example source: [InternalApiSwaggerConfig.java](https://github.com/jme-admin-ch/jme-swagger-example/blob/main/jme-swagger-service/src/main/java/ch/admin/bit/jeap/jme/swagger/messages/InternalApiSwaggerConfig.java) in [jme-swagger-example](https://github.com/jme-admin-ch/jme-swagger-example).

```java
package ch.admin.bit.jeap.jme.swagger.messages;

import org.springdoc.core.models.GroupedOpenApi;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Definition of the internal API, the API this service offers to other applications of the same system.
 * <p>
 * Every API of a service is declared as a bean of type {@link GroupedOpenApi}. The group name is what Swagger UI shows
 * in its API selection box and it is also part of the URL of the generated OpenAPI document
 * (<i>/api-docs/{group}</i>). Which controllers and operations belong to a group is selected with
 * {@code packagesToScan(...)}, {@code packagesToExclude(...)}, {@code pathsToMatch(...)} and
 * {@code pathsToExclude(...)}; the documentation of a group can be adjusted with
 * {@code addOpenApiCustomizer(...)} as shown in
 * {@link ch.admin.bit.jeap.jme.swagger.external.ExternalApiSwaggerConfig}.
 * <p>
 * This group scans this package and therefore contains both versions of the messages API, see
 * {@link ch.admin.bit.jeap.jme.swagger.messages.v1.InternalApiController} and
 * {@link ch.admin.bit.jeap.jme.swagger.messages.v2.InternalApi2Controller}.
 */
@SuppressWarnings("deprecation")
@Configuration
public class InternalApiSwaggerConfig {

    @Bean
    GroupedOpenApi internalApi() {
        return GroupedOpenApi.builder()
                .group("Messaging API")
                .pathsToMatch("/api/**")
                .packagesToScan(this.getClass().getPackageName())
                .build();
    }
}
```

5. Classes and operations that are part of the interface automatically become OpenAPI tags and operations. Paths, methods, parameters, and similar details are taken directly from the Spring definition. Additional documentation can be added with OpenAPI annotations — see the tag and operation property reference in [API Documentation with OpenAPI / Swagger](../../concepts/rest-apis/openapi-documentation.md). Example source: [InternalApi2Controller.java](https://github.com/jme-admin-ch/jme-swagger-example/blob/main/jme-swagger-service/src/main/java/ch/admin/bit/jeap/jme/swagger/messages/v2/InternalApi2Controller.java) in [jme-swagger-example](https://github.com/jme-admin-ch/jme-swagger-example).

```java
package ch.admin.bit.jeap.jme.swagger.messages.v2;

import ch.admin.bit.jeap.security.resource.semanticAuthentication.ServletSemanticAuthorization;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PostAuthorize;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.time.ZonedDateTime;
import java.util.LinkedList;
import java.util.List;
import java.util.Optional;

/**
 * The current version of the messages API. It is documented as a second tag of the same API definition as
 * {@link ch.admin.bit.jeap.jme.swagger.messages.v1.InternalApiController}, the deprecated first version. In V2 the ID
 * of a message can now be any string, which is an incompatible change and therefore results in a new API version.
 * <p>
 * NOTE: To keep the example small, the messages are kept in memory in the controller itself. A real service would
 * delegate to a service and a repository instead.
 */
@SuppressWarnings("deprecation")
@Tag(name = "Messages (V2)", description = "Exchange Messages with a Server. The ID of a message can now be any string")
@RestController
@RequestMapping("/api/messages/v2")
@RequiredArgsConstructor
public class InternalApi2Controller {
    private final ServletSemanticAuthorization jeapAuthorization;

    @Getter
    private final List<Message2Dto> messages = new LinkedList<>();

    @Operation(
            summary = "Create or update a message on the server",
            responses = {
                    @ApiResponse(responseCode = "201", description = "Message has been created"),
                    @ApiResponse(responseCode = "403", description = "The caller has no write right for the receiving business partner")}
    )
    @PutMapping("/{messageId}")
    @PreAuthorize("hasRoleForPartner('swagger','write',#incoming.receiver)")
    public ResponseEntity<Message2Dto> createOrUpdate(@PathVariable("messageId") String messageId, @RequestBody Message2Dto incoming) {
        Optional<Message2Dto> messageOpt = find(messageId);
        if (messageOpt.isPresent()) {
            Message2Dto message = messageOpt.get();
            message.setReceiver(incoming.getReceiver());
            message.setText(incoming.getText());
            return ResponseEntity.status(HttpStatus.CREATED).body(message);
        }

        //Time send is set by the server, not by the client
        incoming.setTimeSend(ZonedDateTime.now());
        //ID must be equal to the ID in the URL
        incoming.setId(messageId);
        messages.add(incoming);
        return ResponseEntity.status(HttpStatus.CREATED).body(incoming);
    }

    @Operation(
            summary = "Get all messages",
            responses = {
                    @ApiResponse(responseCode = "200", description = "The messages the caller is allowed to read"),
                    @ApiResponse(responseCode = "403", description = "The caller has no read right")}
    )
    @GetMapping
    @PreAuthorize("hasRole('swagger','read')")
    public List<Message2Dto> readAll(@RequestParam(required = false) String receiver) {
        return messages.stream()
                .filter(m -> receiver == null || receiver.equals(m.getReceiver()))
                .filter(m -> jeapAuthorization.hasRoleForPartner("swagger", "read", m.getReceiver()))
                .toList();
    }

    @Operation(
            summary = "Get a single message from the server",
            responses = {
                    @ApiResponse(responseCode = "200", description = "The message"),
                    @ApiResponse(responseCode = "403", description = "The caller has no read right for the business partner of this message"),
                    @ApiResponse(responseCode = "404", description = "No message with this ID exists")}
    )
    @GetMapping("/{messageId}")
    @PreAuthorize("hasRole('swagger','read')")
    @PostAuthorize("hasRoleForPartner('swagger','read',returnObject.receiver)")
    public Message2Dto readSingle(@PathVariable("messageId") String messageId) {
        return find(messageId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "No message with this ID exists"));
    }

    @Operation(
            summary = "Delete an existing message on the server",
            responses = {
                    @ApiResponse(responseCode = "200", description = "The message has been deleted"),
                    @ApiResponse(responseCode = "403", description = "The caller has no write right for the business partner of this message"),
                    @ApiResponse(responseCode = "404", description = "No message with this ID exists")
            })
    @DeleteMapping("/{messageId}")
    @PreAuthorize("hasRole('swagger','write')")
    public void delete(@PathVariable("messageId") String messageId) {
        Message2Dto message = find(messageId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "No message with this ID exists"));
        if (!jeapAuthorization.hasRoleForPartner("swagger", "write", message.getReceiver())) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN);
        }
        messages.remove(message);
    }

    private Optional<Message2Dto> find(String messageId) {
        return messages.stream()
                .filter(m -> m.getId().equals(messageId))
                .findFirst();
    }
}
```

6. DTO classes used as parameters or return values automatically become OpenAPI schema definitions. Additional documentation can be added with OpenAPI annotations — see the schema property reference in [API Documentation with OpenAPI / Swagger](../../concepts/rest-apis/openapi-documentation.md). Example source: [Message2Dto.java](https://github.com/jme-admin-ch/jme-swagger-example/blob/main/jme-swagger-service/src/main/java/ch/admin/bit/jeap/jme/swagger/messages/v2/Message2Dto.java) in [jme-swagger-example](https://github.com/jme-admin-ch/jme-swagger-example).

```java
package ch.admin.bit.jeap.jme.swagger.messages.v2;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.ZonedDateTime;

/**
 * The message of the current API version, where the ID can be any string.
 * <p>
 * Fields that the server sets are documented as read-only, so they are not part of the request body Swagger UI
 * pre-fills. Fields without an explicit required mode are optional, which is the default of {@code @Schema}.
 */
@Data
@NoArgsConstructor
@Builder
@AllArgsConstructor
public class Message2Dto {
    @Schema(description = "The message ID, can be any string but usually a UUID.",
            accessMode = Schema.AccessMode.READ_ONLY,
            example = "3fa85f64-5717-4562-b3fc-2c963f66afa6")
    private String id;
    @Schema(requiredMode = Schema.RequiredMode.REQUIRED, description = "The message content", example = "Hello World")
    private String text;
    @Schema(requiredMode = Schema.RequiredMode.REQUIRED, description = "The SAP-ID of the receiving business partner", example = "12345")
    private String receiver;
    @Schema(description = "The time when this message was sent. Will be set by the server",
            accessMode = Schema.AccessMode.READ_ONLY,
            example = "2020-04-23T14:50:05.648291+02:00")
    private ZonedDateTime timeSend;
}
```

7. To use an API with [Authentication for REST APIs](../../concepts/authentication-and-authorization/protecting-rest-apis/index.md) interactively in Swagger UI, a corresponding client must be created on the authentication server. In the mock server, such a client can be defined as follows:

```yaml
client-id: "jme-swagger-tester"
client-secret: "{noop}secret"
registered-redirect-uri: ["${service-url}swagger-ui/oauth2-redirect.html"]
bproles: ...
userroles: ...
```

In Keycloak, a corresponding Swagger UI client must be created as described under Configuration parameters: [Clients](../../concepts/authentication-and-authorization/testing/oauth2-mock-server.md).

## Related

- [API Documentation with OpenAPI / Swagger](../../concepts/rest-apis/openapi-documentation.md) — the OpenAPI object, tag, operation and schema property reference, and a link to the full `jme-swagger-example`.
