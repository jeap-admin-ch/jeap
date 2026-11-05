# API Documentation with OpenAPI / Swagger

## Overview

OpenAPI (formerly also known as the Swagger Specification) is a standard for describing REST APIs. It started as part of the Swagger software project and has been an independent project since 2016. OpenAPI allows resources and operations of a REST API to be described using YAML or JSON, is easy to read, and has strong tooling support. The Blueprint Microservice uses the following tools:

- **Swagger UI** is an open-source web application that can visualize OpenAPI specifications. Operations can be invoked interactively directly from the UI. Swagger UI can be integrated easily into existing web applications. The Swagger ecosystem also contains additional tools for creating and managing OpenAPI specifications, but they are not used in the Blueprint Microservice.
- **springdoc-openapi** is a library from the Spring Boot ecosystem that automatically creates an OpenAPI specification from Spring REST controllers and OpenAPI annotations. It is the unofficial successor to SpringFox.

With OpenAPI, a service can define multiple interfaces. Each interface consists of tags, which contain the actual operations, and schemas, which describe the transferred data structures.

### Interface

An interface is a self-contained collection of operations and schemas. Each service must define at least one interface. Multiple interfaces per service make sense, for example, when:

- a service offers both an external and an internal interface. This makes it possible to create a dedicated OpenAPI specification for each, so the external interface can, for example, be offered through an API gateway.
- a service has several external interfaces for different user groups.
- a service has several versions of an API.

Dividing operations into interfaces only affects the OpenAPI documentation; it does not change technical reachability. In springdoc-openapi, interfaces can be created with a `GroupedOpenApi` bean. The following properties can be defined per interface (see the [Info object in the OpenAPI specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#infoObject)):

| OpenAPI object | Property | Description                                                                                                     | How to set in springdoc-openapi | Recommended usage                                                                                                           |
| --- | --- |-----------------------------------------------------------------------------------------------------------------| --- |-----------------------------------------------------------------------------------------------------------------------------|
| Info | `title` | The title or name of the interface                                                                              | Global in the `@OpenAPIDefinition` annotation; can be overridden per interface in `GroupedOpenApi`. | Set for every interface.                                                                                                    |
| Info | `description` | Description of the interface; may contain [CommonMark](https://spec.commonmark.org/) syntax                     | Global in the `@OpenAPIDefinition` annotation; can be overridden per interface in `GroupedOpenApi`. | Set for every interface.                                                                                                    |
| Info | `contact` | Contact details                                                                                                 | Global in the `@OpenAPIDefinition` annotation; can be overridden per interface in `GroupedOpenApi`. | Set this to the team maintaining the service. For external APIs, use an external contact address.                           |
| Info | `version` | The version of the interface                                                                                    | Global in the `@OpenAPIDefinition` annotation; can be overridden per interface in `GroupedOpenApi`. | Set for every interface. Use the format `v<N>`, analogous to [Evolution and Versioning of REST-APIs](evolution-versioning). |
| Info | `termsOfService` | URL with the terms under which this API may be used                                                             | Global in the `@OpenAPIDefinition` annotation; can be overridden per interface in `GroupedOpenApi`. | Usually not used in the Blueprint Microservice.                                                                             |
| Info | `license` | License under which this API may be used                                                                         | Global in the `@OpenAPIDefinition` annotation; can be overridden per interface in `GroupedOpenApi`. | Usually not used in the Blueprint Microservice.                                                                             |
| SecurityRequirements | — | Required authentications. For [Authentication for REST APIs](../authentication-and-authorization/protecting-rest-apis/index.md), a security requirement named `oauth` is predefined. | Global in the `@OpenAPIDefinition` annotation; can be overridden per interface in `GroupedOpenApi`. Additional authentication schemes can be defined with a `@SecurityRequirement` annotation. | Use whenever an operation is protected by OAuth; it may also be used for other authentication mechanisms.                   |
| ExternalDocumentation | — | Link to documentation                                                                                           | Global in the `@OpenAPIDefinition` annotation; can be overridden per interface in `GroupedOpenApi`. | Point to interface documentation, for example on Confluence. For external APIs, use external documentation.                 |
| Server | — | List of servers implementing the interface                                                                      | Global in the `@OpenAPIDefinition` annotation; can be overridden per interface in `GroupedOpenApi`. | Usually not used in the Blueprint Microservice.                                                                             |
| Extension | — | Proprietary extensions                                                                                          | Global in the `@OpenAPIDefinition` annotation; can be overridden per interface in `GroupedOpenApi`. | Usually not used in the Blueprint Microservice.                                                                             |

Example of an OpenAPI definition:

```java
@OpenAPIDefinition(
        info = @Info(
                title = "JME Swagger Example for an internal API",
                description = "An example how to integrate swagger into jEAP microservice blueprint",
                contact = @Contact(
                        email = "jEAP-Community@bit.admin.ch",
                        name = "jEAP",
                        url = "https://github.com/jeap-admin-ch/"
                ),
                version = "v1"
        ),
        security = {@SecurityRequirement(name = "OIDC")},
        externalDocs = @ExternalDocumentation(
			url = "https://github.com/jeap-admin-ch",
			description = "Documentation in Blueprint Microservice")
)
```


### Tags

Each interface can be divided into tags. A tag can, for example, represent:

- a resource.
- a version of a resource.
- a sub-resource.

By default, springdoc-openapi creates one tag per Spring Boot controller. Additional tags can be created with additional `@Tag` annotations. The following properties can be defined per tag (see the [Tag object in the OpenAPI specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#tagObject)):

| Property | Description | How to set in springdoc-openapi | Recommended usage |
| --- | --- | --- | --- |
| `name` | Name of the tag | By default, the bean name; it can be overridden in the `@Tag` annotation. | You may override it if the class name is too technical, but it should retain a clear relationship to the class name. |
| `description` | Short description | In the `@Tag` annotation | Use it when the tag name is not self-explanatory. |
| `externalDocs` | Reference to external documentation | In the `@Tag` annotation | If additional documentation is available, link it here. For external APIs, use external documentation. |

Example of a `@Tag` annotation:

```java
@Tag(
	description = "Exchange Messages with a Server. This version of the interface is deprecated, please use V2 instead",
	externalDocs = @ExternalDocumentation(url = "https://github.com/jeap-admin-ch",
			description = "Documentation in Blueprint Microservice"))
```


### Operations

Each tag provides a set of operations. An operation corresponds to a function with an HTTP verb, a path, parameters, and defined return values. The following properties can be defined per operation (see the [Operation object in the OpenAPI specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#operationObject)):

| Property | Description | How to set in springdoc-openapi | Recommended usage                                                                                                                                                                   |
| --- | --- | --- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `tags` | List of tags to which the operation belongs | Automatically the tag of the class; can be overridden in the `@Operation` annotation. | Do not override it; it is better to move functions into the correct class.                                                                                                          |
| `summary` | Short summary of the operation | In the `@Operation` annotation | Set it whenever useful; it may be omitted if the HTTP verb and path are self-explanatory.                                                                                           |
| `description` | Description of the operation; may contain [CommonMark](https://spec.commonmark.org/) syntax | In the `@Operation` annotation | Usually not necessary.                                                                                                                                                              |
| `externalDocs` | Link to external documentation | In the `@Operation` annotation | If additional documentation is available, link it here. For external APIs, use external documentation.                                                                              |
| `operationId` | Unique ID of the operation | Generated automatically; can be overridden in the `@Operation` annotation. | Do not override it.                                                                                                                                                                 |
| `parameters` | List of parameters with name, location (`query` or `path`), and schema | Generated from the function parameters; can be extended in the `@Operation` annotation. | Document it manually when the parameter name is not self-explanatory.                                                                                                               |
| `requestBody` | Expected request body of the operation, including schema | Generated from the function parameters; can be extended in the `@Operation` annotation. | Set it manually when the body is not self-explanatory.                                                                                                                              |
| `responses` | Return values the function may produce | In the `@Operation` annotation | Document it when special return codes are used. Standard return codes such as 200, 400, 401, and 403 do not need to be mentioned explicitly; for a 404, explain what was not found. |
| `callbacks` | List of out-of-band callbacks of the operation | In the `@Operation` annotation | Usually not used in the Blueprint Microservice. For asynchronous communication, use [Messaging](../messaging).                                                                      |
| `deprecated` | Whether the operation is deprecated and should no longer be used | Set when an `@Deprecated` annotation is present | Prefer setting it through `@Deprecated` annotations.                                                                                                                                |
| `security` | Security requirements of the interface can be overridden per operation | In the `@Operation` annotation | Use only when different security requirements apply per operation; normally this should not be necessary.                                                                           |
| `servers` | Server list of the interface can be overridden per operation | In the `@Operation` annotation | Usually not used in the Blueprint Microservice.                                                                                                                                     |

Example of an `@Operation` annotation:

```java
@Operation(
        summary = "Get a single message from the server",
        responses = {
                @ApiResponse(responseCode = "200"),
                @ApiResponse(responseCode = "404", description = "No message with this ID exist")}
)
```


### Schemas

Objects passed as request or response bodies are stored in the interface as OpenAPI schemas. These schemas are generated automatically, but can be extended with `@Schema` annotations. These annotations can be placed on a class as well as on individual fields. The OpenAPI schema is an extension of the JSON schema, and all properties available there can also be used in an OpenAPI schema. For a complete list, see the [Schema object in the OpenAPI specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#schemaObject). The most commonly used properties are:

| Property | Description | How to set in springdoc-openapi | Recommended usage |
| --- | --- | --- | --- |
| `required` | Whether the field is required; the default is `false` | In the `@Schema` annotation | Set it when a field is required. |
| `description` | Description of the field; may contain [CommonMark](https://spec.commonmark.org/) syntax | In the `@Schema` annotation | Set it when the meaning is not obvious. |
| `readOnly` | Marks a field as read-only, meaning it is set in the response but cannot be changed in a request | In the `@Schema` annotation | Set it when this is not obvious. |
| `writeOnly` | Marks a field as write-only, meaning it is not returned in the response but can be changed in a request | In the `@Schema` annotation | Set it when this is not obvious. |
| `externalDocs` | Link to external documentation | In the `@Schema` annotation | If additional documentation is available, link it here. For external APIs, use external documentation. |
| `example` | Example of how the value should be provided | In the `@Schema` annotation | Set it when the value is not obvious. |
| `deprecated` | Whether the schema is deprecated and should no longer be used | In the `@Schema` annotation | Set it when a field should no longer be used. |

Example of a schema definition:

```java
@Schema(deprecated = true)
public class MessageDto {
	@Schema(
		description = "The message ID", 
		readOnly = true, 
		example = "3fa85f64-5717-4562-b3fc-2c963f66afa6")
	private UUID id;

	@Schema(
		required = true, 
		description = "The message content", 
		example ="Hello World")
	private String text;

	@Schema(
		required = true,
		description = "The SAP-ID of the receiving business partner",
		example = "12345")
	private String receiver;

	@Schema(
        description = "The time when this message was sent. Will be set by the server",
		readOnly = true,
		example = "2020-04-23T14:50:05.648291+02:00")
	private ZonedDateTime timeSend;
}
```


## Integration

With the `jeap-spring-boot-swagger` starter, OpenAPI / Swagger can be integrated into your own application: it brings the required dependencies for springdoc-openapi and Swagger UI, configures Spring Security so Swagger UI can be public or protected with Basic Auth, and configures Swagger UI so REST APIs with authentication can also be used interactively.

**See [How to: document a REST API with OpenAPI](../../how-tos/rest-apis-and-web/document-a-rest-api-with-openapi.md)** for the setup steps: adding the starter dependency, declaring the `@OpenAPIDefinition` and `GroupedOpenApi` beans, documenting operations and schemas with annotations, and enabling interactive calls with authentication.

## Example

The [jme-swagger-example](https://github.com/jme-admin-ch/jme-swagger-example) documents a simple REST interface with OpenAPI.

## Further documentation

- [OpenAPI, Wikipedia](https://de.wikipedia.org/wiki/OpenAPI)
- [OpenAPI Initiative](https://www.openapis.org/)
- [OpenAPI 3.0 Specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md)
- [Swagger Website](https://swagger.io/)
- [springdoc-openapi Website](https://springdoc.org/)
