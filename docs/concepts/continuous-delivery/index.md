# Continuous Delivery

## Overview

> **What is Continuous Delivery?**
> Continuous Delivery is the ability to get changes of all types - including new features, configuration changes, bug fixes and experiments - into production, or into the hands of users, safely and quickly in a sustainable way.
>
> The goal is to make deployments - whether for a large-scale distributed system, a complex production environment, an embedded system, or an app - predictable, routine affairs that can be performed on demand.
>
> We achieve all this by ensuring our code is always in a deployable state, even in the face of teams of thousands of developers making changes on a daily basis. We thus completely eliminate the integration, testing and hardening phases that traditionally followed "dev complete", as well as code freezes.
>
> -- Jez Humble, [https://continuousdelivery.com/](https://continuousdelivery.com/)

This section documents how Continuous Delivery and deployment are implemented for jEAP microservices. It primarily documents the techniques and methods used for this, how [zero-downtime deployments](zero-downtime-deployments.md) can be implemented, and how changes can be released to production independently of other components by splitting them into individual steps - [Expand - Migrate - Contract](expand-migrate-contract.md).

Related documentation on this topic:

- [Testing](../testing/index.md)
- [Feature Flags](../config-secrets-management/feature-flags.md)

## Topics

- [Expand - Migrate - Contract](expand-migrate-contract.md)
- [Zero-Downtime Deployments](zero-downtime-deployments.md)
