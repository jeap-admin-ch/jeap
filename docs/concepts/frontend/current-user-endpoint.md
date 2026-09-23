# Current-User Endpoint

The **jEAP Security Starter** includes an endpoint that retrieves user information and authorizations based on the provided **bearer token**. It returns this data in a standardized JSON format. This endpoint is primarily intended to be used by frontends to access token details without needing to parse the token in the frontend.

## Content

Here are the attributes that are returned in the response by the endpoint. Only non-empty values are returned. The only attribute that is always present is the subject.

| Name | Corresponding claim from token |
| --- | --- |
| subject | sub |
| name | name |
| preferredUsername | preferred_username |
| familyName | family_name |
| givenName | given_name |
| locale | locale |
| authenticationContextClassReference | ac |
| authenticationMethodsReferences | amr |
| adminDirUid | admin_dir_uid |
| userExtId | ext_id |
| userRoles | userroles |
| businessPartnerRoles | bproles |
| pamsLoginLevel | login_level |

The following is a complete example of a JSON response:

```js
{
	"subject": "subject",
	"name": "name",
	"preferredUsername": "preferredUsername",
	"familyName": "familyName",
	"givenName": "givenName",
	"locale": "locale",
	"authenticationContextClassReference": "1",
	"authenticationMethodsReferences": [
        "pwd",
		"otp"
	],
	"adminDirUid": "adminDirUID",
	"userExtId": "extId",
	"userRoles": [
		"my-user-role"
	],
	"businessPartnerRoles": {
		"12345789": [
			"jme_@thing_#read",
			"jme_@partner_#read"
		]
	},
	"pamsLoginLevel": "loginLevel"
}
```

## Configuration

By default, this endpoint is not active. To activate this endpoint, the following property must be configured:

```yaml
jeap:
  security:
    oauth2:
      current-user-endpoint:
        enabled: true
```

By default, this endpoint is accessible via the designated path **/api/current-user**.

It is possible to configure another path with the following property:

```yaml
jeap:
  security:
    oauth2:
      current-user-endpoint:
        path: /api/custom-path
```

## Customization

The response content can be customized by adding or removing attributes. This requires defining a new DTO and a Customizer to create it.

The custom DTO must extend the `JeapCurrentUserDto` class, introducing new attributes while calling the superclass constructor. Existing attributes can be removed by setting them to `null`, except for the required `subject` attribute, which cannot be null.

In this example, a new attribute `myCustomAttribut` is added, while `adminDirUid` and `pamsLoginLevel` are set to `null`, excluding them from the response.

```java
@Data
public class JmeCurrentUserDto extends JeapCurrentUserDto {

    String myCustomAttribut;

    public JmeCurrentUserDto(JeapCurrentUser jeapCurrentUser, String myCustomAttribut) {
        super(jeapCurrentUser);
        this.myCustomAttribut= myCustomAttribut;
		setAdminDirUid(null);
        setPamsLoginLevel(null);
    }
}
```

This DTO can be constructed in the Customizer class. This class must implement the `JeapCurrentUserCustomizer` interface and be instantiated as a Spring bean.

```java
public interface JeapCurrentUserCustomizer<T extends JeapCurrentUser> {

    T customize(JeapCurrentUser jeapCurrentUser);

}
```

Example of an implementation:

```java
@org.springframework.stereotype.Component
public class JmeCurrentUserCustomizer implements JeapCurrentUserCustomizer<JmeCurrentUserDto> {

    @Override
    public JmeCurrentUserDto customize(JeapCurrentUser jeapCurrentUser) {
        return new JmeCurrentUserDto(jeapCurrentUser, "fooBar");
    }
}
```

## Examples

- [jme-security-example](https://github.com/jme-admin-ch/jme-security-example/blob/main/README.md)
- [jme-security-oauth2-example](https://github.com/jme-admin-ch/jme-security-oauth2-example/blob/main/README.md)
