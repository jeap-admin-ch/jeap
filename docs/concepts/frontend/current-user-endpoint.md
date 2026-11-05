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

## Enabling and Customizing the Endpoint

**See [How to: enable and customize the current-user endpoint](../../how-tos/rest-apis-and-web/enable-and-customize-current-user-endpoint.md)**
for the steps to activate the endpoint, configure a custom path, and customize the response attributes.

## Examples

- [jme-security-example](https://github.com/jme-admin-ch/jme-security-example/blob/main/README.md)
- [jme-security-oauth2-example](https://github.com/jme-admin-ch/jme-security-oauth2-example/blob/main/README.md)
