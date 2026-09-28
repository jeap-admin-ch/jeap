# Authorization with simple roles

The following sections describe the integration and use of the `jeap-spring-boot-security-starter` library for
the case that an application authorizes user access against [simple roles](../role-concept.md#simple-roles).

## Integration

Authorization with simple roles is activated as described in
[Authentication and authorization for REST APIs – Integration](rest-api-authentication-and-authorization.md#integration).
However, note the following:

> **Note:** The configuration property `jeap.security.oauth2.resourceserver.system-name` must not be set when
> authorizing with simple roles, as it would otherwise activate authorization with semantic roles.

## Authorization checks

To check the authorization of a user based on simple roles, the following query methods are available:

| Method | Explanation |
| --- | --- |
| `hasRole(role)` | Does the user have the role `role`, either independently of a business partner (`userroles`) or for at least one business partner (`bproles`)? |
| `hasRoleForPartner(role, businessPartner)` | Does the user have the role `role` for the specified business partner `businessPartner`? (`bproles`) |
| `hasRoleForAllPartners(role)` | Does the user have the role `role` for all business partners, i.e. independently of a business partner? (`userroles`) |
| `getPartnersForRole(role)` | For which business partners does the user have the role `role`? (`bproles`) |

### Declarative authorization

The authorization check methods described above are available in the
[SpEL](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#expressions) expressions of
the `@PreAuthorize` and `@PostAuthorize` annotations of Spring Security:

```java
@PreAuthorize("hasRole('role')")
public Data getData(...) {
...

@PreAuthorize("hasRoleForPartner('role', #partnerId)")
public Partner getPartner(String partnerId) {
...
```

> **Note:** Unfortunately, IntelliJ cannot recognize these additional methods. Auto-completion etc. is therefore not
> available inside the SpEL string (see the
> [bug report in IntelliJ](https://youtrack.jetbrains.com/issue/IDEA-167762#focus=streamItem-27-3283942-0-0)).

### Programmatic authorization

Not all permissions can be checked purely declaratively. Sometimes, for example, data has to be loaded first in
order to check, based on the loaded data, whether a user may access it. The `jeap-spring-boot-security-starter`
therefore also offers all the authorization check methods described above directly in program code by providing
a Spring bean of type `ServletSimpleAuthorization` (WebMvc) that implements the methods.

Example of programmatic authorization with WebMvc:

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

## Business partner queries

Sometimes it is necessary to know the concrete business partners for which the current user has a certain role,
for example to load only those objects from the database that belong to these partners. The following query
method is available for this purpose:

| Query method | Explanation |
| --- | --- |
| `getPartnersForRole(role)` | All business partners for which the user has the given role. |

## Examples

The jEAP example project
[jme-security-oauth2-example](https://github.com/jme-admin-ch/jme-security-oauth2-example)
contains a resource that gives examples of both declarative and programmatic authorization with simple roles: [jme-security-oauth2-resource-service / .../resource/ThingResource.java](https://github.com/jme-admin-ch/jme-security-oauth2-example/blob/main/jme-security-oauth2-resource-service/src/main/java/ch/admin/bit/jeap/jme/security/oauth/resource/ThingResource.java)

```java
package ch.admin.bit.jeap.jme.security.oauth.resource;

import ch.admin.bit.jeap.security.resource.authentication.ServletSimpleAuthorization;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.access.prepost.PostAuthorize;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.Collection;
import java.util.Optional;
import java.util.Set;
import java.util.function.Supplier;
import java.util.stream.Collectors;

import static java.util.Collections.singleton;

/**
 * This class gives an example for an OAuth2 protected resource 'thing' that requires certain roles for access.
 * The thing resource manages data of things that belong to business partners. To access a thing's data a user is
 * required to have the role 'thing_read' for the specific business partner to which the thing to be accessed belongs.
 */
@RestController
@Slf4j
@RequiredArgsConstructor
public class ThingResource {

    private static final String THING_READ_ROLE = "thing_read";

    private final ServletSimpleAuthorization jeapAuthorization;

    private Set<Thing> things = Set.of(
            new Thing("1", "11111", "Thing1"),
            new Thing("2", "11111", "Thing2"),
            new Thing("3", "22222", "Thing3"),
            new Thing("8", "88888", "Thing8"),
            new Thing("9", "99999", "Thing9"));

    @GetMapping("/api/things")
    @PreAuthorize("hasRole('" + THING_READ_ROLE + "')")
    public Collection<Thing> listThings() {
        // Does the token grant read access on the things of all partners?
        if (jeapAuthorization.hasRoleForAllPartners(THING_READ_ROLE)) {
            // Fetch all things.
            return listAll();
        } else {
            // Determine the partners the token grants read access on things...
            Collection<String> partners = jeapAuthorization.getPartnersForRole(THING_READ_ROLE);
            // ...then only provide the things belonging to those partners.
            return listForPartners(partners);
        }
    }

    @GetMapping("/api/partners/{partnerId}/things")
    @PreAuthorize("hasRoleForPartner('" + THING_READ_ROLE + "', #partnerId)")
    public Collection<Thing> listThingsForBusinessPartner(@PathVariable("partnerId") String partnerId) {
        return listForPartners(singleton(partnerId));
    }

    /**
     * We can't do a detailed authorization check on the thing entering the method because we do not yet know the
     * partner to which the thing belongs. However, we can do this check when leaving the method, because the return
     * object contains the partner id. This web endpoint will not return the thing if the token does not contain the role
     * 'things_read' for the partner to which the thing belongs. If the return object would not contain the partner id,
     * the detailed authorization check would have to be done programmatically using the appropriate
     * ServletSimpleAuthorization bean method. See {@link #getThingById2(String)} for such an example.
     */
    @GetMapping("/api/things/{id:[0-4][0-9]*}")
    @PreAuthorize("hasRole('" + THING_READ_ROLE + "')")
    @PostAuthorize("hasRoleForPartner('" + THING_READ_ROLE + "', returnObject.getPartnerId())")
    public Thing getThingById1(@PathVariable("id") String id) {
        return findThingById(id).orElseThrow(supplyThingNotFoundStatusException(id));
    }

    /**
     * Same as {@link #getThingById1(String)} but replacing the declarative @PostAuthorize() check with a programmatic check.
     * See {@link #getThingById1(String)} for explanation.
     */
    @GetMapping("/api/things/{id:[5-9][0-9]*}")
    @PreAuthorize("hasRole('" + THING_READ_ROLE + "')")
    public Thing getThingById2(@PathVariable("id") String id) {
        Thing thing = findThingById(id).orElseThrow(supplyThingNotFoundStatusException(id));
        if (jeapAuthorization.hasRoleForPartner(THING_READ_ROLE, thing.getPartnerId())) {
            return thing;
        } else {
            throw new AccessDeniedException("Access to thing with id '" + id + "' denied.");
        }
    }

    private Supplier<ResponseStatusException> supplyThingNotFoundStatusException(final String thingId) {
        return () -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Thing with id '" + thingId + "' not found");
    }

    private Collection<Thing> listAll() {
        return things;
    }

    private Collection<Thing> listForPartners(Collection<String> partners) {
        return things.stream().filter(thing -> partners.contains(thing.getPartnerId())).collect(Collectors.toSet());
    }

    private Optional<Thing> findThingById(String id) {
        return things.stream().filter(thing -> thing.getId().equals(id)).findFirst();
    }
}
```

## Further documentation

- [Role concept in the Blueprint Microservice](../role-concept.md)

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Authentication and authorization for REST APIs](rest-api-authentication-and-authorization.md) — integrate jEAP Security into a REST API.
- [Role concept in the Blueprint Microservice](../role-concept.md) — understand simple roles, semantic roles and authorities.
- [Authorization with semantic roles](rest-api-authorization-with-semantic-roles.md) — authorize against roles composed of system, tenant, resource and operation.
- [Authorization with authorities](rest-api-authorization-with-authorities.md) — derive fine-grained authorities from roles.
