# Feature Flags

## Guide

Consider the following scenario: the application is in production, but development of the system isn't finished yet. In production operation, current bugs have priority. At the same time, the team is also working on several new features. Some of these features are small and can easily be merged into `develop`/`master` for the next release. But it may be that a feature must not or should not go into the next release yet. This can have various reasons:

- Surrounding systems aren't "ready" yet
- Users haven't been informed/trained yet
- A law/regulation only takes effect on a certain date
- etc...

Since we work with a trunk-based Git workflow (DEVELOP and MASTER branches), the later a feature branch is merged, the more likely a merge hell becomes.

One approach to this is the feature flag (or feature toggle) pattern. The idea is simple: separate deployment from release. Based on a certain configuration, the feature is turned on or off.

A feature flag is essentially a boolean (true, false) that's checked at certain points in the application. The application must behave differently accordingly.

A feature flag only makes sense if the state can be changed without redeploying the application, i.e. at runtime. For this reason, we need to separate the configuration from the application and have a means for the application to become aware of configuration changes. For this, we use config providers (ConfigMaps, AWS AppConfig, ...), which manage the configurations that can be changed at runtime and, where applicable, inform the clients about it.

## Using Feature Flags

The jeap-spring-boot-featureflag-starter uses the feature flag library Togglz. Alternatively, the plain Spring Boot tools (`@RefreshScope`, `@ConditionalOnProperty`, `@ConfigurationProperties`, ...) can also simply be used.

Docs: [https://www.togglz.org/](https://www.togglz.org/)

Source code: [https://github.com/togglz/togglz](https://github.com/togglz/togglz)

This library is added via the required `jeap-spring-boot-featureflag-starter` dependency.

### Configuration

In the configuration files, feature flags must be defined under `togglz.features`:

```yaml
togglz:
  features:
    MY_FIRST_FEATURE_FLAG:
      enabled: false
    MY_SECOND_FEATURE_FLAG:
      enabled: true
```

### Client

#### Integration

The following dependency enables working with feature flags:

```xml
<dependency>
	<groupId>ch.admin.bit.jeap</groupId>
	<artifactId>jeap-spring-boot-featureflag-starter</artifactId>
</dependency>
```

For the feature flags prepared in the configuration (ConfigMap, AWS AppConfig, ...), you can create an enum in the client application to make the feature flags type-safe. Please observe the [Naming Conventions for Feature Flags](#naming-conventions-featureflags).

```java
public enum FeatureFlags implements org.togglz.core.Feature {

	BUSINESS_MICROSERVICE_A_PROJECT_1234_DECLARATION_CALCULATION,

	BUSINESS_MICROSERVICE_B_PROJECT_2342_ROUTE_CALCULATION;

	public boolean isActive() {
		return FeatureContext.getFeatureManager().isActive(this);
	}
}
```

#### Usage in Application Logic

The use of these feature flag enums in the application logic can vary widely and must be considered case by case.

if-then variant:

```java
if (FeatureFlags.BUSINESS_MICROSERVICE-A_PROJECT_1234_DECLARATION_CALCULATION.isActive()) {
	return FeatureFlags.BUSINESS_MICROSERVICE_A_PROJECT_1234_DECLARATION_CALCULATION.name() + " is active";
}
else {
 	return FeatureFlags.BUSINESS_MICROSERVICE_A_PROJECT_1234_DECLARATION_CALCULATION.name() + " is not active";
}
```

Swapping variant services:

```java
@Configuration
public class AppConfig {

@Bean
public SomeService oldSomeService() {
	return new OldSomeServiceImpl();
}

@Bean
public SomeService newSomeService() {
	return new NewSomeServiceImpl();
}

@Bean
public FeatureProxyFactoryBean proxiedSomeService() {
	FeatureProxyFactoryBean proxyFactoryBean = new FeatureProxyFactoryBean();
	proxyFactoryBean.setFeature(FeatureToggles.USE_NEW_SOMESERVICE.name());
	proxyFactoryBean.setProxyType(SomeService.class);
	proxyFactoryBean.setActive(this.newSomeService());
	proxyFactoryBean.setInactive(this.oldSomeService());
	return proxyFactoryBean;
}

@Bean
@Primary
public SomeService someService(@Autowired FeatureProxyFactoryBean proxiedSomeService) throws Exception {
return (SomeService) proxiedSomeService.getObject();
}
//...
}
```

### Activation Strategies

Togglz defines the concept of activation strategies. They're responsible for deciding whether an enabled feature is actually active. Activation strategies can, for example, be used to activate features only for certain users, for certain client IPs, or at a certain point in time.

In the config itself, we define this feature flag as follows:

```yaml
MY_CUSTOM_FLAG:
  enabled: true
  strategy: "roleBasedActivationStrategy"
  param:
    allowedRole: "jme_@myCustomFlag_#read"
```

strategy: must refer to the concrete implementation of an `ActivationStrategy`.

param: arbitrary parameters can be passed here. As an example, we pass the string `"jme_@myCustomFlag_#read"` under the key `allowedRole`. The name `allowedRole` has nothing to do with the Togglz library; it was chosen by the developer of the `roleBasedActivationStrategy` itself.

The following example shows a strategy for activation depending on the jEAP security role. For the strategy to be found, the class must be listed in `src/main/resources/META-INF/services/org.togglz.core.spi.ActivationStrategy`.

```java
package ch.admin.jeap.example.config.client;

import org.togglz.core.activation.Parameter;
import org.togglz.core.activation.ParameterBuilder;
import org.togglz.core.repository.FeatureState;
import org.togglz.core.spi.ActivationStrategy;
import org.togglz.core.user.FeatureUser;

import java.util.Set;

/**
 * Example for a Role Based Activation Strategy
 *
 * The config could look like this:
 *
 * MY_CUSTOM_FLAG:
 *   enabled: true
 *   strategy: "roleBasedActivationStrategy"
 *   param:
 *     allowedRole: "jme_@myCustomFlag_#read"
 *
 * Remark: The Params like 'allowedRole' are free to define. You can
 * choose a fantasy name, and you get that value on the FeatureState Object.
 *
 */
public class RoleBasedActivationStrategy implements ActivationStrategy {

    private static final String ROLES = "roles";
    private static final String ALLOWED_ROLE = "allowedRole";
    private static final String ALLOWED_ROLE_DESCRIPTION = "User role that activates the flag when present";

    private static final String ROLE_PREFIX = "ROLE_";

    public static final String ID = "roleBasedActivationStrategy";
    public static final String NAME = "My activation strategy example";

    @Override
    public String getId() {
        return ID;
    }

    @Override
    public String getName() { return NAME; }

    /**
     * Simple example for a custom activation strategy implementation:
     * Checks if the User has the 'allowedRole', which is a parameter in the featureState.
     *
     * @param featureState the object contains the config from the configuration provider
     * @param user Contains the roles of the logged-in user
     * @return true if the FeatureFlag is Active, false if not
     */
    @Override
    @SuppressWarnings("unchecked")
    public boolean isActive(FeatureState featureState, FeatureUser user) {
        Set<String> roleList;
        try {
            roleList = (Set<String>) user.getAttribute(ROLES);
        } catch (ClassCastException e) {
            return false;
        }
        // Here we get the value of our in the config freely defined parameter 'allowedRole'
        String allowedRole = ROLE_PREFIX + featureState.getParameter(ALLOWED_ROLE);
        return roleList != null && roleList.contains(allowedRole);
    }

    @Override
    public Parameter[] getParameters() {
        return new Parameter[] {
                ParameterBuilder.create(ALLOWED_ROLE).label(ALLOWED_ROLE_DESCRIPTION)
        };
    }
}
```

## Naming Conventions FeatureFlags

| When | Naming convention | Example | Notes |
| --- | --- | --- | --- |
| Feature flag name | `<<Jira Key>>_<<MEANINGFUL_NAME>>` ⟹ `<<FEATURE FLAG NAME>>` | PROJECT_1234_DECLARATION_CALCULATION | A feature flag name must always include the relevant Jira key. |
| When used by multiple business applications | `<<FEATURE FLAG NAME>>` | BUSINESS_2344_DECLARATION_CALCULATION_2022 | A feature flag used in multiple business applications does not include the name of the business application. |
| Only one business application, but multiple microservices | `<<BUSINESS APPLICATION>><<FEATURE FLAG NAME>>` | BUSINESS_PROJECT_1234_DECLARATION_CALCULATION | If a feature flag is intended for multiple microservices within one business application. |
| Only one business application and one microservice | `<<BUSINESS APPLICATION>>_<<MICROSERVICE NAME>>_<<FEATURE FLAG NAME>>` | BUSINESS_MICROSERVICE_A_PROJECT_1234_DECLARATION_CALCULATION | If a feature flag is intended for exactly one microservice. |
