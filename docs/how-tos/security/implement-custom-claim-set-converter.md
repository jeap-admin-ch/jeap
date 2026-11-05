# How to: implement a custom claim set converter

Implement this when an authorization server or B2B gateway issues access tokens whose claims don't
match the [format jEAP Security expects](../../concepts/authentication-and-authorization/tokens/tokens-in-the-blueprint-microservice.md#access-token),
so the claims expected by jEAP Security must be derived from the claims actually present in the token.

## Steps

1. Implement a Spring converter that maps a claim set to another claim set, and expose it as a Spring
   bean:

   ```java
   @Component("eiamClaimSetConverter")
   public class EiamClaimSetConverter implements Converter<Map<String, Object>, Map<String, Object>> {

       @Override
       public Map<String, Object> convert(Map<String, Object> source) {
           // implementation of the converter
       }

   }
   ```

2. Implement the claim mapping logic. The following example
   ([EiamClaimSetConverter.java](https://github.com/jeap-admin-ch/jeap-spring-boot-starters/blob/main/jeap-spring-boot-security-starter/src/main/java/ch/admin/bit/jeap/security/resource/claimsetconverter/EiamClaimSetConverter.java)
   in the repository [jeap-spring-boot-starters](https://github.com/jeap-admin-ch/jeap-spring-boot-starters)) adapts the claims of an access token issued by an
   authorization server (called eIAM) to jEAP Security by
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

3. Activate the converter by naming its bean in the authorization server or B2B gateway configuration
   with the `claim-set-converter-name` property. The following example
   ([application-local.yml](https://github.com/jme-admin-ch/jme-security-oauth2-example/blob/main/jme-security-oauth2-resource-authorities-service/src/main/resources/application-local.yml)
   in the repository [jme-security-oauth2-example](https://github.com/jme-admin-ch/jme-security-oauth2-example)) activates the converter from step 2:

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

4. When using the `auth-servers` configuration option, configure a claim set converter name separately on
   each list entry. Each entry can reference a different converter bean, or several entries can reference
   the same bean:

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

- [Integrating different authorization servers](../../concepts/authentication-and-authorization/authorization-servers/integrating-different-authorization-servers.md) — what a claim set converter is and the `claim-set-converter-name` configuration property reference.
- [Tokens in the Blueprint Microservice](../../concepts/authentication-and-authorization/tokens/tokens-in-the-blueprint-microservice.md) — the claims jEAP Security expects in an access token.
- [How to: call a secured REST API from Java](call-a-secured-rest-api-from-java.md) — the client side of calling a REST API protected by jEAP Security.
