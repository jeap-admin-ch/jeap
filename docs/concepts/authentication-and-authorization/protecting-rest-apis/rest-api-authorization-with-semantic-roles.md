# Authorization with semantic roles

The following sections describe the integration and use of the `jeap-spring-boot-security-starter` library when
an application authorizes user access against [semantic roles](../role-concept.md#semantic-roles).

## Integration

For the integration steps, see
[How to: authorize REST API access with roles](../../../how-tos/security/authorize-rest-apis-with-roles.md#steps-authorize-with-semantic-roles).
In short, the configuration property `jeap.security.oauth2.resourceserver.system-name` must be set for
authorization with semantic roles.

## Authorization checks

To check the authorization of a user based on semantic roles, the following query methods are available:

| Method | Explanation |
| --- | --- |
| `hasRole` | Does the user have a role, either independently of a business partner (`userroles`) or for at least one business partner (`bproles`)? |
| `hasRoleForPartner` | Does the user have a role for a specific business partner? (`bproles`) |
| `hasRoleForAllPartners` | Does the user have a role for all business partners, i.e. independently of a business partner? (`userroles`) |
| `getPartnersForRole` | For which business partners does the user have the role? (`bproles`) |

In these query methods, the role is specified by naming its individual elements. Not all elements have to
be specified; only the specified elements are then checked for authorization.
The following patterns are typically available:

| Pattern | Explanation |
| --- | --- |
| `operation` | Does the user have a role with the specified operation? |
| `resource, operation` | Does the user have a role with the specified operation for the specified resource? |
| `tenant, resource, operation` | Does the user have a role with the specified operation for the specified resource and the specified tenant? |

### Example

An example illustrates the query methods and their patterns. Let us assume:

- An **employee** of a freight forwarder may read customs declarations in the application `freight` for the
  partner companies "12345" and "9999". Their access token therefore contains the claim
  `"bproles": { "12345": ["freight_@declaration_#read"], "9999": ["freight_@declaration_#read"] }`.
- The technical user of the **microservice** "Billing" may create, read, modify and delete the
  customs declarations of all business partners. Its access token therefore contains the claim
  `"userroles": ["freight_@declaration"]`.
- The **accounting system** of the company "12345" may read the customs declarations and the billing statements
  of its company. Its access token therefore contains the claim
  `"bproles": { "12345": ["freight_@declaration_#read", "freight_@billing_#read"] }`.

The following queries then return the following results for the employee, the microservice and the accounting
system:

| Query | Employee | Microservice | Accounting system |
| --- | :---: | :---: | :---: |
| `hasRole('declaration', 'read')` | ✅ | ✅ | ✅ |
| `hasRoleForPartner('declaration', 'read', '12345')` | ✅ | ✅ | ✅ |
| `hasRoleForPartner('declaration', 'read', '9999')` | ✅ | ✅ | ❌ |
| `hasRoleForPartner('read', '9999')` | ✅ | ✅ | ❌ |
| `hasRole('declaration', 'create')` | ❌ | ✅ | ❌ |
| `hasRole('billing', 'read')` | ❌ | ❌ | ✅ |
| `hasRoleForPartner('billing', 'read', '12345')` | ❌ | ❌ | ✅ |
| `hasRoleForAllPartners('declaration', 'read')` | ❌ | ✅ | ❌ |
| `hasRoleForAllPartners('billing', 'read')` | ❌ | ❌ | ❌ |

### Checking roles declaratively or programmatically

**See [How to: authorize REST API access with roles](../../../how-tos/security/authorize-rest-apis-with-roles.md#steps-authorize-with-semantic-roles)**
for how to check the query methods above declaratively with `@PreAuthorize`/`@PostAuthorize`, or
programmatically through the `ServletSemanticAuthorization` Spring bean.

### Role queries

Sometimes it is necessary to know the actual permissions of the current user, for example to load all objects
from the database that the user has access to. The following query methods are available for this purpose:

| Query method | Explanation |
| --- | --- |
| `getAllRoles(operation)` | All roles of the user that authorize them for the given operation. |
| `getAllRolesForPartner(operation, partner)` | All roles of the user that authorize them for the given operation on behalf of the given business partner. Also includes all roles the user has for the given operation independently of a business partner (i.e. for all business partners). |
| `getAllRolesForAllPartners(operation)` | All roles of the user that authorize them for the given operation independently of a business partner (i.e. for all business partners). |

> **Note:** Since wildcards are allowed in semantic roles, be prepared for one of the returned roles to contain
> wildcards.

Example of a role query:

```java
private List<Task> getTasksForAllAllowedTenants() {
	Collection<SemanticApplicationRole> allReadRoles = jeapSemanticAuthorization.getAllRoles("task", "read");
	boolean hasTenantWildcard = allReadRoles.stream().anyMatch(role -> role.getTenant() == null);
	if(hasTenantWildcard) {
		return taskRepository.findAll();
	}
	return allReadRoles.stream()
		.map(SemanticApplicationRole::getTenant)
		.flatMap(taskRepository::findForTenant)
		.collect(Collectors.toList());
}
```

## Business partner queries

Sometimes it is necessary to know the actual business partners for which the current user has a certain
permission, for example to load only those objects from the database that belong to these partners. The
following query methods are available for this purpose:

| Query method | Explanation |
| --- | --- |
| `getPartnersForRole(operation)` | All business partners for which the user has at least one role with the given operation. |
| `getPartnersForRole(resource, operation)` | All business partners for which the user has at least one role with the given operation for the given resource. |
| `getPartnersForRole(tenant, resource, operation)` | All business partners for which the user has at least one role with the given operation for the given tenant and the given resource. |

## Examples

The jEAP example project
[jme-security-example](https://github.com/jme-admin-ch/jme-security-example)
contains a resource that gives examples of both declarative and programmatic authorization with semantic roles.

## Further documentation

- [Role concept in the Blueprint Microservice](../role-concept.md)

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Authentication and authorization for REST APIs](rest-api-authentication-and-authorization.md) — integrate jEAP Security into a REST API.
- [Role concept in the Blueprint Microservice](../role-concept.md) — understand simple roles, semantic roles and authorities.
- [Authorization with simple roles](rest-api-authorization-with-simple-roles.md) — authorize against roles compared one-to-one as strings.
- [Authorization with authorities](rest-api-authorization-with-authorities.md) — derive fine-grained authorities from roles.
- [How to: authorize REST API access with roles](../../../how-tos/security/authorize-rest-apis-with-roles.md) — the integration and authorization-check steps.
