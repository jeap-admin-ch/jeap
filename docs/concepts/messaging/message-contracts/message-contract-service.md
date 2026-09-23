# Message Contract Service

> A Message Contract Service is only instantiated once per system group (a federal office, a larger program, a Solution Train, ...). It is not necessary to instantiate and operate a separate Message Contract Service for every business application!

The Message Contract Service manages so-called "[Message Contracts](index.md)", i.e. the message-type consumer/producer declarations of a microservice. These declare the message types that a specific version of the microservice consumes and/or produces on a topic.

```plantuml
@startuml
title Message Contract Service Context

left to right direction
skinparam shadowing false
skinparam componentStyle rectangle
skinparam packageStyle rectangle
skinparam defaultTextAlignment center

package "Message Contract Service" {
  component "Message Contract Service" as messageContractService
  component "Schema Validation" as schemaValidation
  component "Avro Schema Client" as avroSchemaClient
}

package "Business Application" {
  component "Application Service" as applicationService
}

database "Message Type Registry\n(Git Repo)" as messageTypeRegistry
database "Nexus Repository" as nexusRepository

note right of messageTypeRegistry
  Upload Messaging Contracts
end note

note bottom of applicationService
  Register Deployment / Can-I-Deploy
  Schema Compatibility Check
end note

note top of avroSchemaClient
  Retrieve Avro Schema for
  Message Type Version
end note

note bottom of nexusRepository
  Publish Message Type as JAR
end note

messageContractService --> messageTypeRegistry : upload / manage contracts
messageContractService --> avroSchemaClient : retrieve schema
avroSchemaClient --> messageTypeRegistry : get schema for version
schemaValidation --> messageTypeRegistry : compatibility check

applicationService ..> schemaValidation : register deployment / compatibility check
applicationService ..> messageContractService : use message contract
messageContractService ..> nexusRepository : publish message type JAR

@enduml
```

## Setting up a Message Contract Service instance

The Message Contract Service is a Spring Boot microservice based on the jEAP Microservices Blueprint, with a REST API protected by Basic Auth and a PostgreSQL database, without a frontend/UI.

The entire logic is provided as a library and can be instantiated in a dedicated project using `jeap-message-contract-service-instance` as the parent project, as follows:

**pom.xml**

```xml
...
	<parent>
        <groupId>ch.admin.bit.jeap</groupId>
        <artifactId>jeap-message-contract-service-instance</artifactId>
        <version>use-the-latest-version-here</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
...
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <mainClass>ch.admin.bit.jeap.messagecontract.web.MessageContractApplication</mainClass>
                </configuration>
            </plugin>
        </plugins>
    </build>
```

The following two properties must be set, and are best injected as a secret from Vault:

| Property | Purpose |
| --- | --- |
| `jeap.messagecontract.write-user.username` | Username for write operations on the REST API |
| `jeap.messagecontract.write-user.password` | Password for write operations on the REST API |

### GitHub MessageType Repository Configuration

MessageType repositories hosted on GitHub must be specially configured so that authentication can happen via a GitHub App. The properties for each configured repository must be defined as follows:

```yaml
messages:
  repositories:
    - uri: "https://github.com/.../some-message-type-registry.git"
      type: "GITHUB"
      parameters:
        GITHUB_APP_ID: "1303838"
        GITHUB_PRIVATE_KEY_PEM: "-----BEGIN RSA PRIVATE KEY-----..."
```

Each element in the list has the following properties:

| Property | Purpose |
| --- | --- |
| `messages.repositories[0].uri` | Repository URL |
| `messages.repositories[0].type` | Repository type — currently only `"GITHUB"` is supported |
| `messages.repositories[0].parameters` | A map with specific GitHub parameters for authentication: `GITHUB_APP_ID` (the GitHub App ID) and `GITHUB_PRIVATE_KEY_PEM` (the private key of the GitHub App) |

## REST API

See the Swagger UI for the Swagger documentation of the REST API.

### Contract API

| Operation | Resource | Purpose | Authentication |
| --- | --- | --- | --- |
| GET | `/api/contracts` | Lists all existing contracts | None |
| PUT | `/api/contracts/{appName}/{appVersion}` | Uploads new contracts | Basic Auth |
| DELETE | `/api/contracts/{appName}/{appVersion}` | Deletes an existing contract | Basic Auth |

Example response for `GET /api/contracts`:

```json
[
  {
    "appName": "my-app",
    "appVersion": "1.0.0",
    "messageType": "MyType",
    "messageTypeVersion": "2.0.0",
    "topic": "my-topic",
    "role": "CONSUMER",
    "registryUrl": "https://git/repo",
    "commitHash": "badcafe",
    "branch": "main",
    "compatibilityMode": "BACKWARD",
    "encryptionKeyId": "exampleKeyId"
  }, ...
]
```

Example request body for `PUT /api/contracts/{appName}/{appVersion}`:

```json
{
  "contracts": [
    {
      "messageType": "MyType",
      "messageTypeVersion": "2.0.0",
      "topic": "my-topic",
      "role": "CONSUMER",
      "registryUrl": "https://git/repo",
      "commitHash": "badcafe",
      "branch": "main",
      "compatibilityMode": "BACKWARD",
      "encryptionKeyId": "exampleKeyId"
    }, ...
  ]
}
```

Example request for `DELETE /api/contracts/{appName}/{appVersion}`:

```
/api/contracts/my-app/1.0.0?
messageType=MyType&
mesageTypeVersion=2.0.0&
topic=my-topic&
role=PRODUCER
```

See the Swagger UI for the Swagger definition of an instance of a Message Contract Service.

### Deployment API

| Operation | Resource | Purpose | Authentication |
| --- | --- | --- | --- |
| GET | `/api/deployments` | Lists all existing deployments | None |
| PUT | `/api/deployments/{appName}/{appVersion}/{environment}` | Uploads a new deployment | Basic Auth |
| GET | `/api/deployments/compatibility/{appName}/{appVersion}/{environment}` | Checks whether a planned deployment of an app version to an environment is compatible with the other consumers/producers of the same message type on the same topic (consumers are checked against producers and vice versa) | Basic Auth |

Example response for `GET /api/deployments`:

```json
[
  {
    "appName": "jme-buildpipeline-example",
    "appVersion": "0.0.1",
    "environment": "REF",
    "createdAt": "2022-10-07T16:01:22.235068+02:00"
  }, ...
]
```

The compatibility-check endpoint (`GET /api/deployments/compatibility/{appName}/{appVersion}/{environment}`) returns:

- **412 PRECONDITION FAILED**: the deployment cannot proceed — at least one messaging interaction is schema-incompatible
- **200 OK**: the deployment can proceed — all messaging interactions are schema-compatible

JSON response fields:

- `$.compatible`: `true` / `false`
- `$.message`: human-readable error message (e.g. for output in the build log)
- `$.interactions`: interactions between `<appName>` and consumers/producers of the same message type on the same topic
- `$.incompatibilities`: list of schema incompatibilities

Example:

```json
{
  "compatible": false,
  "interactions": [
    {
      "appName": "test-consumer-app",
      "appVersion": "1.0",
      "messageType": "ActivZoneEnteredEvent",
      "messageTypeVersion": "2.0.0",
      "topic": "test-topic",
      "role": "CONSUMER"
    }
  ],
  "incompatibilities": [
    {
      "interaction": {
        "appName": "test-consumer-app",
        "appVersion": "1.0",
        "messageType": "ActivZoneEnteredEvent",
        "messageTypeVersion": "2.0.0",
        "topic": "test-topic",
        "role": "CONSUMER"
      },
      "schemaIncompatibilities": [
        {
          "incompatibilityType": "NAME_MISMATCH",
          "message": "expected: ch.admin.bit.reference.ZoneReferences",
          "location": "/fields/3/type/name"
        },
        {
          "incompatibilityType": "READER_FIELD_MISSING_DEFAULT_VALUE",
          "message": "journeyActivationRequestReference",
          "location": "/fields/3/type/fields/0"
        },
        {
          "incompatibilityType": "NAME_MISMATCH",
          "message": "expected: ch.admin.bit.reference.ZonePayload",
          "location": "/fields/4/type/name"
        }
      ]
    }
  ],
  "message": "App test-consumer-app:1.0 is consuming incompatible message type ActivZoneEnteredEvent:2.0.0 on topic test-topic\n- NAME_MISMATCH at /fields/3/type/name: expected: ch.admin.bit.reference.ZoneReferences\n- READER_FIELD_MISSING_DEFAULT_VALUE at /fields/3/type/fields/0: journeyActivationRequestReference\n- NAME_MISMATCH at /fields/4/type/name: expected: ch.admin.bit.reference.ZonePayload"
}
```

See the Swagger UI for the Swagger definition of an instance of a Message Contract Service.

## Data Model

The data model is flat and consists of the following tables:

### MessageContract

This table contains the information for each producer/consumer contract, per app name/version:

| App Name | App Version | Message Type Name | Version | Role | Topic | Message Type Registry URL | Commit Hash | Branch | Compat. Mode | Message Type Schema as Avro Protocol JSON | encryptionKeyId |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| my-service-a | 1.0.0 | MyEventX | 1.5.2 | PRODUCES | my-event-x | git@... / https://... | 1abc123 | master | BACKWARD | `{ ... }` | exampleKey |
| my-service-b | 2.1.2 | MyCommandY | 2.0.2 | CONSUMES | my-command-y | git@.../ https://... | 435bcda | feature/foo | FORWARD | `{ ... }` | null |

- Commit hash and branch are optional; one of the two must be provided. The commit hash has higher precedence if known, as it is more precise.
- For the possible values of the compatibility mode, see [Confluent's schema-registry documentation](https://docs.confluent.io/platform/current/schema-registry/avro.html#compatibility-types).
- `encryptionKeyId` is optional; if present, it references the wrapping key used to encrypt the message type.

### Deployment

This table contains the information for each deployment, per app name/version and environment:

| App Name | App Version | Environment | Created at |
| --- | --- | --- | --- |
| my-service-a | 1.0.0 | ABN | 2022-10-07T16:01:22.235068+02:00 |
| my-service-b | 2.1.2 | PROD | 2022-10-07T16:01:22.235068+02:00 |

## Development

The jEAP Message Contract Service is developed in the [jeap-message-contract-service](https://github.com/jeap-admin-ch/jeap-message-contract-service) repository. See its [CHANGELOG](https://github.com/jeap-admin-ch/jeap-message-contract-service/blob/main/CHANGELOG.md) for release notes.

## See also

- [Message Contracts](index.md) — how a microservice declares what it consumes/produces.
- [Can-I-Deploy for Messaging](can-i-deploy-for-messaging.md) — the schema-compatibility check this service performs before a deployment.
- [Message Types](../message-types.md) — message-type fundamentals.
