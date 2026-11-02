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

The jeap-spring-boot-featureflag-starter uses the feature flag library [Togglz](https://www.togglz.org/).
Alternatively, the plain Spring Boot tools (`@RefreshScope`, `@ConditionalOnProperty`,
`@ConfigurationProperties`, ...) can also simply be used.

**For adding the dependency, defining and checking flags, and writing a custom activation strategy, see
[jeap-spring-boot-featureflag-starter](https://jeap-admin-ch.github.io/docs/building-blocks/spring-boot-starters/jeap-spring-boot-starters/jeap-spring-boot-featureflag-starter).**

## Naming Conventions FeatureFlags

| When | Naming convention | Example | Notes |
| --- | --- | --- | --- |
| Feature flag name | `<<Jira Key>>_<<MEANINGFUL_NAME>>` ⟹ `<<FEATURE FLAG NAME>>` | PROJECT_1234_DECLARATION_CALCULATION | A feature flag name must always include the relevant Jira key. |
| When used by multiple business applications | `<<FEATURE FLAG NAME>>` | BUSINESS_2344_DECLARATION_CALCULATION_2022 | A feature flag used in multiple business applications does not include the name of the business application. |
| Only one business application, but multiple microservices | `<<BUSINESS APPLICATION>><<FEATURE FLAG NAME>>` | BUSINESS_PROJECT_1234_DECLARATION_CALCULATION | If a feature flag is intended for multiple microservices within one business application. |
| Only one business application and one microservice | `<<BUSINESS APPLICATION>>_<<MICROSERVICE NAME>>_<<FEATURE FLAG NAME>>` | BUSINESS_MICROSERVICE_A_PROJECT_1234_DECLARATION_CALCULATION | If a feature flag is intended for exactly one microservice. |
