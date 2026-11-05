# How to: use lightweight access tokens with Keycloak

Starting with Keycloak version 24, a token mapper switch "**Add to lightweight access token**" lets you
control which information a lightweight access token carries, separately from the regular "**Add to
access token**" switch. By default, this switch is off for most standard mappers, so a lightweight access
token contains only minimal information.

## Steps

1. Enable the mappers that must still contribute to lightweight access tokens. By default, most token
   mappers do not add their claim to lightweight access tokens, which is the intended purpose. If you
   require specific information to be included (e.g. subject, given name, family name, locale, certain
   IDs, etc.), enable the "Add to lightweight access token" switch on the mappers that provide this
   information — these are typically located in the default scope `profile`. If the token is going to be
   processed by the jEAP security library, also enable it on the mapper providing the `ctx` claim, since the
   library validates whether an issuer is authorized to authenticate clients in that context.

2. Choose how a client gets issued lightweight access tokens, either:

   - **Always for this client** — in the client's configuration, navigate to the "Advanced" tab in the
     "Advanced Settings" section and set the option "**Always use lightweight access token**" to "on"; or
   - **A client profile applied via a client policy** — apply a **client profile** containing the
     **executor** "**use-lightweight-access-token**" to a client via a **client policy** configured in the
     "Realm settings" in the "Client policies" tab.

3. For the flexible, opt-in alternative, where a client decides per authentication request whether it
   needs a lightweight access token, set up a client profile driven by an optional scope:

   - Create a new *optional* scope `lightweight-access-token`.
     - Set the option "Include in token scope" to `on`.
   - Create a new client profile `lightweight-access-token-profile`.
     - Add the executor `use-lightweight-access-token` to the profile.
   - Create a new client policy `lightweight-access-token-policy`.
     - Add a condition of type `client-scopes` to the policy.
       - Configure the `expected scopes` option with the `lightweight-access-token` scope as an *optional*
         scope.
     - Add the profile `lightweight-access-token-profile` to the policy.
   - Add the scope `lightweight-access-token` as *optional* scope to the client that should be able to
     fetch a lightweight access token.
   - When making an authentication request to Keycloak with the client, include the scope
     `lightweight-access-token` in the request's `scope` parameter.

   By including or excluding the `lightweight-access-token` scope in an authentication request, the client
   can choose whether to request a lightweight access token or not.

With lightweight access tokens, token mappers can be activated on a client for the introspection endpoint
but not for access tokens. If the mappers adding a user's authorizations (roles) are not activated on
lightweight access tokens for a client, the access tokens issued to that client will contain only limited
user information — in particular, they won't contain the user's authorizations. A client using such a
token must have the resource query the Keycloak token introspection endpoint to retrieve them; see
[Token introspection](../../concepts/authentication-and-authorization/tokens/token-introspection.md).

## Related

- [Minimizing access token sizes](../../concepts/authentication-and-authorization/tokens/minimizing-access-token-sizes.md) — why access tokens get large and the other available size-reduction options.
- [Token introspection](../../concepts/authentication-and-authorization/tokens/token-introspection.md) — resolving a lightweight token's authorizations at the authorization server, and caching introspection results.
- [How to: enable and debug jEAP token introspection](enable-and-debug-token-introspection.md)
- [How to: use dynamic OAuth2 scopes](use-dynamic-oauth2-scopes.md)
- [How to: prune roles from access tokens](prune-roles-from-access-tokens.md)
