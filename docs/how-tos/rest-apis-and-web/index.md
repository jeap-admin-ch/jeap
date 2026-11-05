# How-Tos: REST APIs & Web

Building and publishing HTTP APIs, frontend integration, and real-time updates to the browser.

## HTTP APIs

- [Enable HTTP compression](../../concepts/rest-apis/http-compression.md) for a Spring Boot server and its REST clients.
- [Document a REST API with OpenAPI](document-a-rest-api-with-openapi.md) — add the swagger starter, declare interfaces as `GroupedOpenApi` beans, and document operations/schemas with annotations.
- [Publish an OpenAPI spec to the Architecture Repository](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-open-api-publisher-starter/getting-started) — add the starter, enable publishing, configure OAuth2.

## Frontend integration

- [Enable and customize the current-user endpoint](enable-and-customize-current-user-endpoint.md) — expose token claims to a frontend as JSON, with a custom DTO/customizer if needed.
- [Handle direct frontend route navigation in Spring Boot SCS](handle-direct-frontend-route-navigation.md) — fix 404s on a bookmarked/external direct link into a single-page application's own routing.

## Real-time updates

- [Push resource-change events to the browser](https://jeap-admin-ch.github.io/docs/building-blocks/libraries/jeap-server-sent-events/getting-started) and subscribe to them, via Server-Sent Events.
