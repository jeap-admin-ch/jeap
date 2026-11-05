# How to: authorize REST API access with authorities

[Authorities](../../concepts/authentication-and-authorization/role-concept.md#authorities) let an
application check fine-grained, application-local permissions derived from a user's roles, using Spring
Security's own authority mechanism.

## Steps

1. Complete the basic integration described in
   [Authentication and authorization for REST APIs – Integration](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authentication-and-authorization.md#integration).
   Leave `jeap.security.oauth2.resourceserver.system-name` unset — setting it activates authorization with
   semantic roles instead.
2. If the default role-to-authority mapping (prefixing each role with `ROLE_`) is not sufficient, provide a
   custom `AuthoritiesResolver` Spring bean — see
   [Authorization with authorities – Integration](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authorization-with-authorities.md#integration)
   for the API and an example implementation.
3. Check an authority declaratively in the
   [SpEL](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#expressions)
   expressions of the `@PreAuthorize` and `@PostAuthorize` annotations using `hasAuthority`:

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

4. Or, to query the actual authorities of a user — for example to search a database for objects matching
   these permissions — obtain them from the Spring Security `Authentication`:

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

## Related

- [Authorization with authorities](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authorization-with-authorities.md) — the `AuthoritiesResolver` API reference and a complete example.
- [Role concept in the Blueprint Microservice](../../concepts/authentication-and-authorization/role-concept.md) — understand simple roles, semantic roles and authorities before choosing one.
- [How to: authorize REST API access with roles](authorize-rest-apis-with-roles.md) — the alternative models based on roles carried in the token.
- [Authentication and authorization for REST APIs](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authentication-and-authorization.md) — the basic integration these steps build on.
