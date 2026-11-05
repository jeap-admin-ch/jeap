# How to: write a Pact consumer test

A Pact consumer test is a normal JUnit test that records the requests a consumer sends and the
responses it expects, so Pact can generate a contract (a "pact") for the provider to verify against.

## Steps

### 1. Add the Pact dependencies

Maven parent: As always, use the latest `jeap-spring-boot-parent`.

```xml title="pom.xml"
...
	<parent>
		<groupId>ch.admin.bit.jeap</groupId>
		<artifactId>jeap-spring-boot-parent</artifactId>
		<version>41.10.0</version> <!-- use the latest version -->
        <relativePath/> <!-- lookup parent from repository -->
	</parent>
...
```

Maven dependencies:

```xml title="pom.xml"
<dependencies>
...
	<dependency>
    	<groupId>au.com.dius.pact.consumer</groupId>
        <artifactId>junit5</artifactId>
        <scope>test</scope>
        <!-- version managed by jeap parent -->
    </dependency>
...
</dependencies>
```

Maven plugins when using `jeap-spring-boot-parent` version >= 28.0.1:

```xml title="pom.xml"
<plugins>
...
	<plugin>
    	<groupId>au.com.dius.pact.provider</groupId>
        <artifactId>maven</artifactId>
         <!-- version managed by jeap parent -->
	</plugin>
...
</plugins>
```

Maven plugins when using `jeap-spring-boot-parent` version < 28.0.1:

```xml title="pom.xml"
<plugins>
...
	<plugin>
    	<groupId>au.com.dius.pact.provider</groupId>
        <artifactId>maven</artifactId>
         <!-- version managed by jeap parent -->
        <executions>
        	<!-- The actual publishing of pacts to the pact broker depends on a profile,
			 and gets activated in jeap pipeline builds by default. -->
         	<execution>
            	<phase>install</phase>
                <goals>
                	<goal>publish</goal>
                </goals>
			</execution>
		</executions>
	</plugin>
...
</plugins>
```

### 2. Annotate the consumer test class

A Consumer Pact Test is a normal JUnit test.

The annotations mentioned below are only those concerning pacts. Additional JUnit or jEAP-Security specific ones can be seen in the example → [TaskClientConsumerPactTest.java - jme-cdct-consumer-example](https://github.com/jme-admin-ch/jme-cdct-consumer-example/blob/main/src/test/java/ch/admin/bit/jeap/jme/cdct/consumer/web/api/gateway/TaskClientConsumerPactTest.java)

```java title="ConsumerTest"
@PactConsumerTest
@PactTestFor(pactVersion = PactSpecVersion.V4)
@MockServerConfig(hostInterface = "localhost", port = "8888")
class ConsumerPactTest {
...
```

- `@PactConsumerTest`: Indicates that this class contains Pact consumer tests.
- `@PactTestFor`: Specifies the version of the Pact specification to be used.
- `@MockServerConfig`: Configures the mock server provided by Pact.

### 3. Define the Pact interactions

- Methods annotated with `@Pact` define interactions between the consumer and provider using the Pact DSL.
- Each method specifies a given provider state, an interaction (request/response), and returns a Pact object.
- Interactions defined in the jme-cdc-example-consumer include requesting a task by ID, requesting multiple tasks, handling insufficient authorization, etc.

:::warning
There seems to be a bug in the Pact JUnit extension when constructor injection is used on the test class which results in the Pact extension not picking up the `@Pact` annotations on methods defining interactions. Use field injection instead.
:::

```java title="Pact Interaction Method Example"
@Pact(provider = PROVIDER, consumer = CONSUMER)
    private V4Pact requestTaskWithFixedIdTaskBeingPresentInteraction(PactBuilder builder) {
    final String path = API_PATH + "/1";
    return builder.
            given("A task with task id '1' is present").
            expectsToReceiveHttpInteraction("A GET request to " + path, httpInteractionBuilder ->  httpInteractionBuilder.
                withRequest(httpRequestBuilder -> httpRequestBuilder.
                    header(HttpHeaders.AUTHORIZATION, "Bearer " + taskReadToken).
                    method("GET").
                    path(path)).
                willRespondWith(httpResponseBuilder -> httpResponseBuilder.
                    status(200).
                    header("Content-Type", "application/json").
                    body(
                        newJsonBody(o -> {
                            o.stringValue(ID_FIELD_NAME, "1");
                            o.stringType(TITLE_FIELD_NAME, TITLE_EXAMPLE_VALUE);
                            o.stringType(CONTENT_FIELD_NAME, CONTENT_EXAMPLE_VALUE);
                        }).
                    build()))).
            toPact();
    }
```

### 4. Write the test method

- Test methods annotated with `@Test` execute consumer Pact tests for the interactions defined (in the example above the interaction is defined by the method with the name **requestTaskWithFixedIdTaskBeingPresentInteraction**)
- Each test method references an `@Pact` annotated method and asserts the corresponding interaction.

```java title="Test Method Example"
@Test
    @PactTestFor(pactMethod = "requestTaskWithFixedIdTaskBeingPresentInteraction")
    void testGetTaskByIdWithFixedIdTaskBeingPresent() {
        mockRestClientBuilderFactory.getAuthTokenProvider().setAuthToken(taskReadToken);

        Task result = taskClient.getTaskById("1");

        assertTaskValues(result, "1",TITLE_EXAMPLE_VALUE, CONTENT_EXAMPLE_VALUE);
    }
```

The interested reader may have noticed that authentication is integrated in these two example methods. This requires some additional configuration which can be seen in the examples → [jme-cdct-consumer-example](https://github.com/jme-admin-ch/jme-cdct-consumer-example) and [TaskClientConsumerPactTest.java](https://github.com/jme-admin-ch/jme-cdct-consumer-example/blob/main/src/test/java/ch/admin/bit/jeap/jme/cdct/consumer/web/api/gateway/TaskClientConsumerPactTest.java#L40). Alternatively, aspects of authentication might also be covered using provider states.

## Related

- [Consumer-Driven Contract Tests](../../concepts/testing/consumer-driven-contract-tests/index.md) — motivation, big picture and the Pact Broker concepts behind this procedure.
- [How to: write a Pact provider test](write-a-pact-provider-test.md)
- [jme-cdct-consumer-example](https://github.com/jme-admin-ch/jme-cdct-consumer-example)
