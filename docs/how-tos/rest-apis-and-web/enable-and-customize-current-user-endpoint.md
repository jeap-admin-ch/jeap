# How to: enable and customize the current-user endpoint

The **jEAP Security Starter**'s current-user endpoint returns user information and authorizations from the bearer token as JSON, for frontends that want this data without parsing the token themselves. See [Current-User Endpoint](../../concepts/frontend/current-user-endpoint.md) for the full attribute reference.

## Steps

1. Enable the endpoint, which is inactive by default:

```yaml
jeap:
  security:
    oauth2:
      current-user-endpoint:
        enabled: true
```

   The endpoint is then accessible via the default path **/api/current-user**.

2. (Optional) Configure a custom path instead:

```yaml
jeap:
  security:
    oauth2:
      current-user-endpoint:
        path: /api/custom-path
```

3. (Optional) To add or remove attributes from the response, define a custom DTO. It must extend the `JeapCurrentUserDto` class, introducing new attributes while calling the superclass constructor. Existing attributes can be removed by setting them to `null`, except for the required `subject` attribute, which cannot be null.

   In this example, a new attribute `myCustomAttribute` is added, while `adminDirUid` and `pamsLoginLevel` are set to `null`, excluding them from the response.

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

4. Construct the custom DTO in a Customizer class. This class must implement the `JeapCurrentUserCustomizer` interface and be instantiated as a Spring bean.

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

## Related

- [Current-User Endpoint](../../concepts/frontend/current-user-endpoint.md) — the full response attribute reference and example JSON response.
