# PostgreSQL with Spring and Flyway

## Introduction

The usage of the "public" DB schema as the default schema to use when creating DB objects is deprecated
since PostgreSQL 15. To use PostgreSQL 15, you need to create and configure a specific schema. So that all
projects using jEAP are consistent, it has been defined that this schema must be named "data". See
[Naming Conventions](../naming-conventions.md#postgresql-default-schema) for details.

## Configure the default schema in the application properties

These properties must be configured in `application.yml` to use a schema name in the application:

- `spring.jpa.properties.hibernate.default_schema`
- `spring.datasource.hikari.schema`
- `spring.flyway.default-schema`

## Example

**application.yml**

```yaml
...
spring:
  jpa:
    properties:
      hibernate:
        default_schema: data
  datasource:
    ...
    hikari:
      schema: ${spring.jpa.properties.hibernate.default_schema}
  flyway:
    ...
    # Flyway creates automatically the default schema if it doesn't exist
    default-schema: ${spring.jpa.properties.hibernate.default_schema}
```

## Configuration for H2

When h2 is used for unit testing, the schema `data` must also be created. By default, h2 converts
identifiers to uppercase and spring/hikari won't be able to find the right schema.

In this case it is possible to create the schema in the init statement of the database and to configure
`DATABASE_TO_UPPER=FALSE` to deactivate the uppercasing.

Example:

**application.yml**

```yaml
...
spring:
  datasource:
    driver-class-name: org.h2.Driver
    url: "jdbc:h2:mem:testdb;INIT=CREATE SCHEMA IF NOT EXISTS data;DATABASE_TO_UPPER=FALSE;MODE=PostgreSQL"
...
```

References:

- [http://www.h2database.com/html/features.html](http://www.h2database.com/html/features.html)

## Links

Example: [https://github.com/jme-admin-ch/jme-crypto-example/blob/main/src/main/resources/application.yml](https://github.com/jme-admin-ch/jme-crypto-example/blob/main/src/main/resources/application.yml)
