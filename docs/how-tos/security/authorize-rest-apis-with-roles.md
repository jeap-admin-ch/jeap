# How to: authorize REST API access with roles

jEAP supports two role models for authorizing access to a REST API:
[simple roles](../../concepts/authentication-and-authorization/role-concept.md#simple-roles) and
[semantic roles](../../concepts/authentication-and-authorization/role-concept.md#semantic-roles). Pick the
model your application uses, then follow the matching steps below.

## Steps: authorize with simple roles

1. Complete the basic integration described in
   [Authentication and authorization for REST APIs – Integration](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authentication-and-authorization.md#integration).
   Leave `jeap.security.oauth2.resourceserver.system-name` unset — setting it activates authorization with
   semantic roles instead.
2. Check a role declaratively in the
   [SpEL](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#expressions)
   expressions of the `@PreAuthorize` and `@PostAuthorize` annotations:

   ```java
   @PreAuthorize("hasRole('role')")
   public Data getData(...) {
   ...

   @PreAuthorize("hasRoleForPartner('role', #partnerId)")
   public Partner getPartner(String partnerId) {
   ...
   ```

   > **Note:** Unfortunately, IntelliJ cannot recognize these additional methods. Auto-completion etc. is
   > therefore not available inside the SpEL string (see the
   > [bug report in IntelliJ](https://youtrack.jetbrains.com/issue/IDEA-167762#focus=streamItem-27-3283942-0-0)).

3. Or, when the check cannot be expressed declaratively — for example because the data has to be loaded
   first — check a role programmatically through the `ServletSimpleAuthorization` (WebMvc) Spring bean:

   ```java
   import ch.admin.bit.jeap.security.resource.authentication.ServletSimpleAuthorization;
   ...

   private ServletSimpleAuthorization jeapAuthorization;
   ...

   public Partner findPartner(...) {
   	Partner partner = ...
   	//Throw an exception if the user is not allowed to access the partner
   	if (!jeapAuthorization.hasRoleForPartner("role", partner.getPartnerId())) {
   		throw new AccessDeniedException("Missing role for partner with id '" + partner.getPartnerId());
   	}
   	return partner;
   }
   ```

For the full set of available query methods and a complete worked example, see
[Authorization with simple roles](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authorization-with-simple-roles.md).

## Steps: authorize with semantic roles

1. Complete the basic integration described in
   [Authentication and authorization for REST APIs – Integration](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authentication-and-authorization.md#integration),
   and set `jeap.security.oauth2.resourceserver.system-name` — it is required for authorization with
   semantic roles.
2. Check roles declaratively in the
   [SpEL](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#expressions)
   expressions of the `@PreAuthorize` and `@PostAuthorize` annotations (MVC and WebFlux):

   ```java
   @PreAuthorize("hasRole('resource', 'operation')")
   public Data getData(...) {
   ...

   @PreAuthorize("hasRoleForPartner('resource', 'operation', #partnerId)")
   public Partner getPartner(String partnerId) {
   ...
   ```

   > **Note:** Unfortunately, IntelliJ cannot recognize these additional methods. Auto-completion etc. is
   > therefore not available inside the SpEL string (see the
   > [bug report in IntelliJ](https://youtrack.jetbrains.com/issue/IDEA-167762#focus=streamItem-27-3283942-0-0)).

3. Or, when the check cannot be expressed declaratively — for example because the data has to be loaded
   first — check roles programmatically through the `ServletSemanticAuthorization` Spring bean:

   ```java
   import ch.admin.bit.jeap.security.resource.semanticAuthentication.ServletSemanticAuthorization;
   ...

   private ServletSemanticAuthorization jeapAuthorization;
   ...

   public Partner findPartner(...) {
   	Partner partner = ...
   	//Throw an exception if the user is not allowed to access the partner
   	if (!jeapAuthorization.hasRoleForPartner("resource", "operation", partner.getPartnerId())) {
   		throw new AccessDeniedException("Missing role for partner with id '" + partner.getPartnerId());
   	}
   	return partner;
   }
   ```

For the full set of available query methods, including how to query all roles or all business partners a
user has access for, see
[Authorization with semantic roles](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authorization-with-semantic-roles.md).

## Related

- [Role concept in the Blueprint Microservice](../../concepts/authentication-and-authorization/role-concept.md) — understand simple roles, semantic roles and authorities before choosing one.
- [Authorization with simple roles](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authorization-with-simple-roles.md) — query-method reference and a complete worked example.
- [Authorization with semantic roles](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authorization-with-semantic-roles.md) — query-method reference and a worked example of query results.
- [How to: authorize REST API access with authorities](authorize-rest-apis-with-authorities.md) — the alternative model for application-local, fine-grained permissions.
- [Authentication and authorization for REST APIs](../../concepts/authentication-and-authorization/protecting-rest-apis/rest-api-authentication-and-authorization.md) — the basic integration these steps build on.
