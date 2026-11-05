# Authorization with authorities

The following sections describe the integration and use of the `jeap-spring-boot-security-starter` library when
an application authorizes user access against [authorities](../role-concept.md#authorities).

## Integration

For the integration steps, see
[How to: authorize REST API access with authorities](../../../how-tos/security/authorize-rest-apis-with-authorities.md).
This page describes the `AuthoritiesResolver` API used by that integration.

The code that derives authorities from roles has to be integrated into the application. For
this, the application has to provide a Spring bean of type `AuthoritiesResolver`. If no custom
`AuthoritiesResolver` is defined, a `DefaultAuthoritiesResolver` is used, which simply creates an authority for
each role by prefixing the role with `ROLE_`.

An `AuthoritiesResolver` implementation has access to both the user roles (`userroles`) and the business partner
roles (`bproles`) of the user. From these, the implementation can derive an arbitrary set of authorities in the
form of Spring Security `GrantedAuthority` instances.

Skeleton of a custom `AuthoritiesResolver` implementation:

```java
@Component
public class ExampleAuthoritiesResolver implements AuthoritiesResolver {

    @Override
    public Collection<GrantedAuthority> deriveAuthoritiesFromRoles(Set<String> userRoles, Map<String, Set<String>> businessPartnerRoles) {
        // Implementation
    }

}
```

A suitable `GrantedAuthority` implementation is, for example, the Spring Security class `SimpleGrantedAuthority`,
which is essentially a simple wrapper around a string.

A concrete example of an `AuthoritiesResolver` is given in
[jme-security-oauth2-resource-authorities-service](https://github.com/jme-admin-ch/jme-security-oauth2-example/blob/main/jme-security-oauth2-resource-authorities-service/src/main/java/ch/admin/bit/jeap/jme/security/oauth/resource/ExampleAuthoritiesResolver.java).

## Authorization checks

Authorities are a basic mechanism of Spring Security. To check the authorization of a user based on authorities,
the standard Spring Security mechanisms can be used.

**See [How to: authorize REST API access with authorities](../../../how-tos/security/authorize-rest-apis-with-authorities.md)**
for how to check authorities declaratively with `@PreAuthorize`/`@PostAuthorize` and programmatically from the
`Authentication`.

## Examples

The jEAP example project
[jme-security-oauth2-example](https://github.com/jme-admin-ch/jme-security-oauth2-example)
contains the module `jme-security-oauth2-resource-authorities-service` with a resource that gives an example of
authorization with authorities, including the
[ExampleAuthoritiesResolver](https://github.com/jme-admin-ch/jme-security-oauth2-example/blob/main/jme-security-oauth2-resource-authorities-service/src/main/java/ch/admin/bit/jeap/jme/security/oauth/resource/ExampleAuthoritiesResolver.java)
described above.

## Further documentation

- [Role concept in the Blueprint Microservice](../role-concept.md)

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Authentication and authorization for REST APIs](rest-api-authentication-and-authorization.md) — integrate jEAP Security into a REST API.
- [Role concept in the Blueprint Microservice](../role-concept.md) — understand simple roles, semantic roles and authorities.
- [Authorization with simple roles](rest-api-authorization-with-simple-roles.md) — authorize against roles compared one-to-one as strings.
- [Authorization with semantic roles](rest-api-authorization-with-semantic-roles.md) — authorize against roles composed of system, tenant, resource and operation.
- [How to: authorize REST API access with authorities](../../../how-tos/security/authorize-rest-apis-with-authorities.md) — the integration and authorization-check steps.
