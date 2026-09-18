# Can-I-Deploy for Messaging

By Can-I-Deploy we mean the automatic **check of the prerequisites for a deployment to an environment**. This prevents a component from being deployed that is not compatible with the components already installed on that environment. This page describes what Can-I-Deploy means for messaging specifically — i.e. the schema-compatibility check of a message schema against an environment.

![Introduction: producer and consumer versions exchanging messages over a topic, with a can-I-deploy check gating deployment](intro-can-i-deploy.png)

## What does Can-I-Deploy mean for messages?

Can-I-Deploy means, for messaging:

- Reader schema *"can-read"* writer schema
    - The **consumer (reader schema)** can **read the Avro record written** by the **producer (writer schema)**
    - This means the producer either uses the same schema, or one that is compatible with the reader schema — e.g. that all mandatory fields in the reader schema are also written by the writer.
    - Details: see [Evolution of Messages](../evolution-of-messages/index.md) (how it works)

```plantuml
@startuml
skinparam linetype ortho
skinparam nodesep 40
skinparam ranksep 30
skinparam rectangle {
  BorderColor Black
}
skinparam component {
  BorderColor Black
}
rectangle "Producer" as n0
rectangle "Consumer" as n2
rectangle "Writer\nSchema" as n4
rectangle "Reader\nSchema" as n5
rectangle "Topic" as n1
rectangle "Can-I-Deploy:\n'Reader Schema' can-read 'Writer Schema'" as n3

n0 --> n1
n1 --> n2
n3 -[dashed]-> n4
n3 -[dashed]-> n5

n0 -[hidden]-> n2
n2 -[hidden]-> n4
n4 -[hidden]-> n5
n5 -[hidden]-> n1
n1 -[hidden]-> n3
@enduml
```

The prerequisites for this are:

- The Message Contract is known (consumer / producer / type version / topic — see [Message Contracts](index.md))
    - **Consumer and producer can be matched via the topic**
    - **The producer's and consumer's schemas are known**

## How does the can-I-deploy check work?

### Schematic flow of declaring/checking Message Contracts and can-I-deploy checks

To perform a can-I-deploy check for a message consumer/producer (jEAP microservice):

1. The [Message Contracts](index.md) of the microservice version must be declared
2. The Message Contracts must be uploaded to the [Message Contract Service](message-contract-service.md) during the build
3. A can-I-deploy check (schema compatibility check) must be performed via the [Message Contract Service](message-contract-service.md) before the deployment
4. The deployment of the microservice version must be recorded on the [Message Contract Service](message-contract-service.md) by the deployment pipeline

![Full flow from message-type definition and contract declaration, through build-time upload and can-I-deploy checks, to deployment recording](messaging-contract-flow.png)

## See also

- [Message Contracts](index.md) — what a Message Contract declares and how it is created.
- [Message Contract Service](message-contract-service.md) — where Message Contracts and deployments are recorded, and can-I-deploy checks are performed.
- [Evolution of Messages](../evolution-of-messages/index.md) — how Avro schema compatibility/evolution works.
