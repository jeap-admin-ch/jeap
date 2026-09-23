# Config & Secrets Management

## Overview

For Spring Boot-based microservices, the configuration of the microservices is typically defined in stage-specific configuration. The concrete stage is provided at execution time as a runtime parameter (active profile), and Spring Boot then activates the configuration from the matching configuration files. The development team typically maintains these configuration files for all stages directly in the microservices. In a microservice architecture, this can lead to various problems:

1. **Externalized configuration:** the lifecycle of configuration doesn't always match that of the software code. It should be possible to configure a business application independently of code changes to its microservices, i.e. it shouldn't be necessary to build and deploy a new version of a microservice just to change its configuration for a stage. This isn't possible with Spring Boot configuration files that are part of the microservice code and build.
2. **Cross-microservice configuration:** configuration settings can affect multiple microservices. If such settings are maintained per service in configuration files, it's difficult to ensure a consistent state of the cross-microservice configuration.
3. **Centrally traceable configuration:** for every configuration change, it must be traceable who made the change and for what reason (e.g. a Jira ticket). If the configuration is maintained per service, it's difficult to get an overall picture of the configuration changes in the business application.
4. **Feature flags:** feature flags allow individual features of a business application to be turned on or off independently of a deployment. Among other things, this makes it possible to deploy new features to the production environment early and with low risk. Toggled features can affect the interplay of multiple microservices, so feature flags must be able to be turned on or off centrally for the business application. This is very difficult, if not impossible, to achieve reliably with individual configuration files in the microservices.
5. **Access to sensitive configuration data:** configuration files can contain sensitive data (e.g. service credentials). Access to such data must be restrictable. This is difficult, if not impossible, to achieve with configuration files.
6. **Certificate management:** certificates have their own lifecycle and must be replaceable without deploying a new version of the application. This isn't possible if certificates are managed as part of the application.

Many of these points can be solved with *centralized configuration management*. Usually, the operating platform provides a configuration mechanism for this, which can be managed via GitOps processes and a repository. Example: ConfigMaps on Kubernetes/OpenShift, AWS AppConfig on AWS, ...

## Topics

- [Feature Flags](feature-flags.md)
