# Authorization with authorities

The following sections describe the integration and use of the `jeap-spring-boot-security-starter` library when
an application authorizes user access against [authorities](../role-concept.md#authorities).

## Integration

The first step for authorization with authorities is the basic integration of
jEAP Security as described in
[Authentication and authorization for REST APIs – Integration](rest-api-authentication-and-authorization.md#integration).
Note the following:

> **Note:** The configuration property `jeap.security.oauth2.resourceserver.system-name` must not be set when
> authorizing with authorities, as it would otherwise activate authorization with semantic roles.

In a second step, the code that derives authorities from roles has to be integrated into the application. For
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
the standard Spring Security mechanisms can be used. The following sections give examples of
some of these mechanisms.

### Declarative authorization

Authorities can be checked in the
[SpEL](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#expressions) expressions of
the `@PreAuthorize` and `@PostAuthorize` annotations using the `hasAuthority` method:

```java
@RestController
public class ExampleResource {

	@GetMapping("/example")
	@PreAuthorize("hasAuthority('example:read')")
	public String hello() {
		return "Hello World";
	}
}
```

### Querying the authorities of a user

Sometimes the actual permissions of a user have to be known, for example to search a database for objects
matching these permissions. For such cases, the authorities of a user can be obtained from their Spring Security
`Authentication`, for example as follows:

```java
@RestController
public class ExampleResource {

	@GetMapping("/example")
	public String hello(Authentication authentication) {
       	Collection<? extends GrantedAuthority> authorities = authentication.getAuthorities();
		...
	}
}
```

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
