# Using UUIDs

## Overview

### Motivation for UUIDs

- Distributed systems, distributed creation of IDs without a central instance
- Event-driven architecture with asynchronous communication - IDs are often generated at the source for
  idempotency
- Horizontal scaling
- Independent of the DB technology
- Traceability, since the ID is known from the start
- More flexible processes, since the steps that generate an ID don't necessarily have to happen first

### What are properties of UUIDs?

- Can be created in a distributed way without access to a central instance
- Conditionally human-readable or communicable
- Size: 128 bits / 16 bytes per ID
- PostgreSQL: offers a specialized UUID data type

## When are UUIDs suitable?

- When there is a requirement for distributed generation of IDs without a central instance
  - e.g. for asynchronous communication, replication, for idempotency, ...
- Merging data from different stores/sources without ID conflicts
- No external indication of the structure of IDs / harder to guess (in contrast to e.g. a sequential
  customer ID or similar)
- For simple creation in application code without a DB roundtrip, for smaller data volumes

## When are UUIDs not suitable?

- As business IDs that must be used, written or communicated by end users
- As primary key for a very large number of rows
  - Indexes may not fit into memory and are unnecessarily large
  - Partitioning based on the primary key is not possible with Type 4 UUIDs (Java: `UUID.randomUUID()`) or
    Type 1 UUIDs (time-based, but fractions of a second come first and the year last, so not sequential)
  - Partitioning is improved with Type 7 UUIDs, since these are sorted chronologically, e.g.:

    ```java
    <dependency>
      <groupId>com.fasterxml.uuid</groupId>
      <artifactId>java-uuid-generator</artifactId>
    </dependency>

    UUID timeBasedUuid = Generators.timeBasedEpochGenerator().generate()
    ```

  - The problem is accentuated with JOINs across multiple tables, which are then all linked via UUID
- As primary keys that are only used within the context of a single microservice, and therefore don't need
  the benefits of distributed creation
  - Exception: only small amounts of data need to be managed
- In general, technical primary keys should not be used externally for reasons of decoupling from internal
  details/data structures (regardless of whether UUIDs are used)

## UUID externally, efficient ID internally

If IDs must be created in a distributed way, they can be kept as a secondary key on a record. For requests
from external systems, the UUID is used to identify the record; internally, integer keys are used for
database access. This allows both distributed ID generation and efficient access for larger data volumes
within the microservice.

## UUIDs in PostgreSQL

PostgreSQL offers its own
[native UUID data type](https://www.postgresql.org/docs/current/datatype-uuid.html) for UUIDs. This should
be used. **In particular, UUIDs should not be stored as VARCHAR.**

## Further documentation

- [https://www.postgresql.org/docs/current/datatype-uuid.html](https://www.postgresql.org/docs/current/datatype-uuid.html)
- [https://blog.codinghorror.com/primary-keys-ids-versus-guids/](https://blog.codinghorror.com/primary-keys-ids-versus-guids/)
