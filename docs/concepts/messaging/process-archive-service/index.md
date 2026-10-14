# Process Archive Service

<a id="context-overview"></a>

## Purpose

The Process Archive Service (PAS) archives business data for traceability.

## How it works

A message triggers archiving:
the data is either included in the message or fetched from the responsible service through a REST API.
The PAS stores the data and its identifying metadata as an archived artifact in an S3-compatible store.

```mermaid
flowchart LR
    Services[Business microservices] -->|Trigger message| PAS[Process Archive Service]
    PAS -->|Fetch data if needed| Services
    PAS -->|Archive data and metadata| Store[(Archive storage)]
    PAS -->|Artifact notifications when enabled| Consumers[Interested services]
```

Archive types describe the data format and retention requirements. Versioning, retention and object
lock protect archived versions. PCS snapshots are one possible kind of archived data; the archive-reader
library supports retrieving artifacts later.

<a id="integration"></a><a id="example"></a><a id="detailed-documentation"></a><a id="context"></a><a id="runtime-view"></a><a id="see-also"></a><a id="configuration"></a><a id="pas-as-message-consumer"></a><a id="determining-the-data-to-archive"></a><a id="case-event-notification"></a><a id="case-event-carried-state-transfer"></a><a id="example-configuration"></a><a id="standardized-archive-data-rest-interface"></a><a id="transporting-archive-data-as-avro-over-rest-interfaces"></a><a id="archive-data-types-defined-via-avro-schema"></a><a id="schema-validation-in-the-pas"></a><a id="archive-data-types-defined-via-configuration"></a><a id="sharedarchivedartifactversioncreatedevent"></a><a id="archived-artifact-listener"></a><a id="publishing-archived-artifacts-via-feature-flag-from-pas-version-8140"></a><a id="integration-with-an-s3-object-store"></a><a id="connection"></a><a id="specific-configuration-for-aws-s3"></a><a id="requirements-for-the-s3-object-store-buckets"></a><a id="object-lock-and-ado-access-during-outage-with-dell-ecs"></a><a id="object-storage-strategy"></a><a id="default-object-storage-strategy"></a><a id="custom-object-storage-strategy"></a><a id="hash-provider"></a><a id="schema-storage-on-the-bucket"></a><a id="data-expiration-and-locking"></a><a id="example-of-the-expiration-of-a-versioned-object"></a><a id="creating-a-lifecycle-policy-on-the-bucket-by-the-pas"></a><a id="validating-that-the-lifecycle-for-an-object-expires"></a><a id="locking-and-expiration"></a><a id="encryption"></a><a id="storage-on-object-storage"></a><a id="encryption-key-definition-from-pas-version-6100"></a><a id="legacy-encryption-definition-hashicorp-vault-only"></a><a id="receiving-encrypted-kafka-records-with-jeap-messaging"></a><a id="metrics"></a><a id="development"></a>

## Documentation

- [Service documentation](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-process-archive-service/)
- [Getting started](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-process-archive-service/getting-started)
