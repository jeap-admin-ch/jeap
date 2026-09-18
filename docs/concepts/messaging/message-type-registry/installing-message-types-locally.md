# Installing the Message Types of a Message Type Registry Locally

## Problem

You want to build *all* message types in a message type registry *locally* and *install* the maven artifacts
created in your *local maven repository*.

## Solution

Configure the **compile-message-types** goal of the **jeap-messaging-avro-maven-plugin** in your message type
registry project locally with the following option:

- **generateAllMessageTypes**: `true`

Configure the **deploy-message-type-artifacts** goal of the **jeap-messaging-avro-maven-plugin** in your message
type registry project locally with the following options:

- **mavenDeployGoal**: `install`
- **mavenGlobalSettingsFile**: `<path-to-your-local-maven-settings-xml-file>`
  - alternatively, don't configure the `mavenGlobalSettingsFile` option and provide a `settings.xml` file in the
    root directory of your message type registry.
- **phase**: `install`

Then run **`mvn install`**. This will generate sources for all message types in the registry, compile those
sources, create jar files from the message type binaries, and install the jars in your local Maven repository.

Example configuration:

```xml
...
            <plugin>
                <groupId>ch.admin.bit.jeap</groupId>
                <artifactId>jeap-messaging-avro-maven-plugin</artifactId>
                <version>8.49.1</version>
                <executions>
                    <execution>
                        <!-- Disable default execution from parent -->
                        <phase>none</phase>
                    </execution>
                    <execution>
                        <id>compile-message-types</id>
                        <goals>
                            <goal>compile-message-types</goal>
                        </goals>
                        <configuration>
                            <generateAllMessageTypes>true</generateAllMessageTypes>
                            <gitUrl>https://github.com/jme-admin-ch/jme-message-type-registry.git</gitUrl>
                            <jeapMessagingVersion>${jeap-messaging.version}</jeapMessagingVersion>
                            <groupIdPrefix>ch.admin.bit.jme.messagetype</groupIdPrefix>
                            <trunkBranchName>master</trunkBranchName>
                            <skip>${jeap.messagetypes.compile.skip}</skip>
                        </configuration>
                    </execution>
                    <execution>
                        <phase>install</phase>
                        <id>deploy-message-type-artifacts</id>
                        <goals>
                            <goal>deploy-message-type-artifacts</goal>
                        </goals>
                        <configuration>
                            <mavenDeployGoal>install</mavenDeployGoal>
                            <mavenGlobalSettingsFile>/home/foobar/.m2/settings.xml</mavenGlobalSettingsFile>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
...
```

## Details

### generateAllMessageTypes

If you configure `generateAllMessageTypes` to `false`, the message type registry build will only process message
types that have been added since the last tagged commit to the trunk branch.

### phase

The default phase of the `deploy-message-type-artifacts` goal is `deploy`. In order to run the goal for a local
install of the message type artifacts, the goal has to be bound to the `install` phase instead.

### mavenDeployGoal

The jeap-messaging-avro-maven-plugin creates and builds separate Maven projects (pom files) for every message type.
To just install the built maven artifacts locally (and not deploy them to a remote Maven repository), the goal of
those maven runs must be set to `install` (instead of its default `deploy`).

### mavenGlobalSettingsFile

The Maven `settings.xml` file provides the information needed to access maven repositories, i.e. authentication,
proxy settings, mirrors, etc.

### Authentication

Starting with version 8.48.0, if you set the environment variable `MESSAGE_TYPE_REPO_GIT_TOKEN` (or the variable
specified by `messageTypeRepoGitTokenEnvVariableName`) to a Git access token, the
`jeap-messaging-registry-maven-plugin` will use this token and JGit to access a remote repository. Otherwise, the
plugin will use your system's Git installation to run git commands locally for accessing remote repositories, and
by doing so will automatically inherit your local Git authentication settings (e.g. SSH keys).

## See also

- [Message Type Registry](index.md)
