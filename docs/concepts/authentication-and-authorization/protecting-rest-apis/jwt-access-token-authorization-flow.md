# JWT access token authorization flow in jEAP Security

The following diagram shows the flow of an authorization against an OAuth2 access token in jEAP Security.

1. An HTTP request with a JWT bearer token in the HTTP `Authorization` header arrives.
2. The token is processed according to the jEAP Security configuration that the application has set up for the
   specific issuer of the token (`iss` claim), e.g. the configuration for Keycloak vs. the configuration for the
   B2B gateway (see [Integrating different authorization servers](../authorization-servers/integrating-different-authorization-servers.md)).
3. The token is decoded by a `JwtDecoder` configured for the issuer, and its timestamp, signature, audience and
   context are validated.
4. The claims of the token are transformed by the
   [claim set converter](../authorization-servers/integrating-different-authorization-servers.md#transforming-access-tokens-with-claim-set-converters)
   configured for the issuer.
5. The `JwtDecoder` creates a `Jwt` instance from the (transformed) token.
6. The `JeapAuthenticationConverter` creates a jEAP-specific Spring Security token authentication
   (`JeapAuthenticationToken`) from the `Jwt`. The authorities of the authentication are derived from the roles of
   the authentication by a configurable authorities resolver.
7. The authorization check then takes place on the basis of the created authentication. jEAP supports three
   different ways of interpreting the authentication for authorization:
   [semantic roles](rest-api-authorization-with-semantic-roles.md),
   [simple roles](rest-api-authorization-with-simple-roles.md) and
   [authorities](rest-api-authorization-with-authorities.md).

```plantuml
@startuml
hide circle
hide empty members
skinparam packageStyle frame

package "Bearer token" as P1 {
  class "(1) JWT" as JWT {
    userroles
    bproles
    ctx
    login_level
    ext_id
    locale
  }
}

package "JWT decoder" as P2 {
  class "(2) IssuerJwtDecoder" as IJD {
    decode(token)
  }
  class "(3) JwtDecoder" as JD {
    jwkSetUri
    signAlgos
  }
  class "(4) ClaimSetConverter" as CSC
  class "TimestampValidator" as TV
  class "AudienceValidator" as AV
  class "ContextIssuerValidator" as CIV
}
note left of IJD
  Multi-tenancy:
  one JwtDecoder per
  configured issuer
end note

package "Jwt instance" as P3 {
  class "(5) Jwt" as Jwt {
    userroles
    bproles
    ctx
    login_level
    ext_id
    locale
  }
}

package "Authentication converter" as P4 {
  class "(6) JeapAuthenticationConverter" as JAC {
    convert(jwt)
  }
  class "AuthoritiesResolver" as AR {
    deriveAuthoritiesFromRoles(userroles, bproles)
  }
}

package "Authentication" as P5 {
  class "JeapAuthenticationToken" as JAT {
    getUserRoles()
    getBusinessPartnerRoles()
    getJeapAuthenticationContext()
    getTokenAttributes()
    getTokenName()
    getTokenGivenName()
    getToken...()
    getAuthorities()
  }
}

package "(7) Authorization" as P6 {
  class "Semantic role authorization" as SRA {
    hasRole(resource, operation)
    hasRoleForPartner(resource, operation, partner)
    hasRoleForAllPartners(resource, operation)
  }
  class "Simple role authorization" as SIA {
    hasRole(role)
    hasRoleForPartner(role, partner)
    hasRoleForAllPartners(role)
  }
  class "Authorities authorization" as AA {
    hasAuthority(authority)
  }
}

JWT ..> IJD : decoded by
IJD *-- JD : one for every\nconfigured issuer
JD o-right- CSC
JD *-- TV
JD *-- AV
JD *-- CIV
JD ..> Jwt : creates
Jwt ..> JAC : converted by
JAC o-- AR
JAC ..> JAT : creates
JAT ..> SRA : used by
JAT ..> SIA : used by
JAT ..> AA : used by
SRA -[hidden]right- SIA
SIA -[hidden]right- AA
@enduml
```

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Authentication and authorization for REST APIs](rest-api-authentication-and-authorization.md) — integrating jEAP Security into a REST API.
- [Integrating different authorization servers](../authorization-servers/integrating-different-authorization-servers.md) — per-issuer configuration and claim set converters.
- [Tokens in the Blueprint Microservice](../tokens/tokens-in-the-blueprint-microservice.md) — the claims jEAP Security expects in a token.
- [Role concept in the Blueprint Microservice](../role-concept.md) — simple roles, semantic roles and authorities.
- [Authorization with semantic roles](rest-api-authorization-with-semantic-roles.md)
- [Authorization with simple roles](rest-api-authorization-with-simple-roles.md)
- [Authorization with authorities](rest-api-authorization-with-authorities.md)
