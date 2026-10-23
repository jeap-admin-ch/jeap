# Message Contract Service

> A Message Contract Service is only instantiated once per system group (a federal office, a larger program, a Solution Train, ...). It is not necessary to instantiate and operate a separate Message Contract Service for every business application!

The Message Contract Service manages so-called "[Message Contracts](index.md)", i.e. the message-type consumer/producer declarations of a microservice. These declare the message types that a specific version of the microservice consumes and/or produces on a topic.

## Development

The jEAP Message Contract Service is developed in the [jeap-message-contract-service](https://github.com/jeap-admin-ch/jeap-message-contract-service) repository. See its [CHANGELOG](https://github.com/jeap-admin-ch/jeap-message-contract-service/blob/main/CHANGELOG.md) for release notes.

## See also
- [Service documentation](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-message-contract-service/)
- [Message Contracts](index.md) — how a microservice declares what it consumes/produces.
- [Can-I-Deploy for Messaging](can-i-deploy-for-messaging.md) — the schema-compatibility check this service performs before a deployment.
- [Message Types](../message-types.md) — message-type fundamentals.
