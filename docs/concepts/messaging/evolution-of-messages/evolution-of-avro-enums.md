# Evolution of Avro Enums

## Overview and Recommendations

In general, we recommend using `enum` instead of `string` as the type of a message type field that can only hold a limited number of values (according to your business logic), as this makes the message type contract more specific and helps prevent integration errors at runtime.

There are different ways to define an enumeration in Avro and in jEAP messaging, and those different ways have different implications on your options to evolve the enums, i.e. to extend or shrink an enum definition. The following sections discuss those options in detail, while the compatibility table below gives a summary of the options.

Based on the detailed discussions below, we recommend the following:

- If applicable to your business logic, define default values in your enums, as this provides the maximum flexibility with regard to the evolution of the enums.
- For enums that might have to evolve, prefer defining those enums within the namespace of a message type instead of defining them as common types, because for the latter the evolution of enums is trickier and restricted to backward compatibility if you did not take precautions.
- Be aware that backward compatibility is only a viable evolution option if you know all your consumers and those consumers agreed to upgrading to new message type versions within a timeframe that suits your needs.
- Use `string` instead of `enum` only as a last resort.

### Compatibility Matrix

The different ways of defining an enum in Avro and jEAP messaging support different options for the evolution of an enum with regard to the compatibility of the evolution:

| Compatibility | Extending the enum | Shrinking the enum |
| --- | --- | --- |
| Enum type defined in the message type namespace, **with** default value | full | full |
| Enum type defined in the message type namespace, **without** default value | backward | forward |
| Enum type defined in a common namespace, **with** default value | backward (full)* | backward (full)* |
| Enum type defined in a common namespace, **without** default value | backward | (forward)* |

\* Only if an alias to the next version had been added in advance to the enum type version to be evolved (see [Restrictions on Enums as Common Types](#restrictions-on-enums-as-common-types) for details).

## Backward or Forward Evolution of Enums without Default Value

Let's assume we have an enum definition that does not define a default value:

```java
enum JmeDeclarationType {
    TYPE_FOO, TYPE_BAR
}
```

In this case, the compatibility (*backward* or *forward*) of a change to the enum differs depending on the change (*extending* or *shrinking*). This restricts the flexibility in the evolution of the enum.

### Extending the Enum

If we extend this enum with an additional value `TYPE_42`, this change will be *backward compatible only*, which means *all* consumers will have to upgrade to the new version before the producer is allowed to upgrade to the new version. This is only viable if the producer knows all its consumers and those consumers agreed to upgrade to a new version in the time frame needed by the producer.

```java
enum JmeDeclarationType {
    TYPE_FOO, TYPE_BAR, TYPE_42
}
```

### Shrinking the Enum

If we shrink the enum by removing a value (e.g. `TYPE_BAR`), this change will be *forward compatible only*, which means the producer must upgrade before any of its consumers.

```java
enum JmeDeclarationType {
    TYPE_FOO
}
```

## Fully Compatible Evolution of Enums with Default Values

Since version 1.9.0, Avro supports defining a default enum value. Changes to an enum with a default value are fully compatible, i.e. forward compatible and backward compatible at the same time. This provides full flexibility in the evolution of the enum.

An enum with a default value can be defined like this:

```java
enum JmeDeclarationType {
    UNKNOWN, TYPE_FOO, TYPE_BAR
} = UNKNOWN;
```

In this case, a consumer will deserialize any enum value it does not understand to the default value specified in the enum (here: `UNKNOWN`).

> **Note:** The (business) logic behind a default value must be clearly defined, especially for a default value of the kind "UNKNOWN".

> **Note:** Defining a default value in the enum is not the same as defining a default value on a field with type enum. If you want to add a new enum field to a message type in a fully compatible way, you still must provide a default value for the field regardless of the default value defined in the enum. Often, the default on the field and the default in the enum will be the same value, but need not be.

## Restrictions on Enums as Common Types

Certain [restrictions](../message-type-registry/index.md#common-data) apply to Avro types defined in the `_common` folder of a [jEAP message type registry](../message-type-registry/index.md). One of them is that such types can't be changed, and therefore evolution of such a type can only be done by defining a new version of the type in a *different* Avro namespace. This poses a challenge for the evolution of an enum defined as a common type (one defined in the `_common` folder).

Because the enum has to change its Avro namespace as it evolves, each version of the enum will have its own namespace and will be seen as a different type by the Kafka Avro deserializer. If a producer publishes a message version using version 1 of an enum and the consumer expects a message version using version 2 of the enum, deserialization of the message will fail, because the Avro deserializer expected version 2 of the enum, not version 1. Deserialization will fail regardless of the compatibility of the enum versions' value sets, i.e. even if the enum versions were fully compatible with regard to their value definitions.

This would make it impossible to use such enums in a message type if the enum must be able to evolve while keeping the message type versions using those enum versions compatible to some extent. However, Avro provides a workaround for this problem in the form of *aliases*. With an alias, we can define a new version of an enum to be equivalent to the old version of the enum.

Let's assume we defined the following enum as a common type (i.e. in the `_common` folder), as version 1, in the namespace `ch.admin.bit.jme.common.v1`:

```java
@namespace("ch.admin.bit.jme.common.v1")
protocol JmeDeclarationTypeProtocol {
    enum JmeDeclarationType {
        UNKNOWN, TYPE_FOO, TYPE_BAR
    } = UNKNOWN;
}
```

If we want to define a version 2 of this common type enum, we must do this in another namespace, e.g. `ch.admin.bit.jme.common.v2`. To be able to deserialize the previous version of the enum into this version, we also need to tell Avro that this version is equivalent to the previous version. We can do this by adding the annotation `@aliases(["ch.admin.bit.jme.common.v1.JmeDeclarationType"])` to the enum declaration.

```java
@namespace("ch.admin.bit.jme.common.v2")
protocol JmeDeclarationTypeProtocol {
    @aliases(["ch.admin.bit.jme.common.v1.JmeDeclarationType"])
    enum JmeDeclarationType {
        UNKNOWN, TYPE_FOO, TYPE_BAR, TYPE_42
    } = UNKNOWN;
}
```

Now the Kafka Avro deserializer will be able to deserialize a message with the enum in version 1 into a message with the enum in version 2. Deserialization will not succeed the other way round, as the `@aliases` declaration only seems to have an effect if it is in the target schema, i.e. in the schema of the message consumer. Therefore, the new enum version declared above only supports backward compatibility.

For forward compatibility, we would have to add `@aliases(["ch.admin.bit.jme.common.v2.JmeDeclarationType"])` to the type definition of the first enum version. But as common types (the ones in the `_common` folder) cannot be changed after they have been published, we would effectively be stuck with backward compatibility only if we started out with version 1 from above.

If an enum defined as a common type must be able to evolve in a forward compatible way, it must be defined with an `@aliases` annotation pointing to a hypothetical future version of the enum. If this is forgotten, evolution of the enum is restricted to backward compatibility.

## See also

- [Evolution of Messages](index.md) — forward/backward compatibility and the EMC strategies this page's recommendations apply to.
- [jEAP Message Type Registry](../message-type-registry/index.md) — where common types, including enums, are declared.
