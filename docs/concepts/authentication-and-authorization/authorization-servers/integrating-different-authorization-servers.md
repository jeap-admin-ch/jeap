# Integrating different authorization servers

The jEAP Security library relies on the OpenID Connect / OAuth2 standards for the authentication and authorization of
users. Accordingly, the library is in principle compatible with authorization servers implementing these standards.
Within these standards, the jEAP Security library defines a specific [role concept](../role-concept.md) and a matching
[structure of OAuth2 access tokens](../tokens/tokens-in-the-blueprint-microservice.md#access-token). Ideally, the authorization
server in use can be configured to issue access tokens directly in the form expected by the jEAP Security library. As
this is not always possible, the jEAP Security library provides an extension point through which the access tokens
issued by an authorization server can be transformed into the
[format](../tokens/tokens-in-the-blueprint-microservice.md#access-token) expected by the jEAP Security library. This allows the
jEAP Security library to be used together with authorization servers that cannot be configured to issue access tokens
in the format required by the library. The following sections describe how such an authorization server can be
successfully integrated with the jEAP Security library.

## Transforming access tokens with claim set converters

jEAP Security allows configuring one claim set converter each for a configured authorization server or a configured
B2B gateway. With a claim set converter, the claims of an access token can be adapted for further processing by
Spring Security. The adaptations take place *after* the signature of the access token has been validated.

With the help of a claim set converter, access tokens with claims other than those expected by jEAP Security can be
made suitable for jEAP Security. To do so, the claims expected by jEAP Security must be derived from other claims of
the token. For example, the `userroles` claim expected by jEAP Security could be derived from a `role` claim in
tokens issued by a certain authorization server.

The claims jEAP Security expects in a token are described in
[Tokens in the Blueprint Microservice](../tokens/tokens-in-the-blueprint-microservice.md).

### Configuration

A claim set converter for the tokens of an authorization server or B2B gateway is activated with the option
`claim-set-converter-name` in the authorization server or B2B gateway configuration:

| Configuration property | Affected tokens | Configuration | Example |
| --- | --- | --- | --- |
| `jeap.security.oauth2.resourceserver.authorization-server.claim-set-converter-name` | Authorization server | Spring bean name | `eiamClaimSetConverter` |
| `jeap.security.oauth2.resourceserver.auth-servers[n].claim-set-converter-name` | Authorization server at list index `n` | Spring bean name | `eiamClaimSetConverter` |
| `jeap.security.oauth2.resourceserver.b2b-gateway.claim-set-converter-name` | B2B gateway | Spring bean name | `b2bClaimSetConverter` |

### Implementing your own claim set converter

A claim set converter is a normal Spring converter that maps a claim set to a claim set again:

```java
@Component("eiamClaimSetConverter")
public class EiamClaimSetConverter implements Converter<Map<String, Object>, Map<String, Object>> {

    @Override
    public Map<String, Object> convert(Map<String, Object> source) {
        // implementation of the converter
    }

}
```

A claim set converter implementation must be exposed as a Spring bean. The implementation can then be activated with
the configuration properties described above by naming the converter bean (`eiamClaimSetConverter` in the example
above).

The following code shows an example claim set converter implementation
([EiamClaimSetConverter.java](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter/src/main/java/ch/admin/bit/jeap/security/resource/claimsetconverter/EiamClaimSetConverter.java)
in the repository [jeap-spring-boot-starters](https://github.com/jeap-admin-ch/jeap-spring-boot-starters)). The implementation adapts the claims of an access token issued by
an authorization server (called eIAM) to jEAP Security by
- renaming the `role` claim to `userroles`
- renaming the `userExtId` claim to `ext_id`
- mapping the `language` claim to the `locale` claim
- setting the `ctx` claim to `USER` (assuming the authorization server eIAM only manages users (no systems))

```java
package ch.admin.bit.jeap.security.resource.claimsetconverter;

import org.springframework.lang.NonNull;

import java.util.HashMap;
import java.util.Map;

public class EiamClaimSetConverter extends AbstractClaimSetConverter {

    @Override
    public Map<String, Object> doConvert(@NonNull Map<String, Object> claims) {
        Map<String, Object> mappedClaims = new HashMap<>(claims);
        renameClaim("role", "userroles", mappedClaims);
        renameClaim("userExtId", "ext_id", mappedClaims);
        mapClaim("language", "locale", mappedClaims,
                language -> language.toString().toUpperCase());
        mappedClaims.put("ctx", "USER");
        return mappedClaims;
    }

}
```

The following configuration shows an example of activating this claim set converter
([application-local.yml](https://github.com/jme-admin-ch/jme-security-oauth2-example/blob/main/jme-security-oauth2-resource-authorities-service/src/main/resources/application-local.yml)
in the repository [jme-security-oauth2-example](https://github.com/jme-admin-ch/jme-security-oauth2-example)):

```yaml
jeap:
  security:
    oauth2:
      resourceserver:
        authorization-server:
          issuer: "http://localhost:8081/jme-security-oauth2-auth-scs"
          jwk-set-uri: "${jeap.security.oauth2.resourceserver.authorization-server.issuer}/.well-known/jwks.json"
          claim-set-converter-name: eiamClaimSetConverter
```

When using the `auth-servers` configuration option, configure a claim set converter name separately on each list entry.
Each entry can reference a different converter bean, or several entries can reference the same bean:

```yaml
jeap:
  security:
    oauth2:
      resourceserver:
        auth-servers:
          - issuer: https://issuer-one.example.ch
            jwk-set-uri: https://issuer-one.example.ch/jwks
            claim-set-converter-name: firstClaimSetConverter
          - issuer: https://issuer-two.example.ch
            jwk-set-uri: https://issuer-two.example.ch/jwks
            claim-set-converter-name: secondClaimSetConverter
```

## Related

- [Authentication and authorization](../index.md) — the overview of authentication and authorization in jEAP: authentication contexts, functional and data authorization, OpenID Connect and OAuth2.
- [Tokens in the Blueprint Microservice](../tokens/tokens-in-the-blueprint-microservice.md) — the claims jEAP Security expects in an access token.
- [Role concept in the Blueprint Microservice](../role-concept.md) — the role model behind the `userroles` and `bproles` claims.
- [Authentication and authorization for REST APIs](../protecting-rest-apis/rest-api-authentication-and-authorization.md) — configuring authorization servers and B2B gateways in the jEAP Security Starter.
- [Keycloak](keycloak.md) — the authorization server whose tokens jEAP Security processes without a converter.
- [OpenID Connect / OAuth2 mock server](../testing/oauth2-mock-server.md) — issuing tokens in local development.
