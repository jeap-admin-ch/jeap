# Evolution and Versioning of REST-APIs

## Overview

REST APIs change over the course of an application's lifecycle, which can lead to incompatibilities between providers and consumers of an interface. When a consumer and a provider have to update an interface at the same time, these two services have a **deployment dependency**, since they are no longer independently deployable. To prevent this, only **backwards-compatible** changes should be made whenever possible. If this is not possible, it may be necessary to support several API variants for a certain period. This requires **versioning** of the interface.

## Evolution Strategies for APIs

When evolving APIs, the Blueprint Microservice follows the principle "evolve when possible, version when necessary". [Consumer Driven Contract Tests with Pact](todo) are used to ensure compatibility between consumer and provider. As long as all contracts are fulfilled, a REST API can be evolved freely. This means that even non-backwards-compatible changes can be carried out in two compatible steps (Expand / Migrate / Contract strategy, or parallel change strategy, see also [martinfowler.com](https://martinfowler.com/bliki/ParallelChange.html)). For example, if the return type of a field needs to change, this can be done as follows:

- First, the existing interface is extended with a new return field of the new type, while the old field continues to be returned as well. Since all contracts are still fulfilled, this is a backwards-compatible change (**Expand**).
- Then the consumers are adapted so that they only read the new field (**Migrate**). Consumers can be migrated independently of each other.
- Once all consumers have migrated, the old return field can be removed. Since it is no longer used in the new contracts, this is again a backwards-compatible change (**Contract**).

This is not always possible, however, and requires increased communication effort between consumer and producer. If this is not possible, an Expand / Migrate / Contract strategy with versioning must be used as a fallback:

- First, a new version of the API is implemented in the provider (**Expand**). The old version is still supported so all consumers keep working.
- Then the consumers are adapted so that they use the new version of the interface (**Migrate**). Consumers can be migrated independently of each other.
- Once all consumers have migrated, the old interface can be removed from the provider (**Contract**).

Different types of APIs impose different requirements on versioning:

| Type | Coupled Internal APIs | Independent Internal APIs                                                                                                         | Cross-Application APIs                                                                 | Public APIs |
|---|---|-----------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|---|
| **Description** | REST API between two components of a business application that are deployed together | REST API between two or more components of a business application that are not deployed together                                  | REST API between two or more components of different business applications             | REST API called by third-party systems |
| **Example** | API of a backend-for-frontend called by the Angular frontend | API provided to other microservices of the same business application                                                              | API provided to other applications                                                     | API for partners called through the API gateway |
| **Lifecycle** | Consumer and provider are always deployed together | Consumer and provider are developed together but usually not deployed together                                                    | Consumer and provider are neither developed nor deployed together                      | No influence on the lifecycle of the partner applications |
| **Communication paths** | Short | Short                                                                                                                             | Medium (needs e.g. coordination at PI planning)                                        | Long |
| **Ensuring compatibility** | By the team | [Consumer Driven Contract Tests with Pact](todo)                                                                                  | [Consumer Driven Contract Tests with Pact](todo)                                       | Must be defined case by case, e.g. by a specification |
| **Changes** | Can be changed freely | Usually through evolution. If non-backwards-compatible changes are made and downtime is not possible, use Expand/Migrate/Contract | Evolution possible as long as contracts are honored, otherwise Expand/Migrate/Contract | Must be defined case by case by the application |
| **Versioning** | Not necessary | Only if you want to decouple deployments                                                                                          | Necessary if contracts are not honored                                                 | Usually necessary |

## Responsibility of API Consumers

For this to work, consumers of an API must follow these rules:

- API consumers must be built robustly ("Be conservative in what you send, be liberal in what you accept", see also [Postel's Law](https://en.wikipedia.org/wiki/Robustness_principle)). Often, consumers are not interested in all fields of a response. In such cases, the consumer must not depend on fields it does not need.
- The [Consumer Driven Contract Tests with Pact](todo) must be complete. A consumer must be able to handle every response that lies within the contract.
- With global versioning of a producer API, only one version may be consumed at a time.
- When a consumed API is updated to a new version, it should be updated within a reasonable time frame (~1 PI).

## Versioning Methods

There are two methods for API versioning. By default, **versioning on resources** should be used, but for individual services **global versioning** can also be useful. Within a single service, however, the two methods must not be mixed.

| Type | Description | Example | Application |
|---|---|---|---|
| **Versioning on Resources** | Each resource has its own version. Publishing a new version of a resource has no effect on the other resources. If a resource is removed, the interface is marked as deprecated without introducing a new interface. | `/api/resource/v3`<br/>`/api/other/v2` | Less effort for a new version. If a resource changes, only that resource needs to be versioned. Should therefore be used whenever possible. |
| **Global Versioning** | The API has one version; every version contains all necessary resources. | `/api/v3/resource`<br/>`/api/v3/other` | When the resources themselves change between versions. |

In both cases, the following points apply:

- The version must be part of the path, for example `/api/myresource/v4`. Other options, such as the version as a query string or in the domain name, must not be used for internal APIs, and for public APIs only if otherwise specified.
- Versions must follow the scheme `v<N>`, where N is a simple, monotonically increasing version number, e.g. `/api/myresource/v3`, `/api/myresource/v4`, etc.
- Versioning should only be applied when necessary. For example, a `v1` is normally not necessary, but can be used if it is clear that further versions will be needed. As a rule, new APIs should have no version, e.g. `/api/myresource`, and only get one after the first change, e.g. `/api/myresource/v2`.
- When a new version becomes available, all necessary operations (and, in the case of global versioning, all resources) must be available in that version. Consumers must not use operations from different versions. For example, if only a POST operation is changed, all GET operations must still be present in the new version so that the old version can later be removed.

## Deprecation of Old Versions

> **Note:** In the future, this should be supported by the Spring Boot starter.

When a new version of an API is published, old API versions must be marked as `deprecated`. This allows existing consumers to migrate to the new interface. As a rule, consumers should migrate to the new version in the PI following the deprecation announcement, so that the provider can decommission the old interface in the PI after that.

An interface must be marked in the following ways:

- The `deprecated` flag must be set in the OpenAPI / Swagger documentation.
- The provider must set a [Sunset header](https://tools.ietf.org/html/rfc8594) in the HTTP response.
- The version must be set to `deprecated` in the Pact Broker for [Consumer Driven Contract Tests with Pact](todo).

## Implementation in Java

How the different URLs are managed in Java code is generally left to the applications; different strategies are needed depending on the use case. The following approaches can be useful:

- A dedicated controller should be created for each new version. This makes it easy to remove old versions later.
- Controllers of old versions can either call the controllers of the new versions or a common service. What should be avoided is the new version calling the old one, or versioning leaking into the service layer.
- DTO definitions that have not changed, or have changed only compatibly, can be shared between versions. In some cases, `FAIL_ON_UNKNOWN_PROPERTIES` may need to be set in the JSON deserializer for this.

## Example

> **TODO:** An example of API integration still needs to be created.

## Further Reading

- [Expand / Migrate / Contract Strategy, martinfowler.com](https://martinfowler.com/bliki/ParallelChange.html)
- [API Versioning Has No "Right Way", apisyouwonthate.com](https://apisyouwonthate.com/blog/api-versioning-has-no-right-way)
- [Roy Fielding on Versioning, Hypermedia, and REST, InnoQ](https://www.infoq.com/articles/roy-fielding-on-versioning/)
