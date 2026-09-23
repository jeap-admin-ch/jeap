# Versioning of Business Objects

## Overview

Business objects can change over the course of their lifecycle. Accordingly, when accessing a business object, it is important to know which version is being referred to, depending on the situation. This can be the case, for example, with:

- Event notification: asynchronous notification about a business object referring to a specific version
  - For example, referring to the initial state of the object in an ObjectCreatedEvent vs. referring to a modified state in an ObjectModifiedEvent
- Access via a synchronous REST API to a specific version of a business object
  - For example, as a reaction to an event notification
- Storage, filing, or archiving of a specific version of a business object

:::info
In this context, the term "version" refers to the business lifecycle of the business object, not to its form or schema.
:::

## Versioning

- Not all business objects are mutable, and not all business objects require versioning from a business perspective. **Versioning should therefore only be used when it is required for business reasons.**
- **When designing APIs and messages, it must be defined whether versioning of the business objects is necessary.**
- Every change to a business object results in a new version of the business object.
  - **Versions must be modeled as a monotonically incrementing integer with a base of 1.**
  - No semantic versioning!
- Versioning usually applies to the entire business object.
  - The aggregate root / transaction boundary is typically the business object as a whole.
  - Versioning of sub-objects / sub-resources is not normally expected. It can be deviated from for specific business requirements.

## Technical Implementation

### Querying Versioned Business Objects via REST APIs

A specific version of a business object is referenced using the `version` query parameter. If this query parameter is missing, it is assumed that the current version of the business object is being referenced.

```java
/swimrings/<id>?version=2                        // Version of the resource is specified
/swimrings/<id>                                  // Version missing -> current version is referenced
/swimrings/<id>/factory?version=2                // Version refers to the root resource (= aggregate root)
/swimrings/<id>/valve?version=2&valveVersion=3   // Version refers to the root resource (= aggregate root), valveVersion to the version of the sub-resource (exception case)
```

### Referencing Versioned Business Objects in Messages (Events, Commands)

See also Message Types for the general structure of messages.

```js
record SwimringReference {
  string type = "Swimring";
  string id;   // Business object identifier
  int version; // Business object version
}
```

### Versioning of Business Objects When Stored in Object Storage Backends (S3-Compatible)

S3 can automatically version objects when they are stored and generates a long technical ID for each version of an object. Versioning can be switched on at the bucket level; it is disabled by default. Versioning must be enabled when it is required from a business perspective.

- The technical S3 version ID of an object (a 1024-bit string) **must be mapped by the application to a business version number** (1, 2, 3, ...).
- **When communicating via APIs and messages, the business version number must be used to reference a business object.**
- The business version number must be stored in the S3 object metadata under the key `version`:

```java
ObjectMetadata metadata = new ObjectMetadata();
metadata.addUserMetadata("version", String.valueOf(businessObjectVersion));
```

See also:

- Basics of versioning on S3: [https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)
- Creating a bucket with versioning: [https://docs.aws.amazon.com/AmazonS3/latest/userguide/manage-versioning-examples.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/manage-versioning-examples.html)
- Uploading objects with metadata: [https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html)

### Entity Version with JPA/Hibernate as Business Object Version

If a field annotated with `@Version` is used in JPA/Hibernate as the version of a business object, the field must be initialized with 1, so that versioning does not start at 0 (cf. the requirement that "the version number is an integer with a base of 1").

## Further Documentation

- Styleguide and Naming Convention for REST APIs
- Message Types
