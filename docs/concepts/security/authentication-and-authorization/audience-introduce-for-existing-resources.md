# Migrating existing resource access to audience validation

This guide takes an existing system from access tokens without audiences to tokens addressed to their
intended resource servers. It supports two goals: making token introspection compatible with Keycloak's
additional audience check, and requiring audiences for resource access throughout a system. You can pursue
either goal on its own, complete both together, or finish the introspection work first and continue with
strict validation later.

Start by choosing your goal and the clients and resources it affects. Then follow the preparation and
audience introduction steps on this page, and complete the section for your selected goal. The linked
configuration pages explain individual settings; this guide describes the rollout order and completion
criteria.

## Choose your goal and scope

| Goal | What to include | What completion means |
|---|---|---|
| **Support Keycloak's introspection audience check** | Resource servers using introspection, clients supplying the tokens they introspect, and any other recipients affected by changing those tokens' audiences | The selected introspection flows work with audience enforcement enabled and no compatibility exceptions |
| **Require audience restriction throughout your system** | Assess all clients and resource servers in the system, including calls across team boundaries; prepare all applicable resources for strict validation | All applicable resources require matching audiences for `USER`/`SYS` access, and all intended calls work |
| **Achieve both** | The system-wide scope, with introspection users identified within it | Both goals are complete; their enforcement can happen at different times |

### Goal: support Keycloak's introspection audience check

Choose this goal when your immediate need is to stop relying on Keycloak's deprecated introspection
compatibility options. It can be a small migration if only a limited number of your resource servers
use token introspection and those resource servers are only accessed by a limited number of clients.
This goal does not require enabling strict audience validation on resource servers.

Follow the tokens to establish the actual boundary. If one resource server forwards a client's token
to another resource server, then the latter is also affected. The audience of a token must cover all
intended recipients of the token.

Also consider the reach of a configuration change: assigning a default/static audience to a calling client
affects all of its newly issued tokens, not just the ones used in calls to the introspecting resource.
Consider every token usage affected by an audience assignment.

Prioritize this goal where introspection is used: Keycloak's backward compatibility options are deprecated
and scheduled for removal in a future release. See 
[Audience for token introspection on Keycloak](audience-for-token-introspection-on-keycloak.md) for details.

### Goal: require audience restriction throughout the system

Choose this goal when you want every applicable resource in the system to require an audience. Assess
all clients and resources so that frontends, service calls, jobs and forwarding chains are accounted for.
Some may already be correctly configured and need no changes to token issuance.

The assessment is system-wide, but the rollout can proceed one resource at a time. A resource can enable
strict validation once all its relevant callers supply correctly addressed tokens. Other resources can
follow later.

This goal can be pursued separately from the goal to support Keycloak's introspection audience check. Where
introspection already works with audience enforcement, retain that configuration; where its migration is
outstanding, preferably use the introspection preparation and completion sections of this guide as well.

### How the two goals overlap

Adding the intended audiences for introspection already restricts where those tokens can be used: a
jEAP-based resource server rejects a nonempty audience that does not contain the receiving resource's ID,
even when strict validation is `off`. Enabling strict validation additionally rejects tokens with missing
or empty audiences. See the [validation matrix](audience-validation.md#what-jeap-validates).

For example, an Orders resource server might introspect the frontend's lightweight tokens but accept a nightly
job's ordinary tokens without introspection. Migrating the frontend's tokens and Orders' introspection client
can complete the introspection goal. Yet, if the job still supplies audience-free tokens, it must also be
migrated before Orders can enable strict audience validation and require audiences for all `USER`/`SYS` access.

If nearly all traffic undergoes introspection, most audience configuration may therefore already be done
when the introspection goal is complete. In that case, continue with the remaining callers and resource server
enforcement; keep the identifiers and mappings already introduced.

## Organize the rollout

Plan across the affected environments, then perform configuration changes, deployments and verification
**per environment**, starting with DEV and progressing through REF, ABN and PROD. The inventory and
identifier decisions in the audience introduction steps can be shared across environments, but check them
against the actual clients and configuration in each environment. Complete the applicable checks in an
environment before promoting that goal to the next.

DEV environments usually use the jEAP OAuth Mock Server. Represent the clients and token audiences through its
[configuration](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-oauth-mock-server/configuration);
apply the Keycloak scope and audience mapping instructions on environments that actually use Keycloak.

For each environment, use this order:

1. [Prepare the selected migration](#prepare-the-selected-migration), including its observation settings.
2. [Introduce audiences](#introduce-audiences) for the selected clients and all affected recipients.
3. [Complete the Keycloak introspection migration](#complete-the-keycloak-introspection-client-audience-check-migration),
   [complete strict audience enforcement](#complete-the-migration-to-a-general-audience-restriction-throughout-the-system), or do both, according
   to your goal.

When pursuing both goals, you can start with the clients supplying introspected tokens, complete their
introspection migration, and then introduce audiences for the remaining flows. Preparation for unrelated
callers must not delay the more urgent introspection migration. Conversely, a resource ready for strict local
validation can enable it while the migration of other resources is still ongoing.

Application teams inventory calls, deploy receiver and caller changes, and verify tokens and traffic.
On managed platforms, coordinate realm changes, introspection-client provisioning and secret delivery
with the platform team. The platform operator also coordinates removal of Keycloak compatibility
exceptions. Record team readiness separately from platform enforcement.

Use supported component versions containing the required features. The three local validation modes and
the introspection client-ID fallback were introduced in **jEAP Security Starter 24.26.0**, managed from
**jEAP Spring Boot Parent 40.7.0**. The introspection audience check was introduced in **jEAP OAuth Mock
Server 10.6.0**. These are feature introduction versions, not a recommendation to deploy those older
releases; check the effective versions of your supported parent.

## Prepare the selected migration

Apply the subsection for your goal, or both when pursuing both goals. Do this before changing token
issuance in the current environment. These settings help observe existing traffic and maintain compatible
operation while receivers, callers and introspection credentials are being updated.

### For the Keycloak introspection goal

On DEV, set the Mock Server's
[introspection audience check](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-oauth-mock-server/configuration#introspection-endpoint-audience-check)
to `warn` for the clients being migrated. Account for client-specific overrides of the server-wide setting.
Exercise actual traffic and use the warnings to find introspection clients missing from the inventory.
A warning identifies the introspection client; use the resource-server configuration to determine which
resource uses it, particularly when several resources share a client.

The rollout below assumes that token introspection without audience or without the introspection client's
ID in the introspected token's audience remains possible before the changes to the token audiences are
complete. In each Keycloak environment, confirm with the operator that the
necessary temporary [compatibility exceptions](audience-for-token-introspection-on-keycloak.md#keycloaks-temporary-backward-compatibility-options)
are effective for the migrating clients throughout that transition, including newly provisioned clients.
An already migrated flow can retain enforcement. A migration limited to enabling strict audience validation
on resource servers needs no Keycloak compatibility exception.

Keep the existing introspection client IDs and their secrets while introducing resource IDs
and token audiences. The client and credential switch comes after the token flows have been verified.

### For the strict audience enforcement goal

Set the strict audience validation option to `warn` on the resources being prepared and deploy it to all instances:

```yaml
jeap:
  security:
    oauth2:
      resourceserver:
        strict-audience-validation: "warn"
```

Exercise calls and search resource-server logs for `strict-audience-validation=warn`. These warnings
identify accepted `USER`/`SYS` tokens with missing or empty audiences. Use them to supplement the
inventory, including callers that are easy to overlook. Keep resources already enforcing `on` at `on`.

`warn` is not a general dry-run mode: it still rejects a nonempty audience without the resource's ID.
This is why receiver configuration must be deployed before new audiences are issued.

Note that this warning mode is independent of the Mock Server's introspection audience check warning mode:
the jEAP resource server warns about missing or empty token audiences while the mock server warns about
a missing introspection-client membership.

## Introduce audiences

These steps apply to the clients and resources selected for the current rollout. For the introspection
goal, that will be the limited scope established above. For the system-wide enforcement, repeat them for
the remaining resources as you progress. Reuse existing correct configuration after checking its coverage.

### 1. Inventory callers, token flows and recipients

Record which clients obtain tokens, which resources receive them, and which tokens are reused or
forwarded. Include frontends, service clients, background jobs, gateways, test-token issuers and callers
owned by other teams. Explicitly cover rare jobs and flows that exist only in higher environments.

For each token flow, record at least:

| Information | Why it matters |
|---|---|
| Token-obtaining client and issuer/realm | Identifies where to configure audience issuance |
| All intended recipients of that token | Defines the audience entries needed for shared or forwarded tokens |
| Each receiver's effective `resource-id` | Defines the exact value its local validator expects; the default is the `spring.application.name` |
| Token context and existing `aud` | Distinguishes audience-free flows, already correct flows and `B2B` exceptions |
| Introspection conditions, client IDs and credential references | Identifies tokens requiring Keycloak membership and resources sharing an introspection client |
| Environments, owners and verification evidence | Makes rollout coordination and coverage explicit |

Keep the distinction between two kinds of clients clear. The **token-obtaining client** receives the
audience scopes used to issue access tokens. The **introspection client** authenticates the resource
server's request to inspect one of those tokens. Giving an audience scope to the introspection client
does not add that audience to tokens obtained by other clients.

### 2. Agree on identifiers and audience lists

For a resource without an established audience contract, choose its identifier using the
[naming guidance](audience-naming.md). Keep an existing identifier if other callers already address
the resource correctly. Renaming established audiences is outside this migration.

For example, an Orders resource could use `https://resources.example.org/shop/orders`. A token intended
for Orders must then contain that exact value in its audience. If Orders uses introspection, the recommended
dedicated introspection client should have the same ID, so one audience entry satisfies both the resource
server's and Keycloak's introspection audience checks.

Determine the complete intended recipient list for each token usage. Suppose an audience-free token
currently reaches Orders and Inventory resource servers. Adding only Orders to `aud` makes Inventory
reject it, even when Inventory's resource server sets strict audience validation to `off` or
`warn`. Include Inventory's currently expected ID as well, or separate the token usages so each token
addresses its own recipients. Include only actual recipients; adding every service in the system would
unnecessarily broaden the token's audience and weaken security.

### 3. Deploy receiver configuration first

Set or retain each selected resource's `resource-id`. Deploy the configuration to all its instances
and confirm that every recipient affected by the planned token change expects the agreed identifier.
An already correctly configured recipient may need no additional deployment.

```yaml
jeap:
  security:
    oauth2:
      resourceserver:
        resource-id: https://resources.example.org/shop/orders
```

Retain the observation setting (e.g. `warn`) selected before and the working introspection credentials.
Existing explicit introspection client IDs remain in use until the later client switch. If a resource 
omits `introspection.client-id`, it uses the `resource-id` fallback: changing `resource-id` then also
changes the introspection identity. Preserve the current identity explicitly during preparation, or
coordinate its client and matching secret before deploying that change.

Finish receiver preparation before assigning new default/static audiences. Those assignments will affect
the next token acquisition immediately, without any deployment of the calling application.

### 4. Configure audience issuance

Follow [Configuring audiences in Keycloak](audience-configuration-in-keycloak.md) to create resource
scopes and audience mappers and assign them to the **clients obtaining the access tokens**. Use the
audience lists from step 2, including all recipients of shared tokens. Include the audience in normal
and lightweight access tokens and in introspection responses, as described in the mapper instructions.

For the introspection goal, use **default/static scopes on the affected token-obtaining clients** as the
straightforward migration approach. The audience is then included without requiring changes to the clients'
authentication requests. Check the impact on all their token usages before making that assignment.

For general audience restriction, choose default/static scopes for audiences always needed by a client, or
optional/dynamic scopes when the client application should be able to select the required recipients when
obtaining a token. Optional/dynamic scopes require explicitly setting the scope request parameter; the
selection can be fixed in application configuration or chosen at runtime. See
[Selecting audiences](audience-selection.md). A Default audience cannot be deselected by omitting its
scope from a request.

Inspect the resulting audience list for unintended entries from other mappers, such as an Audience
Resolve mapper. Follow the configuration reference when removing those entries, considering other
clients that inherit the same mapper. Preserve required role mappings.

### 5. Align callers, mock data and test tokens

Make optional/dynamic scopes available on the calling client as needed. Update configured client scope lists
where necessary. A default/static scope need not be requested explicitly, although listing it can document
the application's expectation. Use the examples provided by [Selecting audiences](audience-selection.md) for
Spring client registrations and explicit token requests.

In DEV, configure the corresponding token audiences and clients in the Mock Server. Align signed test
tokens with the same resource IDs. The
[jEAP Security Test Starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-starter-test#minting-signed-jwts)
provides `JwsBuilder` for tests that exercise JWT validation. For example, use
`withAudiences("https://resources.example.org/shop/orders")` for a token addressed to the Orders resource.

If tests use the jEAP Security Test Starter's
[OIDC Authorization Code mock](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-starter-test#oidc-authorization-code-mock-server),
check its audience too: it derives `aud` from `client_id` or `withDefaultClientId(...)`. This is a different
test facility from the jEAP OAuth Mock Server.

### 6. Verify the changed flows

Obtain new access tokens through the actual authentication flows and inspect the issued tokens' `aud`
claims. Check that the tokens' audiences contain all intended recipients and no unintended ones.
Assess calls to every affected recipient, including token forwarding, rare jobs and lightweight tokens
where used.

Check for unsuccessful calls as well as for warnings in the logs. A wrong nonempty audience is rejected by
a resource server even in `warn` mode. Test rejection at an unaddressed `USER`/`SYS` resource as well as
success at the intended resources.

Let previously issued audience-free access tokens expire, or ensure their replacement, before enabling
checks that will reject them. Include long-lived sessions in the verification so that continued token
acquisition supplies the expected audiences.

For an introspection client audience check migration, an old introspection client whose ID differs from
the new resource audience may still produce warnings from the OAuth Mock Server at this point. That is
expected until the client switch below. For a combined migration, warnings from callers outside
the current rollout identify remaining strict-validation work; they do not block completing introspection
migration for already prepared token flows.

This stage is complete when the token flows selected for this rollout have the intended audiences and
their actual calls succeed. Record which flows were verified. Quiet logs without traffic do not prove
coverage. Continue with the completion section(s) for the selected goal(s).

## Complete the Keycloak introspection client audience check migration

Use this section after introducing audiences for all token flows that the selected resources introspect and
after verifying the other recipients affected by those audience changes.

### Provision and switch introspection clients

1. **Provision a dedicated client per resource.** In each affected realm, follow
   [Creating the introspection client in Keycloak](audience-for-token-introspection-on-keycloak.md#creating-the-introspection-client-in-keycloak).
   Its ID equals the resource ID, client authentication is enabled, and token-issuing flows are disabled.
   Reuse an existing dedicated client that already meets these requirements. Represent it in the DEV
   mock as appropriate. Coordinate secret delivery with the platform team and keep the old clients
   available during the rollout.
2. **Switch the ID and secret together.** Remove an old explicit introspection `client-id` declaration to make
   use of jEAP Security's fallback to the resource server's resource ID as the introspection client's ID. At
   the same time configure the new secret or secret reference for the new introspection client. Check all configuration
   sources for stale overrides and deploy all instances. Removing only the ID is insufficient: the secret must
   belong to the new client. Repeat for each configured issuer requiring introspection.
3. **Verify actual introspection and API calls.** Compare the authenticated introspection client ID with
   the token's audience for every introspected token flow. Exercise conditional introspection (e.g. when using
   lightweight access tokens) and use newly issued tokens to avoid testing only cached responses. Resolve remaining
   OAuth Mock Server warnings and investigate Keycloak compatibility warnings in its logs with the operator.

The recommended dedicated client avoids an extra audience entry solely for introspection. Retaining a
shared client and adding its ID to tokens is technically possible, but retains shared introspection access
across resources; see the [client recommendation](audience-for-token-introspection-on-keycloak.md#use-the-resource-id-as-the-introspection-client-id).

### Enforce and test in the current environment

On **DEV**, change the OAuth Mock Server's introspection client audience check mode from `warn` to `on`
for the migrated clients. Check client-specific overrides so that the intended mode is effective.
Keep it at `on` after migration to continue simulating Keycloak enforcement.

After the DEV checks pass, progress through **REF, ABN and PROD** using the rollout order above. In each
environment, first finish its audience introduction and client switch, then report readiness to the
operator. Once all introspection users affected by Keycloak's backward compatibility setting are ready,
the Keycloak operator can disable the applicable server-wide and client-level exceptions on Keycloak.

Successful DEV tests do not replace verification against Keycloak in each higher environment.

Test the introspection endpoint with otherwise valid tokens and credentials:

| Audience membership | Expected introspection result with enforcement |
|---|---|
| Contains the authenticated introspection client's ID | `active=true` |
| Does not contain that ID, including a missing or empty audience | `active=false` |


### Completion and stopping point

**The team is ready in an environment** when all token flows with introspection have verified audience
membership of the introspection client ID, all instances use the new client credentials, and the team's
old introspection credentials are no longer used. DEV must also pass positive and negative tests with
the OAuth Mock Server introspection client audience check at `on`. Readiness in a higher environment
can be reported while the operator coordinates other teams.

**The introspection goal is complete in an environment** when enforcement is effective and the endpoint
tests and normal API calls pass: OAuth Mock Server introspection client audience check `on` on DEV, or
Keycloak's check with all relevant compatibility exceptions disabled in a Keycloak environment. After
rollout and observation, arrange retirement of unused clients and credentials with their owner. A shared
old introspection client must remain available until every user has switched.

If compatibility with Keycloak's additional introspection client audience check was your only goal, you
can stop after this has been completed in all required environments. Unrelated clients and resources do
not have to migrate. If you also want general system-wide audience restriction enforcement, reuse the
completed work and continue with the remaining callers and resources below.

## Complete the migration to a general audience restriction throughout the system

Use this section for each resource where audiences should become mandatory. It applies whether you
introduced its audiences directly or already did most of that work for introspection. Existing correctly
addressed tokens need no new audience configuration.

### Establish readiness for the whole resource

Before changing a resource server's strict audience validation option to `on`, account for **all its
`USER`/`SYS` callers**, including those whose tokens are not introspected and callers outside your team.
Check the inventory against actual traffic and resolve remaining `strict-audience-validation=warn` warnings.

The completion criterion here is broader than introspection readiness: every relevant caller of this
resource must supply an audience containing its resource ID. A frontend working with enforced
introspection does not establish readiness for a non-introspected nightly job calling the same resource.

Confirm that old audience-free access tokens have expired or been replaced. Inspect failed calls as
well as warnings, and explicitly exercise infrequent jobs and forwarding chains. Quiet logs alone are
not sufficient evidence.

### Enable and verify strict audience validation

Enable the strict audience validation settings and deploy them to the prepared resource servers in the current
environment:

```yaml
jeap:
  security:
    oauth2:
      resourceserver:
        strict-audience-validation: "on"
```

Use otherwise valid signed `USER` and `SYS` tokens to verify the following audience-related outcomes:

| Token audience | Expected local audience validation |
|---|---|
| Contains the resource's ID, alone or with other intended recipients | Accept |
| Missing | Reject |
| Empty | Reject |
| Nonempty but contains only other resources | Reject |

Exercise real JWT validation rather than injecting an authenticated security context in tests. With
`JwsBuilder`, positive tokens need `withAudiences(...)`; omitting it creates a missing-audience case,
and `withEmptyAudience()` creates an empty-audience case. Include normal and lightweight tokens where
used, forwarding, and an unaddressed recipient. Check that normal API calls still succeed and existing
`B2B` behavior is unchanged.

Roll out to all instances and monitor failures and actual usage before promoting to the next environment.
Working introspection configuration stays in place. Strict audience validation enforcement by a resource
server does not need to wait for the platform to remove Keycloak compatibility exceptions for introspection users.

### Completion and continuing the rollout

**This goal is complete for a resource in an environment** when strict audience validation is `on` and effective
on all of its instances, all intended calls succeed, and the audience rejection tests pass. Repeat for the remaining
resources and environments. The system-wide goal is complete when every applicable resource has reached that state.

Neither goal requires waiting for a future library default change. Keep the explicit `"on"` settings after
migration. Removing the setting later is optional and only appropriate when the deployed component version
demonstrably defaults to `on`, accounting for effective overrides.

## Troubleshooting

| Symptom | What to check |
|---|---|
| API calls fail immediately after adding an audience | Compare `aud` with every recipient's effective `resource-id`; check shared tokens and forwarding. |
| Missing-audience warnings remain | Check resource-scope assignment, explicit requests for optional/dynamic scopes, audience mappers and test-token issuers. Use actual traffic to identify the remaining callers. |
| Lightweight tokens lack `aud` | Check the mapper's **Add to lightweight access token** setting; an audience appearing only in the introspection response is insufficient for strict audience validation by jEAP-based resource servers. |
| Token acquisition returns `invalid_scope` | Compare requested scopes with the calling client's allowed Default/Optional assignments. |
| Introspection returns `invalid_client` | Check the client ID and matching secret, stale configuration overrides and correct Basic-auth encoding of URL-shaped IDs. |
| Introspection returns `active=false` | Check introspection-client audience membership as well as token expiry, revocation and other introspection checks. |
| A negative introspection test succeeds | Check server-wide and client-level compatibility exceptions and OAuth Mock Server overrides. |

Temporarily reverting strict audience validation for a resource server from `on` to `warn` can admit remaining audience-free requests.
It cannot repair a nonempty audience mismatch or a failing introspection request. Similarly, a Keycloak
compatibility exception cannot repair invalid introspection credentials or an audience mismatch.

## Related

- [Audience validation](audience-validation.md) — understand the two different audience checks and their check modes.
- [Naming audiences](audience-naming.md) — choose resource boundaries and identifiers.
- [Configuring audiences in Keycloak](audience-configuration-in-keycloak.md) — apply audience scope and mapper settings.
- [Selecting audiences](audience-selection.md) — configure audiences in token requests.
- [Token introspection on Keycloak](audience-for-token-introspection-on-keycloak.md) — configure introspection clients and compatibility options.
- [Security Starter reference](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-security-starter#audience-validation) — look up resource-server properties.
- [Mock Server configuration](https://jeap-admin-ch.github.io/docs/building-blocks/reusable-microservices/jeap-oauth-mock-server/configuration) — configure DEV clients, token audiences and introspection enforcement.
