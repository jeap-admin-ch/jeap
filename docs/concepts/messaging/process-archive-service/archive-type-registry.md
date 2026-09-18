# Archive Type Registry

## Overview

The Process Archive Service supports arbitrary **transport formats** for archive data. **Using Avro as the format is
recommended**. The Archive Type Registry acts as a **schema repository** and is
organized as a **structured Git repository**. Schemas for archive data are managed in it and, **once published, are
protected against changes** to ensure that the data can still be read in the future.

Using Avro has several advantages:

- Java bindings can be generated
- The Archive Type Registry manages schemas for archive data in a structured way
- PAS can validate data to be archived against the schema when it is stored, ensuring that the data can be read back
  later

## Archive Type Registry

The Archive Type Registry is:

- A separate Git repository
- Maintained directly by the business teams for their own archive types
- Immutable once an archive type has been published — published archive types can no longer be changed
- Consistency-checked to ensure the registry's conventions are followed:
    - A dedicated Archive-Type-Registry Maven plugin checks the registry on every build
    - Only builds that pass this check can be merged to master

### Registry layout

- `schema` (JSON schema for the descriptor; can be selected as a schema in IntelliJ when editing the descriptor, which
  then gives you IDE validation and code completion)
- `archive-types`
    - `_common` (global Avro definitions shared by all business systems)
    - `<business system>` (archive types per business system)
        - `_common` (Avro definitions shared within the business system)
        - `<archive-type>` (one archive type per kind of business data to archive)
            - `archive-type.json` (descriptor for the archive type: name, description, schema versions)
            - `<archive-type>_v1.avdl` (schema for version 1)
            - `<archive-type>_v2.avdl` (schema for version 2)

See [jme-archive-type-registry](https://github.com/jme-admin-ch/jme-archive-type-registry)
for an example of an Archive Type Registry.

#### Addressing archive types

Business data — and therefore archive types — should be definable independently by each business system, i.e. archive
type names are only unique within a single business system. To unambiguously map an archived record to a schema in the
Archive Type Registry, this must be done via the coordinates (business system name, archive type name, version).

## Defining an archive type

The descriptor defines the following properties:

- Name of the type
- System name
- Reference to the ID type
- Description
- Documentation link
- Encryption key reference (optional; needed if the data must be stored encrypted in S3)
- Schema versions

Example descriptor:

```js
{
  "archiveType": "Decree",
  "system": "JME",
  "referenceIdType": "ch.admin.bit.jeap.audit.type.JmeDecreeArchive",
  "description": "archive type example for a decree",
  "documentationUrl": "https://foo/bar",
  "expirationDays": 90,
  // Optional encryption key, define only if data should be encrypted
  "encryptionKey" : {
    "keyId": "my-archive-data-key" // Name of key in the  jEAP Cypto configuration of the PAS, which will then point to a key in a Key Management System (Vault, AWS KMS, ...)
  },
  // Legacy way of defining encryption, cannot be combined with encryptionKey at the same time:
  "encryption" : {
    "secretEnginePath": "transit/jme",
    "keyName": "jme-process-archive-example-s3-key"
  },
  "versions": [
  {
    "version": 1,
    "schema": "Decree_v1.avdl"
  },
  {
    "version": 2,
    "schema": "Decree_v2.avdl",
    "compatibilityMode": "BACKWARD"  // BACKWARD, FORWARD, FULL or NONE (see https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html)
   },
  {
    "version": 3,
    "schema": "Decree_v3.avdl",
    "compatibilityMode": "BACKWARD"  // BACKWARD, FORWARD, FULL or NONE (see https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html)
    "compatibleVersion": 1           // optional, can be specified if required. By default, the previous version is checked for compatibility.
  }
  ]
}
```

A single schema version can be described using an Avro protocol definition:

:::info
By (validated) convention, the archive type's root schema is expected to contain a record with the same name as the
archive type (e.g. `"archiveType":"Decree"` → there must be a record named `Decree`).

It is also validated that each schema version uses its own namespace. Otherwise, the generated Java classes would
collide when Java bindings are generated, and a system would not be able to process several versions of an archive
type at the same time.
:::

Example of an Avro protocol for an archive type:

```js
@namespace("ch.admin.bit.jeap.processarchive.test.decree.v3")
protocol DecreeProtocol {

  import idl "ch.admin.bit.jeap.processarchive.test.DecreeReference.avdl";

  record Decree {
    ch.admin.bit.jeap.processarchive.test.DecreeReference decreeReference;
    timestamp_ms createdAt;
    string title;
    string payload;
  }
}
```

## Validating the registry

A Maven plugin validates the state of the registry to prevent invalid or altered schemas from being merged to the
integration branch.

In particular, it validates:

- That schemas already merged to the integration branch (master) have not been changed
- That the Avro protocol contains a record with the name of the archive type
- That schemas referenced in the descriptor have correct syntax and can be parsed (including imports)
- That the layout of the schema registry matches the structure documented above
- That schemas are named according to `<archive-type>_v<version>.avdl`
- That schemas of different versions are compatible with each other according to their `compatibilityMode`

The Maven plugin is integrated into the schema registry's Maven build as follows:

```xml
<!-- pom.xml - Plugin for validating the Archive Type Registry -->
<build>
  <plugins>
    <plugin>
      <groupId>ch.admin.bit.jeap</groupId>
      <artifactId>jeap-process-archive-type-registry-maven-plugin</artifactId>
      <version>${jeap-process-archive.version}</version>
      <configuration>
        <gitUrl>https://github.com/jme-admin-ch/jme-archive-type-registry.git</gitUrl>
      </configuration>
      <executions>
        <execution>
          <goals>
            <goal>registry</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

## Publishing Java bindings for archive type versions

The `jeap-process-archive-avro-maven-plugin` can generate Java bindings for the archive types from the Avro schemas;
deployment to the Maven repository is also supported. For a complete example, see
[https://github.com/jme-admin-ch/jme-archive-type-registry](https://github.com/jme-admin-ch/jme-archive-type-registry).

```xml
<build>
  <plugins>
            <plugin>
                <groupId>io.github.git-commit-id</groupId>
                <artifactId>git-commit-id-maven-plugin</artifactId>
                <configuration>
                    <skipPoms>false</skipPoms>
                </configuration>
            </plugin>

            <plugin>
                <groupId>ch.admin.bit.jeap</groupId>
                <artifactId>jeap-process-archive-avro-maven-plugin</artifactId>
                <version>${jeap-process-archive-service.version}</version>
                <executions>
                    <execution>
                        <!-- Disable default execution from parent -->
                        <phase>none</phase>
                    </execution>
                    <execution>
                        <id>compile-archive-types</id>
                        <goals>
                            <goal>compile-archive-types</goal>
                        </goals>
                        <configuration>
                            <generateAllArchiveTypes>false</generateAllArchiveTypes>
                            <gitUrl>https://github.com/jme-admin-ch/jme-archive-type-registry.git</gitUrl>
                            <groupIdPrefix>ch.admin.bit.jme.archivetype</groupIdPrefix>
                            <trunkBranchName>master</trunkBranchName>
                            <enableDecimalLogicalType>true</enableDecimalLogicalType>
                            <skip>${jeap.archivetypes.compile.skip}</skip>
                        </configuration>
                    </execution>
                    <execution>
                        <id>deploy-archive-type-artifacts</id>
                        <goals>
                            <goal>deploy-archive-type-artifacts</goal>
                        </goals>
                        <configuration>
                            <mavenDeployGoal>deploy</mavenDeployGoal>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
   </plugins>
</build>
```

## See also

- [Process Archive Service](index.md) — overview and architecture of the Process Archive Service.
- [Process Archive How-To](how-to.md) — step-by-step setup, including how to configure an Archive Type Registry.
- [Process Archive Backfill](backfill.md) — backfilling archived artifacts.
- [Process Archive Reader Library](reader-library.md) — reading archived data from object storage.
