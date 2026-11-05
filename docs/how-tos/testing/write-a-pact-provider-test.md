# How to: write a Pact provider test

A Pact provider test downloads the pacts recorded by consumers from the Pact Broker and verifies the
provider's real behavior against each of them.

## Steps

### 1. Add the Pact dependencies

Maven parent: As always, use the latest `jeap-spring-boot-parent`.

Maven dependencies:

:::info
Where we need the `au.com.dius.pact.provider`, **NOT** `au.com.dius.pact.consumer`
:::

```xml title="pom.xml"
<dependencies>
...
	<dependency>
    	<groupId>au.com.dius.pact.provider</groupId>
        <artifactId>junit5</artifactId>
        <scope>test</scope>
        <!-- version managed by jeap parent -->
    </dependency>
...
</dependencies>
```

### 2. Annotate the provider test class

```java title="ProviderTest"
@Provider("bit-jme-cdc-provider-service")
@PactBroker
@AllowOverridePactUrl 
@IgnoreNoPactsToVerify
class ProviderPactTest {
...
```

- `@Provider`: Specifies the provider name for Pact verification.
- `@PactBroker`: Indicates that the pacts will be fetched from a Pact Broker.
- `@AllowOverridePactUrl`: Allows externally specified pact URL to override other consumer version selectors. Needed to support the automatic verification of changed pacts.
- `@IgnoreNoPactsToVerify`: Ignores the absence of pacts to verify. Useful for new providers that do not yet have any consumers specifying pacts.

### 3. Implement the pact-verification test method

This will verify this provider against all the pacts defined in the Pact Broker for this provider.

```java
@TestTemplate
@ExtendWith(PactVerificationInvocationContextProvider.class)
void testPacts(PactVerificationContext context) {
	// If there are no pacts there will be no context.
    if (context != null) {
    	context.verifyInteraction();
    }
}
```

### 4. Implement the provider state methods

Some (most) interactions need the provider to be in a certain state for a successful test of the interaction. For each such provider state a method needs to be implemented by the provider that puts the provider in the required state. These states correspond to the provider states defined in the consumer pact files. The provider has to coordinate the definition of the provider states required by its consumers, and the states (with their properties) must be part of the provider's documentation.

Example: The following method implements the provider state associated with the name "A task with task id '1' is present". The provider state names defined in the provider and the state names used by the consumers in their interaction specifications must match exactly (see the Pact interaction method example in [How to: write a Pact consumer test](write-a-pact-consumer-test.md)).

```java
@State("A task with task id '1' is present")
void initStateTaskWithId1Present() {
	createTaskWithId("1", "Task with id 1", "Do this and that", "private", ZonedDateTime.now());
}
```

Example: [Source of TaskControllerProviderTest.java](https://github.com/jme-admin-ch/jme-cdct-provider-example/blob/main/jme-cdct-provider-service/src/test/java/ch/admin/bit/jeap/jme/cdct/provider/web/api/example/TaskControllerProviderTest.java)

## Related

- [Consumer-Driven Contract Tests](../../concepts/testing/consumer-driven-contract-tests/index.md) — motivation, big picture, provider states and the Pact Broker concepts behind this procedure.
- [How to: write a Pact consumer test](write-a-pact-consumer-test.md)
- [jme-cdct-provider-example](https://github.com/jme-admin-ch/jme-cdct-provider-example)
