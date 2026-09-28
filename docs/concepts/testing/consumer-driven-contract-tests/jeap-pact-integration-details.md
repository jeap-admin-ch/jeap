# jEAP Pact Integration Details

## Pact Broker

Pact tests need access to the Pact Broker. On the one hand, so that the consumer can publish the pact for the provider to the Pact Broker after its tests; on the other hand, so that the provider can download the pacts addressed to it from the Pact Broker and publish the verification results to the Pact Broker after its tests.

The pacts are published via the Pact Maven plugin, i.e. Maven must be able to communicate with the Pact Broker during the consumer build in order to publish pacts. Downloading pacts and publishing verification results is done by the Pact JVM library during the provider's JUnit tests, i.e. the JUnit tests must be able to communicate with the Pact Broker.

In order for Maven or the JUnit tests to communicate with the Pact Broker, the JVMs running the Maven plugin or the JUnit tests must have access to a truststore that contains the Pact Broker's certificate; otherwise the HTTPS connection to the Pact Broker cannot be established.

## Pact Environments

The Pact Broker can be used to register which consumer and provider versions are deployed in which environments. This allows the Pact Broker to provide information about whether a given new consumer or provider version is compatible with the other provider or consumer versions already deployed in a given environment, i.e. whether the new version can be deployed to the environment without causing incompatibility problems ([can-i-deploy](https://docs.pact.io/pact_broker/can_i_deploy)).

## Branches

Pacts and verifications published to the Pact Broker can be associated with the names of the (git) branches whose builds defined the pact or performed the verifications. Branch support means that, for example, collaboration between consumers and providers on new pact requirements can initially take place in relative isolation on feature branches.

### Main Branch

A main branch can be declared in the Pact Broker for each consumer and provider. A main branch should reference the state of a consumer or provider from which the upcoming releases are made. The Pact Broker typically also has providers request the pacts on their consumers' main branches, in order to verify the pacts of upcoming consumer versions in advance, so to speak.

The main branch of a consumer or provider is typically the "master" or "main" branch. If a consumer or provider uses one of these two branches on the Pact Broker, the Pact Broker will automatically assume that branch as the main branch. If this is not the case, the main branch must be set "by hand" once. To do this, the following command can be executed with the [Pact CLI](https://hub.docker.com/r/pactfoundation/pact-cli) on the Pact Broker for, e.g., a consumer or provider "foo" and its main branch "bar":

```bash
pact-broker create-or-update-pacticipant --name foo --main-branch bar
```

The main branch currently configured for a consumer or provider "foo" can be viewed with the following Pact CLI command:

```bash
pact-broker describe-pacticipant --name foo
```

An example of calling the Pact CLI via the Pact Foundation's Docker image:

```bash
docker run --rm -e PACT_BROKER_BASE_URL="base-url" -e PACT_DISABLE_SSL_VERIFICATION=true pactfoundation/pact-cli:latest pact-broker create-or-update-pacticipant --name foo --main-branch bar
```

Warning: for simplicity, certificate verification has been disabled here; for a secure connection to the Pact Broker, the CLI would correctly need to be given the certificate of the CA that issued the Pact Broker's certificate.

## Preconfiguration of Pact by jEAP

Including [jeap-spring-boot-parent](https://github.com/jeap-admin-ch/jeap-spring-boot-parent) in a project also results in a [preconfiguration](https://github.com/jeap-admin-ch/jeap-internal-spring-boot-parent/blob/main/pom.xml) of Pact:

- The Pact Broker is defined as the shared Pact Broker.
- The Pact Broker's Pending Pacts feature is activated.
- The version identifiers of consumers and providers in the Pact Broker are formed from the consumer's or provider's version with the git commit ID appended.
- Every consumer or provider version is associated with the name of its git branch.
- Every verification result is associated with the git branch name of the provider.
- If enabled, the jEAP microservices deploy pipeline registers on the Pact Broker which versions of consumers and providers have been successfully deployed to which environments.
- If enabled, the jEAP microservices deploy pipeline runs a can-i-deploy check on the Pact Broker before a deployment to the ref, abn and prod environments.
- A provider always verifies the following pacts:
  - The latest pacts from consumers on a branch with the same name as the provider branch<br/>→ For collaboration between consumers and providers on feature branches
  - The latest pacts from consumers on their main branch (typically "master")<br/>→ To check the provider's compatibility with the consumers' current "stable" development versions, which may soon be deployed to the environments
  - The pacts of the consumer versions that are currently deployed in the environments<br/>→ To check the provider's compatibility with the older, deployed consumer versions (backward compatibility)

The preconfiguration for the last point, i.e. the configuration of the pacts requested for verification by a provider, may need to be adapted to the specific needs of a project or situation.

For the provider, the preconfiguration is done by defining system properties when running tests with the maven-surefire-plugin. These system properties are read by the Pact JUnit implementation during the tests. When using the default configuration from the jeap-spring-boot-parent project, its configuration values should generally not be overridden by the projects, whether with Java annotations in the code, with configurations in the Maven profile, or by overriding the system properties.

For the consumer, the Pact configuration is done via the configuration of the Pact Maven plugin. Here too, when using the default configuration from the jeap-spring-boot-parent project, no further configuration of the Pact Maven plugin should generally be made.

### Overriding jEAP's Pact Preconfiguration

Sometimes it may be necessary to override the default configuration from jeap-spring-boot-parent. This is particularly the case when the selection of pacts to be verified by a provider needs to be defined explicitly, which can be desirable, for example, if a consumer team and a provider team did not agree in advance on a branch name under which both wanted to develop their changes for a new feature in their respective repositories. In order for a provider to ensure, in such a case, that it consistently verifies the new pact of the consumer required for the feature from the consumer's feature branch in its own feature branch, the provider must explicitly request the pact from the Pact Broker via the consumer branch name. In the default configuration, this would happen automatically if the consumer and provider developed a feature on identically named branches.

To define the pacts requested for verification, so-called Consumer Version Selectors must be specified.

Unfortunately, the current Pact JVM does not yet support the new Consumer Version Selectors of newer Pact Broker versions. However, there is a way to specify the Consumer Version Selectors to be used in the Pact Broker's native JSON format via a `rawjson` system property. This property must be configured with the desired selectors before the test class starts. This can be done, for example, as follows:

```java
@BeforeAll
static void init() {
    System.setProperty("pactbroker.consumerversionselectors.rawjson", "[{\"mainBranch\": true}, {\"deployedOrReleased\": true}, {\"branch\": \"feature/foo\"}]");
}
```

In the example above, the latest pacts of the affected consumers from the main branch and from the branch "feature/foo" would be requested for verification by the provider, as well as the pacts of consumer versions that are currently deployed or released in an environment. "feature/foo" would be the name of the branch on which the consumer is developing its new pact for the provider. The pacts for the main branch and for the deployed and released versions are additionally requested here too (as in the default configuration), so that the provider can determine during its development whether its changes are backward compatible with the currently used consumer versions.

The configuration options supported by the Pact Broker are listed [here](https://docs.pact.io/pact_broker/advanced_topics/consumer_version_selectors).

#### Removing the Override

If the branches requested for verification are overridden in a feature branch, it must generally be ensured that this override no longer applies when merging to develop/master. Whenever possible, an attempt should therefore be made to agree between the consumer and provider on a common branch name under which a new feature is implemented.

## Developing Breaking Provider Changes

If a provider makes a breaking change, its build may fail with an error if its consumers still publish older pacts that the new provider version can no longer satisfy. In such situations, it may become necessary to temporarily check only the pact of the new consumer version for which the breaking change is being developed. The configuration for this case is a special case of the previously described overriding of the Consumer Version Selectors.

```java
@BeforeAll
static void init() {
    System.setProperty("pactbroker.consumerversionselectors.rawjson", "[{\"branch\": \"feature/foo\"}]");
}
```

## Running Provider Tests Directly in IntelliJ as Individual Unit Tests

First, it should be ensured that the Maven profile `cdct-enable-publishing-local` is not activated in IntelliJ, so that local verification runs do not publish their results to the Pact Broker.

The jeap-spring-boot-parent Maven project defines a default configuration of the Pact integration by defining Pact-specific system properties during test execution with the maven-surefire-plugin. By default, IntelliJ automatically takes over such system properties for its own test execution in the IDE (see IntelliJ Setting > Build, Execution, Deployment > Build Tools > Maven > Running Tests). However, certain configuration values for Pact are not defined as constants by the jeap-spring-boot-parent Maven project, but are "computed" during the Maven build. IntelliJ cannot correctly take over these values; they must therefore be defined explicitly if a provider test is to be run in IntelliJ as an individual unit test.

To do this, the `@PactBroker` annotation must be parameterized as follows:

```java
...
@PactBroker(providerBranch = "provider-feature-branch")
class TaskControllerProviderTest {
...
    @BeforeAll
    static void init() {
        System.setProperty("pactbroker.consumerversionselectors.rawjson", "[{\"mainBranch\":true}, {\"matchingBranch\": true}, {\"deployedOrReleased\": true}]");
    }
...
```

where `provider-feature-branch` is the name of the feature branch on which changes to the provider are currently being made. It is assumed here that the provider and the consumer have agreed on a common branch name.

## Debugging Provider Tests Directly in IntelliJ

For local development of a provider, or for its debugging, one often wants to temporarily not verify all consumers, but specifically only the consumer for which an extension is being made, or whose pact verification one wants to debug. This can be achieved with the parameterization of the `@PactBroker` annotation on the provider test shown below. For the parameterization, we assume that `provider-feature-branch` is the name of the feature branch on which changes to the provider are currently being made, and `consumer-feature-branch` is the name of the feature branch on which the consumer has published a new/changed pact. (Ideally, the consumer and provider would agree on a common feature branch name, so that `provider-feature-branch = consumer-feature-branch` would hold). We also assume that the Pending Pacts feature should not be used, so that verification failures do not merely lead to pending failures but to failed tests when the pact cannot be successfully verified by the provider.

```java
...
@PactBroker(enablePendingPacts = "false", providerBranch = "provider-feature-branch")
class TaskControllerProviderTest {
...
    @BeforeAll
    static void init() {
        System.setProperty("pactbroker.consumerversionselectors.rawjson", "[{\"branch\": \"consumer-feature-branch\"}]");
    }
...
```

If the provider test runs successfully with the described parameterization, the `consumerVersionSelectors` should be extended so that the provider's backward compatibility with older (possibly still deployed) consumer versions is also checked.

The Pact Broker configurations overridden for development or debugging in IntelliJ should not be checked in, as they would otherwise also override the jEAP preconfiguration in the builds on the pipeline.

## Fixing Connection Problems with the Pact Provider Mock

The Pact extension for JUnit creates [a new provider mock server](https://github.com/pact-foundation/pact-jvm/blob/master/consumer/README.md#dealing-with-persistent-http11-connections-keep-alive) in consumer tests for each interaction of a pact. As a result, connections to the provider mock server cannot be cached but must always be re-established. If the HTTP client used by the consumer does not do this, test failures occur due to connection problems at the network level (such as "broken pipe"). In tests, this can manifest itself, for example, in only every second test method succeeding, because the HTTP client only re-establishes the connection after an error.

### Pact Mock Server Add-Close-Header

Pact can be configured via the `pact.mockserver.addCloseHeader` property so that the provider mock server signals to the HTTP client in each response that it should close the connection after receiving the response. This property is automatically activated by jEAP via `jeap-spring-boot-parent`. This should resolve the connection problems described, provided the HTTP client used honors the "Connection: close" header in the response.

If connection problems still occur, one of the solutions in the following sections may help.

### Additional HTTP Client Configurations

If necessary, configure the HTTP client used by the tests to disable connection reuse; the setting is client-specific (for example, `http.keepAlive=false` applies to JDK `HttpURLConnection`, not Apache HttpClient).

In at least one case, it also helped to configure the HTTP client to use only HTTP/1.1 and not HTTP/2.

### @DirtiesContext

The Pact consumer test class can be annotated with `@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)` so that the Spring context must be rebuilt after each test method. This also re-instantiates the HTTP client each time, so it cannot cache connections to the Pact provider mock. However, repeatedly rebuilding the Spring context makes test execution slow.

### Switching the HTTP Client

Since the problem is related to the caching behavior of the HTTP client used, using a different HTTP client may solve the problem. For example, Spring's `RestClient` also directly supports the `JdkClient` and the `JettyHttpClient` instead of the Apache HTTP client. However, one generally does not want to commit to a specific HTTP client just because of a testing problem.
