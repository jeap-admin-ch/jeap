# How to: prune roles from access tokens with the Jeap Roles Pruning Token Mapper

The jEAP Keycloak plugin's Jeap Roles Pruning Token Mapper removes the `userroles` and `bproles` claims
from a token if the number of characters used by those claims exceeds a configured limit, adding the
`roles_pruned_chars` claim with the number of characters the pruned claims would have used. Use it to cap
the size of access tokens for users with more roles than should fit in a token.

## Steps

1. Add the Jeap Roles Pruning Token Mapper to the client, either on the client's dedicated scope (for a
   per-client limit) or on a shared optional scope assigned to several clients (for a realm-wide limit).
   See [Token introspection: roles pruning](../../concepts/authentication-and-authorization/tokens/token-introspection.md#roles-pruning)
   for the mapper's required activation switches.

2. Set the mapper's configuration option for the maximum allowed accumulated number of characters in the
   `userroles` and `bproles` claims. The default is `8000`.

   Size the limit against your platform's actual constraint on the token, keeping in mind that:

   - A JWT first UTF-8-encodes its claims and then Base64-encodes the result. UTF-8 encoding uses more
     than one byte per character for non-ASCII characters, and Base64 encoding adds one third to the
     encoded size.
   - The default limit of 8000 characters therefore translates to 10666 bytes in the access token if the
     roles only use ASCII characters, plus more if the roles contain non-ASCII characters.
   - Without the roles, a standard access token is usually smaller than 2KB. So the default limit of 8000
     characters for roles should result in tokens that are still noticeably smaller than 16KB even with
     some non-ASCII characters in roles — 16KB being the limit AWS puts on the size of an HTTP header
     field, and therefore on access tokens transferred as bearer tokens.

3. Make sure a resource that may receive pruned tokens can still resolve the pruned roles: configure it
   with the jEAP Security library's introspection mode `lightweight` (or `always`) so it fetches the roles
   from the Keycloak token introspection endpoint when they are missing from the token. See
   [How to: enable and debug jEAP token introspection](enable-and-debug-token-introspection.md).

## Related

- [Minimizing access token sizes](../../concepts/authentication-and-authorization/tokens/minimizing-access-token-sizes.md) — why access tokens get large and the other available size-reduction options.
- [Token introspection](../../concepts/authentication-and-authorization/tokens/token-introspection.md) — introspection modes and the roles-pruning mapper's activation switches on a client.
- [How to: enable and debug jEAP token introspection](enable-and-debug-token-introspection.md)
- [How to: use lightweight access tokens](use-lightweight-access-tokens.md)
- [How to: use dynamic OAuth2 scopes](use-dynamic-oauth2-scopes.md)
