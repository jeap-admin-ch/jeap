# Role concept in the Blueprint Microservice

In the Blueprint Microservice, authorization is performed on the basis of application roles. Every access to an
[API protected with OAuth2](protecting-rest-apis/rest-api-authentication-and-authorization.md) carries a
[token](tokens/tokens-in-the-blueprint-microservice.md) with information about the current user, including the roles the
user holds for an application.

The Blueprint Microservice distinguishes between two kinds of roles:

- **User roles** are roles a user holds in principle. The user can exercise such roles *for any business partner*.
  This is typically the case for a technical user, or for persons who must be able to exercise certain roles for all
  business partners, such as administrators or privileged clerks. In the
  [tokens of the Blueprint Microservice](tokens/tokens-in-the-blueprint-microservice.md), such roles are stored in the claim
  **`userroles`**.
- **Business partner roles** are roles a user holds only *in the context of specific business partners*. The user
  can exercise such roles only *for specific business partners*. This is the case, for example, for an employee of a
  business partner who may exercise their roles only for this specific business partner, but not for others. In the
  [tokens of the Blueprint Microservice](tokens/tokens-in-the-blueprint-microservice.md), such roles are stored in the claim
  **`bproles`**.

> **Note:** To use business partner roles, the system used for role management must be able to assign roles
> specifically for particular business partners only.

## Use of roles in contexts

In the Blueprint Microservice, authentication takes place in one of three
[authentication contexts](index.md#authentication-contexts). Different kinds of roles are typically used in the
different contexts.

|  | User context | System context | B2B context |
| --- | --- | --- | --- |
| Context description | Access of a human user to a UI or a service | Service-to-service requests of technical users | Request of an external system to a service through an API gateway using an API subscription |
| `userroles` | Roles the user can exercise on behalf of any business partner | Roles of the technical user for all business partners | n/a |
| `bproles` | Roles the user can exercise only on behalf of specific business partners | n/a | Only roles for the business partner for which the API subscription was created; the API description defines which roles exist |

## Interpretation of roles

Roles in the Blueprint Microservice are simply arbitrary strings without any requirements on their
structure or content. The Blueprint Microservice does, however, offer different models for interpreting roles when
authorizing users. An application has to choose one of these models. The following sections describe the role models
supported by jEAP and the corresponding way roles are checked for user authorization.

## Simple roles

In the *simple roles* model, roles are interpreted as arbitrary strings without a specific structure or content.
For a role check, the roles present and the roles required are simply compared one-to-one.

The page [Authorization with simple roles](protecting-rest-apis/rest-api-authorization-with-simple-roles.md) describes in detail how
simple roles are checked.

### Granularity of simple roles

The Blueprint Microservice makes no assumptions about the granularity of simple roles. Such a role can be a "real"
role such as `head_of_division`, or a permission such as `vacation_approve`.

### Prerequisites for using simple roles

Since the Blueprint Microservice imposes no requirements on simple roles other than that they must be strings,
simple roles can be used very flexibly.

## Semantic roles

In addition to the *simple roles* model, the Blueprint Microservice also supports the *semantic roles* model and
the corresponding *semantic role check*. A semantic role is a simple role that consists of specific elements with a
defined meaning. The following elements are defined:

- **system:** name of the business application that authorizes against the role
- **tenant:** tenant that can exercise the role
- **resource:** type of resource the role can be used for
- **operation:** operation that the role permits on the resource

The tenant element of a role can be used, for example, to define individual data areas for different business
applications in shared services. Shared services offer their services to several business applications. Typically,
however, the different business applications must not be able to access each other's data.

The name of a semantic application role is defined by the elements above. The individual elements are delimited by
dedicated special characters, so that the parts of a semantic role are always clearly recognizable. Standard naming
pattern for semantic roles:

```text
system_%tenant_@resource_#operation
```

Starting with jEAP Security version 20.2.0, semantic roles may also be written in an alternative syntax. This is
necessary, for example, when semantic roles are managed by an authorization server that does not allow the special
characters `%` and `#` in role names. The following naming pattern for semantic roles can be used as an alternative:

```text
system_:tenant_@resource_!operation
```

> **Warning:** The underscore `_` serves as the separator between the individual elements and is not allowed
> within an element.

### Wildcards

Semantic roles support wildcards: individual elements may be omitted. Omitting an element corresponds to a wildcard
for that element. If, for example, the resource element is omitted, the role applies to any resource. Wildcards are
allowed for all elements except the system element.

The page [Authorization with semantic roles](protecting-rest-apis/rest-api-authorization-with-semantic-roles.md) describes in detail
how semantic roles are checked.

### Examples of semantic roles

| Example | Meaning |
| --- | --- |
| `input_#read` | In the business application *Input*, all resources of all business applications (tenants) can be read (*read*) |
| `input_%camiuns_@registrationcertificate_#update` | In the business application *Input*, *registrationcertificate* resources of the business application *camiuns* can be modified (*update*) |
| `input_:camiuns_@registrationcertificate_!update` | Same role as in the previous row, but in the alternative notation |
| `input_%autorisaziun` | In the business application *Input*, all resources of the business application *autorisaziun* can be created, read, modified, deleted etc. (wildcard on operation) |
| `docbox_@decree_#read` | In the business application *DocBox*, all *decree* documents of all business applications can be read (*read*) |
| `biera` | In the business application *Biera*, all resources of all business applications can be created, read, modified, deleted etc. (wildcards on tenant, resource and operation) |

### Granularity of semantic roles

Semantic roles describe fine-grained permissions (of business applications) on resources in a business system.
Semantic roles therefore do not correspond to "real" roles in the sense of the business roles of persons within an
organization.

The fine granularity of semantic roles allows a correspondingly fine-grained authorization of users directly in a
system for managing user roles, i.e. without changes to the code of a business application.

### Prerequisites for using semantic roles

Since semantic roles are fine-grained, a business system will typically define a large number of semantic roles.
For semantic roles to be used efficiently, the role management system should be able to group roles and to
authorize users on the basis of such groups.

The system that manages semantic roles must support the special characters used by semantic roles in role names.
Two syntax variants are currently available for semantic roles. The standard syntax variant uses the special
characters `_`, `%`, `@` and `#`, while the alternative syntax variant uses the special characters `_`, `:`, `@`
and `!`.

## Authorities

For applications that want to use fine-grained roles or permissions but cannot or do not want to maintain them in
the role management system, the Blueprint Microservice additionally supports the concept of *authorities*.
Authorities are fine-grained permissions that are known only within the application itself. To authorize a user
against authorities, the application derives them from the user's coarse-grained roles according to rules it defines
itself. The derivation logic is part of the application code.

If a user has the role `vacation_manager`, for example, authorities such as `vacation_create`, `vacation_delete` or
`vacation_approve` could be derived from it and checked in the corresponding vacation management functions of the
application.

Authorities are simple strings without specific restrictions. For an authorization, the authorities
present and the authorities required are simply compared one-to-one. The page
[Authorization with authorities](protecting-rest-apis/rest-api-authorization-with-authorities.md) describes in detail how authorities
are checked.

> **Note:** Authorities currently cannot be defined for specific business partners; they always
> apply independently of business partners, i.e. for all business partners.

### Prerequisites for using authorities

To use authorities, the application must provide its own code that derives authorities from roles.

### Granularity of authorities

Since authorities are simple strings, they can represent anything. Typically, however, they represent
fine-grained permissions.

## Related

- [Authentication and authorization](index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Tokens in the Blueprint Microservice](tokens/tokens-in-the-blueprint-microservice.md) — the claims (`userroles`, `bproles`) that carry the roles.
- [Authentication and authorization for REST APIs](protecting-rest-apis/rest-api-authentication-and-authorization.md) — where and how roles are checked.
- [Authorization with simple roles](protecting-rest-apis/rest-api-authorization-with-simple-roles.md)
- [Authorization with semantic roles](protecting-rest-apis/rest-api-authorization-with-semantic-roles.md)
- [Authorization with authorities](protecting-rest-apis/rest-api-authorization-with-authorities.md)
- [Authorizing Keycloak clients for consuming application resources](authorization-servers/authorizing-keycloak-clients-for-consuming-applications-resources.md) — assigning roles to consuming applications in the system context.
- [JWT access token authorization flow in jEAP Security](protecting-rest-apis/jwt-access-token-authorization-flow.md) — how roles and authorities are derived from a token at runtime.
