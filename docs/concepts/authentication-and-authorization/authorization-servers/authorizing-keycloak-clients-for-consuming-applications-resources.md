# Authorizing Keycloak clients for consuming application resources

In the system context, the permissions of a consumer are defined in Keycloak. This is roughly illustrated below.

- The provider (business application Bar) creates a realm for the business application Bar in Keycloak.
- The provider creates clients (C1 .. C4) in its realm.
- The provider authorizes the clients according to the [role concept](../role-concept.md) by adding
  **Service Account Roles** to the Keycloak client.
- The consumers obtain an access token from Keycloak that contains the roles defined in the Keycloak client.

![Shared Keycloak clients: business applications Foo (x-, y- and z-service) and Pip (v-service) access the resource res of provider Bar's a-service with read or create and read permissions; Bar's realm in Keycloak holds the clients Foo-readonly (C1), Foo-readwrite (C2), Pip (C3) and Bar (C4) with their bar_@res_#read and bar_@res_#create roles](images/keycloak-clients-shared-keycloak-client.svg)

- x-service and y-service belong to the same business application Foo and require the same permissions → both can
  use the Keycloak client C1.
- z-service also belongs to the business application Foo, but requires more rights than x-service and y-service →
  needs a different Keycloak client C2.
- v-service belongs to the business application Pip → needs its own Keycloak client C3.
- b-service belongs to the business application Bar → needs its own Keycloak client C4.

## Considerations and Recommendations

- We authorize business applications, not microservices, because the provider does not need to know how the
  consuming business application is structured.
  - Refactoring the consuming business application does not change the permissions.
  - A client can be used by several microservices of the consuming business application if they need exactly the
    same rights.
  - If needed, the calling microservice can be identified through the trace ID
    ([Distributed tracing](../../logging/distributed-tracing.md)).
- Each microservice gets only the rights that it needs to perform its tasks, following the
  ([principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)).
  - This can mean that a business application may require several Keycloak clients with different permissions.

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Role concept in the Blueprint Microservice](../role-concept.md) — the roles assigned to a client as service account roles.
- [Keycloak](keycloak.md) — configuring realms, clients and service account roles in Keycloak.
- [Naming conventions](../../naming-conventions.md) — naming of Keycloak clients.
- [Calling secured REST APIs from Java](../calling-secured-rest-apis-from-java.md) — obtaining a token with a Keycloak client from a consuming microservice.
