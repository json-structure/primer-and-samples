# JSON Structure Primer

> Author: Clemens Vasters, Microsoft, February 2025, clemensv@microsoft.com

This primer introduces _JSON Structure_, a modern, strictly typed data
definition language that resembles JSON Schema, but has very different basic
design principles.

JSON Structure focuses on defining data types with clear, deterministic
constraints while supporting extensions for precise representations of numbers,
dates, and more. 

Common programming language concepts like reuse and composition are supported
directly in the schema language, but while avoiding introduction of the entire
complexity of object-oriented programming.

Conditional validation of JSON data against schemas with composition constructs
like `anyOf` or `allOf` is availble in JSON Structure quite similar to JSON
Schema, has been split out into optional extensions, allowing simple data
definitions to remain lightweight and easy to understand.

## 1. Introduction

There are rapidly growing needs for a standardized (IETF RFC) schema language
that can describe data types and structures and whose definitions map cleanly to
programming language types and database constructs as well as into the popular
JSON data encoding. The type model needs to reflect the needs of modern
applications and it must allow rich annotations with semantic information that
can be evaluated and understood by developers and by large language models
(LLMs).

JSON Schema has been in development since ca. 2009 and has gone through several
iterations. The industry has largely settled on "Draft 7" of JSON Schema, with
subsequent releases seeing comparatively weak adoption. There's substantial
frustration that many developers have with JSON Schema because they try to use
it for scenarios that it was not designed for. JSON Schema is a powerful
document validation tool, but it is not a data definition language.

_JSON Structure_ aims to address these different use cases and priorities while
maintaining familiarity with JSON Schema's syntax. While JSON Schema focuses on
and excels at document validation, JSON Structure focuses on being a strong data
definition language.

There are two major use-case scenarios for schema languages in general:

1. Validating JSON data against a schema to ensure conformity to a specific
   structure and constraints.
2. Declaring data types and structures in a machine-readable format that can be
   used to generate code, documentation, or other artifacts across platforms and
   languages.

JSON Schema provides powerful facilities for the first use-case. JSON Structure
prioritizes the second use-case while still supporting the validation scenarios
similar to JSON Schema through extensions.

With JSON Structure, we've designed a type system that addresses common
challenges:

- Clear mapping to programming language types
- Support for more precise numeric types and date/time representations
- Modular approach to extensions
- Simplified cross-references between schema documents
- Straightforward reuse patterns for types

This approach better supports code generation, database mappings, and
integration with modern programming languages, while keeping the validation
capabilities as optional extensions for those who need them.

## 2. Key Concepts

JSON Structure is designed to look and feel very much like the JSON Schema
drafts you already know, but some rules have been tightened up to make it easier
to understand and use. Therefore, existing JSON Schema documents may need to be
updated to conform to the new rules.

### 2.1. Differences to JSON Schema Drafts

- **Strict Typing:** Every schema must explicitly specify its data type. For
  compound types (objects, arrays, sets), additional required metadata like a
  name and other required property definitions help enforce structured data.
- **Identifiers:** Names of types and properties are restricted to the regular
  expression `[A-Za-z_][A-Za-z0-9_]*` to make them easier to map to code and
  database constructs. Map keys may additionally contain `:`, `-`, and `.` and
  may start with a digit.
- **Extended Types:** In addition to JSON primitives such as string, number,
  boolean, and null, JSON Structure Core supports many extended primitive types
  (e.g., `int32`, `int64`, `decimal`, `date`, `uuid`) for high precision or
  format-specific data.
- **Compound Types:** The compound types have been extended to include `set`,
  `map`, and `tuple`
    - **Object:** Define structured data with a required `name` and a set of
      `properties`.
    - **Array:** List of items where the `items` attribute references a declared
      type without inline compound definitions.
    - **Set:** An unordered collection of unique elements.
    - **Map:** A collection of key-value pairs where keys are strings and values
      are of a declared type.
    - **Tuple:** A fixed-length array of elements where each element is of a
      declared type. It's a more compact alternative to objects where the
      property names are replaced by the position in the tuple. Arrays or maps
      of tuples are especially useful for time-series data.
    - **Choice:** A discriminated union of types, where one of the types is
      selected based on a discriminator property. The `choice` keyword is used
      to define the union and the `selector` property is used to specify the
      discriminator property.
- **Namespaces:** Namespaces are a formal part of the schema language, allowing
  for more modular and deterministic schema definitions. Namespaces are used to
  scope type definitions.
- **Cross-Referencing:** The `$ref` keyword has been limited to referencing
  named types that exist within the same document. It can no longer reference
  and insert arbitrary JSON nodes and it can no longer reference external
  documents. To reuse types from other documents, you now need to use the
  `$import` keyword from the optional [import][JSTRUCT-IMPORT] spec to import
  the types you need. Once imported, you can reference types with `$ref`.

### 2.2. Extensibility Model

JSON Structure is designed to be extensible. Any schema can be extended with
custom keywords given that those do not conflict with the core schema language
or companion specifications that are "activated" for the schema document. It's
recommended for custom keywords to have a compnay- or project-specific prefix to
avoid such collisions. It's not required to declare a formal meta-schema to use
custom keywords, but it's recommended to do so.

JSON Structure is designed to be modular. The core schema language is defined in
the [JSON Structure Core][JSTRUCT-CORE] document. Companion specifications
provide additional features and capabilities that can be used to extend the core
schema language. 

The `abstract` and `$extends` keywords enable controlled type extension,
supporting basic object-oriented-programming-style inheritance while not
permitting subtype polymorphism where a sub-type value can be assigned a
base-typed property. This approach avoids validation complexities and mapping
issues between JSON schemas, programming types, and databases.

There are two types of formal extensions: _extensible types_ and _add-in types_.

#### 2.2.1. Extensible Types

It's fairly common that different types share a common basic set of properties.
In JSON Schema itself, the `description` property is a good example of a
property that is shared across all schema and non-schema objects.

An _extensible type_ is declared as `abstract` and provides a set of common
definitions to be shared by extensions. For example, a base type _AddressBase_
MAY be extended by _StreetAddress_ and _PostOfficeBoxAddress_ via `$extends`.
Because it's abstract, _AddressBase_ cannot be used directly anywhere as a type,
however. _Address_ extends _AddressBase_ without adding any additional
properties.

Example:

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "definitions" : {
      "AddressBase": {
        "abstract": true,
        "type": "object",
        "properties": {
            "city": { "type": "string" },
            "state": { "type": "string" },
            "zip": { "type": "string" }
        }
      },
      "StreetAddress": {
        "type": "object",
        "$extends": "#/definitions/AddressBase",
        "properties": {
            "street": { "type": "string" }
        }
      },
      "PostOfficeBoxAddress": {
        "type": "object",
        "$extends": "#/definitions/AddressBase",
        "properties": {
            "poBox": { "type": "string" }
        }
      },
      "Address": {
        "type": "object",
        "$extends": "#/definitions/AddressBase"
      }
    }
}
```

#### 2.2.2. Add-in Types

Add-in types allow modifying any existing type in a schema with additional
properties or constraints. Add-ins are offered to the instance document author
through the `$offers` keywords in the schema document. The instance document
author can then enable the add-in by referencing the add-in name in the `$uses`
keyword. When the instance document does so, the add-in properties are injected
into the designated schema types before the schema is evaluated. Enabled add-ins
are treated as if they were part of the schema from the beginning.

Add-ins can also be enabled in meta-schemas such that they are always applied to
schemas that are based on the meta-schema.

A _add-in type_ is declared as `abstract` and `$extends` a specific type that
does not need to be abstract. For example, a add-in type _DeliveryInstructions_
might be applied to any _StreetAddress_ types in a document:

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://schemas.vasters.com/Addresses",
    "$root": "#/definitions/StreetAddress",
    "$offers": {
        "DeliveryInstructions": "#/definitions/DeliveryInstructions"
    },
    "definitions" : {
      "StreetAddress": {
        "type": "object",
        "properties": {
            "street": { "type": "string" },
            "city": { "type": "string" },
            "state": { "type": "string" },
            "zip": { "type": "string" }
        }
      },
      "DeliveryInstructions": {
        "abstract": true,
        "type": "object",
        "$extends": "#/definitions/StreetAddress",
        "properties": {
            "instructions": { "type": "string" }
        }
      }
    }
}
```

Add-ins are applied to a schema by referencing the add-in name in the `$uses`
keyword that is available only in instance documents. The `$uses` keyword is a
set of add-in names that are applied to the schema for the document.

```json
{
  "$schema": "https://schemas.vasters.com/Addresses",
  "$uses": ["DeliveryInstructions"],
  "street": "123 Main St",
  "city": "Anytown",
  "state": "QA",
  "zip": "00001",
  "instructions": "Leave at the back door"
}
```

### 2.3. Reusing Types across different Schema Documents

The prior versions of JSON Schema in effect allowed for `$ref` to reference
arbitrary JSON nodes from the same or external document, which made references
very difficult to understand and process, especially when the references were
deep links into external schema documents and/or schema documents were
cross-referenced using relative URIs to avoid committing to an absolute schema
location.

JSON Structure has a more controlled approach to limit that complexity. 

  1. The `$ref` keyword can only reference named types that exist within the
     same document. It can no longer reference and insert arbitrary JSON nodes
     and it can no longer reference external documents. 
  2. To reuse types from other documents, you now need to use the `$import`
     keyword from the optional [import][JSTRUCT-IMPORT] spec to import the types
     you need into the scope of the schema document. Once imported, you use the
     imported types as if they were declared in the document. To avoid
     conflicts, you can import external types into a namespace.
  3. Since types are imported and then referenced as if they were declared in
     the document, it's also possible and permitted to "shadow" imported types
     with local definitions by explicitly declaring a type with the same name
     and namespace as as the imported type.

### 2.4. Core and Companion Specifications

The following documents are part of this JSON Structure proposal:

- [JSON Structure Core][JSTRUCT-CORE]: Defines the core schema language for
  declaring data types and structures.
- [JSON Structure Alternate Names and Descriptions][JSTRUCT-ALTNAMES]: Provides
  a mechanism for declaring alternate names and symbols for types and
  properties, including for the purposes of internationalization.
- [JSON Structure Symbols, Scientific Units, and Currencies][JSTRUCT-UNITS]:
  Defines keywords for specifying symbols, scientific units, and currency codes
  on types and properties.
- [JSON Structure Conditional Composition][JSTRUCT-COMPOSITION]: Defines a set
  of conditional composition rules for evaluating schemas.
- [JSON Structure Validation][JSTRUCT-VALIDATION]: Specifies extensions to the
  core schema language for declaring validation rules.
- [JSON Structure Import][JSTRUCT-IMPORT]: Defines a mechanism for importing
  external schemas and definitions into a schema document.

### 2.5. Meta-Schemas

Meta-schemas are JSON Structure documents that define the structure and
constraints of schema documents themselves. Meta-schemas do not have special
constructs beyond what is available in the core schema language.

A meta-schema is referenced in a schema document using the `$schema` keyword.
The meta-schema defines the constraints that the schema document must adhere to.

The value of the `$schema` keyword is a URI that corresponds to the `$id`
declared in the meta-schema document. The URI should be a resolvable URL that
points to the meta-schema document, but for well-known meta-schemas, a schema
processor will typically not actually fetch the meta-schema document. Instead,
the schema processor will use the URI to identify the meta-schema and validate
the schema document against its copy of the meta-schema.

A meta-schema can build on another meta-schema by `$import`ing all of its
definitions and then adding additional definitions or constraints or by
shadowing definitions from the imported meta-schema.

The ["core" meta-schema](./json-schema-core-metaschema-core.json) formally
defines the elements described in the [JSON Structure Core][JSTRUCT-CORE]
document. The "$id" of the core meta-schema is
`https://json-structure.org/meta/core/v0`.

The ["extended" meta-schema](./json-schema-metaschema-extended.json) extends the
core meta-schema with all additional features and capabilities provided by the
companion specifications and offers those features to schema authors. The "$id"
of the extended meta-schema is
`https://json-structure.org/meta/extended/v0`.

The ["validation" meta-schema](./json-schema-metaschema-validation.json) enables
all add-ins defined in the extended meta-schema.

## 3. Using Structure Core 

This section introduces JSON Structure by example.

### 3.1. Example: Declaring a simple object type

Here is an example of a simple object type definition:

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "type": "object",
    "name": "Person",
    "properties": {
        "firstName": { "type": "string" },
        "lastName": { "type": "string" },
        "dateOfBirth": { "type": "date" }
    },
    "required": ["firstName", "lastName"]
}
```

If you are familiar with JSON Schema, you will instantly recognize the structure
of this schema. The `type` attribute specifies that this is an object type. The
`properties` attribute lists the properties of the object, and the `required`
attribute lists the properties that are required.

There are a few differences from prior version of JSON Schema. The `name`
attribute is new and is required for the root type. The `type` attribute is also
required and no longer implied to be `object` if not present. You may also
notice that the "dateOfBirth" property uses the new `date` type, which is an
extended native type.

### 3.2. Example: Declaring Primitive and Extended Types

Below is an example schema that defines a simple profile with a few more
extended types:

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "type": "object",
    "name": "UserProfile",
    "properties": {
        "username": { "type": "string" },
        "dateOfBirth": { "type": "date" },
        "lastSeen": { "type": "datetime" },
        "score": { "type": "int64" },
        "balance": { "type": "decimal", "precision": 20, "scale": 2 },
        "isActive": { "type": "boolean" }
    },
    "required": ["username", "birthdate"]
}
```

The `int64` type is an extended type that represents a 64-bit signed integer.
The `decimal` type is another extended type that represents a decimal number
with a specified precision and scale. The `datetime` type is an extended type
that represents a date and time value.

## 4. Example: Declaring inline compound types

This is an example of a type that is declared inline. This is useful for
compound types that are not reused elsewhere in the schema. The `address`
property of the `UserProfile` type references the inline `Address` type. This
type cannot be referenced from other types in the schema.

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "type": "object",
    "name": "UserProfile",
    "properties": {
        "username": { "type": "string" },
        "dateOfBirth": { "type": "date" },
        "lastSeen": { "type": "datetime" },
        "score": { "type": "int64" },
        "balance": { "type": "decimal", "precision": 20, "scale": 2 },
        "isActive": { "type": "boolean" },
        "address": {
            "type": "object",
            "name": "Address",
            "properties": {
                "street": { "type": "string" },
                "city": { "type": "string" },
                "state": { "type": "string" },
                "zip": { "type": "string" }
            },
            "required": ["street", "city", "state", "zip"]
        }
    },
    "required": ["username", "birthdate"]
}
```

### 4.1. Example: Declaring reusable types in `definitions`

To define reusable types, you can use the `definitions` keyword to define types
that can be referenced by other types in the same document. Here is an example:

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "type": "object",
    "name": "UserProfile",
    "properties": {
        "username": { "type": "string" },
        "dateOfBirth": { "type": "date" },
        "lastSeen": { "type": "datetime" },
        "score": { "type": "int64" },
        "balance": { "type": "decimal", "precision": 20, "scale": 2 },
        "isActive": { "type": "boolean" },
        "address": { "type" : { "$ref": "#/definitions/Address" } }
    },
    "required": ["username", "birthdate"],
    "definitions": {
        "Address": {
            "type": "object",
            "properties": {
                "street": { "type": "string" },
                "city": { "type": "string" },
                "state": { "type": "string" },
                "zip": { "type": "string" }
            },
            "required": ["street", "city", "state", "zip"]
        }
    }
}
```

In this example, the `Address` type is declared in the `definitions` section and
can be referenced by other types in the same document using the `$ref` keyword.
Mind that the `$ref` keyword can now only reference types declared in the
`definitions` section of the same document. The keyword can only be used where a
type is expected.

### 4.2. Example: Structuring types with namespaces

Namespaces are used to scope type definitions. Here is an example of how to use
namespaces to structure your types, with two differing `Address` types:

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "type": "object",
    "name": "UserProfile",
    "properties": {
        "username": { "type": "string" },
        "dateOfBirth": { "type": "date" },
        "networkAddress": { "type" : { "$ref": "#/definitions/Network/Address" } },
        "physicalAddress": { "type": { "$ref": "#/definitions/Physical/Address" } }
    },
    "required": ["username", "birthdate"],
    "definitions": {
        "Network": {
            "Address": {
                "type": "object",
                "properties": {
                    "ipv4": { "type": "string" },
                    "ipv6": { "type": "string" }
                }
            }
        },
        "Physical": {
            "Address": {
                "type": "object",
                "properties": {
                    "street": { "type": "string" },
                    "city": { "type": "string" },
                    "state": { "type": "string" },
                    "zip": { "type": "string" }
                },
                "required": ["street", "city", "state", "zip"]
            }
        }
    }
}
```

### 4.3. Example: Using an Array Type

This example shows how to declare an array of strings, which is not much
different from defining an object:

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "type": "array",
    "items": { "type": "string" }
}
```

You can also declare an array of a locally declared compound type, but you can
not reference the type from elsewhere in the schema:

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "firstName": { "type": "string" },
            "lastName": { "type": "string" },
            "dateOfBirth": { "type": "date" }
        },
        "required": ["firstName", "lastName"]
    }
}
```

To declare an array of a reusable type, you can use the `$ref` keyword:

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "type": "array",
    "items": { "type" : { "$ref": "#/definitions/Person" } },
    "definitions": {
        "Person": {
            "type": "object",
            "name": "Person",
            "properties": {
                "firstName": { "type": "string" },
                "lastName": { "type": "string" },
                "dateOfBirth": { "type": "date" }
            },
            "required": ["firstName", "lastName"]
        }
    }
}
```

### 4.4. Example: Declaring Maps

This example shows how to declare a map of strings to `Color` objects:

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "type": "map",
    "values": { "type": { "$ref": "#/definitions/Color" } },
    "definitions": {
        "Color": {
            "type": "object",
            "name": "Color",
            "properties": {
                "red": { "type": "int32" },
                "green": { "type": "int32" },
                "blue": { "type": "int32" }
            },
            "required": ["red", "green", "blue"]
        }
    }
}
``` 

Instance data for this schema might look like this:

```json
{
    "rose": { "red": 255, "green": 0, "blue": 0 },
    "sky": { "red": 0, "green": 191, "blue": 255 },
    "grass": { "red": 0, "green": 128, "blue": 0 },
    "sun": { "red": 255, "green": 215, "blue": 0 },
    "cloud": { "red": 255, "green": 255, "blue": 255 },
    "moon": { "red": 192, "green": 192, "blue": 192 }
}
```

### 4.5. Example: Declaring Sets

This example shows how to declare a set of strings:

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "type": "set",
    "items": { "type": "string" }
}
```

Sets differ from arrays in that they are unordered and contain only unique
elements. The schema above would match the following instance data:

```json
["apple", "banana", "cherry"]
```

### 4.6. Example: Declaring Tuples

Tuples are fixed-length arrays with named elements, declared via the `tuple` keyword.

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "type": "tuple",
    "name": "PersonTuple",
    "properties": {
        "firstName": { "type": "string" },
        "age":       { "type": "int32" }
    },
    "tuple": ["firstName", "age"]
}
```

An instance of this tuple type:

```json
["Alice", 30]
```

### 4.7. Example: Declaring Choice Types

Choice types define discriminated unions via the `choice` keyword. Two forms are supported:

#### Tagged Unions

Tagged unions represent the selected type as a single-property object:

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "type": "choice",
    "name": "StringOrNumber",
    "choices": {
        "string": { "type": "string" },
        "int32":  { "type": "int32" }
    }
}
```

Valid instances:

```json
{ "string": "Hello" }
{ "int32":  42 }
```

#### Inline Unions

Inline unions extend a common abstract base type and use a selector property:

```json
{
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "type": "choice",
    "name": "AddressChoice",
    "$extends": "#/definitions/Address",
    "selector": "addressType",
    "choices": {
        "StreetAddress":     { "$ref": "#/definitions/StreetAddress" },
        "PostOfficeBoxAddress": { "$ref": "#/definitions/PostOfficeBoxAddress" }
    },
    "definitions": {
        "Address": {
            "abstract": true,
            "type": "object",
            "properties": {
                "city": { "type": "string" },
                "state":{ "type": "string" },
                "zip":  { "type": "string" }
            }
        },
        "StreetAddress": {
            "type": "object",
            "$extends": "#/definitions/Address",
            "properties": { "street": { "type": "string" } }
        },
        "PostOfficeBoxAddress": {
            "type": "object",
            "$extends": "#/definitions/Address",
            "properties": { "poBox": { "type": "string" } }
        }
    }
}
```

Instance of this inline union:

```json
{
    "addressType": "StreetAddress",
    "street":      "123 Main St",
    "city":        "AnyCity",
    "state":       "AS",
    "zip":         "11111"
}
```

## 5. Using Companion Specifications

The JSON Structure Core specification is designed to be extensible through
companion specifications that provide additional features and capabilities. 

The extended schema that includes all companion specifications is identified by
the `https://json-structure.org/meta/extended/v0` URI. Each companion
specification is identified by a unique identifier that can be used in the
`$uses` attribute to activate the companion specification for the schema
document.

The feature identifiers for the companion specifications are:
- `JSONStructureAlternateNames`: Alternate names and descriptions for properties
  and types.
- `JSONStructureUnits`: Symbols, scientific units, and currencies for numeric
  properties.
- `JSONStructureImports`: Importing types from other schema documents.
- `JSONStructureValidation`: Validation rules for JSON data.
- `JSONStructureConditionalComposition`: Conditional composition and validation
  rules.

### 5.1. Example: Using the `altnames` Keyword

The [JSON Structure Alternate Names and Descriptions][JSTRUCT-ALTNAMES]
companion specification introduces the `altnames` keyword to provide alternate
names for properties and types. Alternate names provide additional mappings that
schema processors may use for encoding, decoding, or user interface display.

Here is an example of how to use the `altnames` keyword:

```json
{
    "$schema": "https://json-structure.org/meta/extended/v0/#",
    "$uses": ["JSONStructureAlternateNames"],
    "Person": {
        "type": "object",
        "altnames": {
            "json": "person_data",
            "lang:en": "Person",
            "lang:de": "Person"
        },
        "properties": {
            "firstName": {
                "type": "string",
                "altnames": {
                    "json": "first_name",
                    "lang:en": "First Name",
                    "lang:de": "Vorname"
                }
            },
            "lastName": {
                "type": "string",
                "altnames": {
                    "json": "last_name",
                    "lang:en": "Last Name",
                    "lang:de": "Nachname"
                }
            }
        },
        "required": ["firstName", "lastName"]
    }
}
```

Each named type or property in the schema has been given an `altnames` attribute
that provides alternate names for the type or property. 

The `json` key is used to specify alternate names for JSON encoding, meaning
that if the schema is used to encode or decode JSON data, the alternate key MUST
be used instead of the name in the schema.

Keys beginning with `lang:` are reserved for providing localized alternate names
that can be used for user interface display. Additional keys can be used for
custom purposes, subject to no conflicts with reserved keys or prefixes.

### 5.2. Example: Using the `altenums` Keyword

The [JSON Structure Alternate Enumerations][JSTRUCT-ALTNAMES] companion
specification introduces the `altenums` keyword to provide alternative
representations for enumeration values defined by a type using the `enum`
keyword. Alternate symbols allow schema authors to map internal enum values to
external codes or localized display symbols.

Here is an example of how to use the `altenums` keyword:

```json
{
    "$schema": "https://json-structure.org/meta/extended/v0/#",
    "$uses": ["JSONStructureAlternateNames"],
    "type": "object",
    "name": "Color",
    "properties": {
        "name": { "type": "string" },
        "value": { 
            "type": "string", 
            "enum": ["red", "green", "blue"],
            "altenums": {
                "lang:en": {
                    "red": "Red",
                    "green": "Green",
                    "blue": "Blue"
                },
                "lang:de": {
                    "red": "Rot",
                    "green": "Grün",
                    "blue": "Blau"
                }
            }
        }
    }
}
```

In this example, the `value` property has an `enum` attribute that defines the
possible values for the property. The `altenums` attribute provides alternative
names for each enumeration value. The `lang:en` key provides English names for
the enumeration values, and the `lang:de` key provides German names.

### 5.3. Example: Using the `unit` Keyword

The [JSON Structure Symbols, Scientific Units, and Currencies][JSTRUCT-UNITS]
companion specification introduces the `unit` keyword to provide a standard way
to specify the unit of measurement for numeric properties. The `unit` keyword
allows schema authors to specify the unit of measurement for numeric properties
and provides a standard way to encode and decode numeric values with units.

Here is an example of how to use the `unit` keyword:

```json
{
    "$schema": "https://json-structure.org/meta/extended/v0/#",
    "$uses": ["JSONStructureUnits"],
    "type": "object",
    "name": "Pressure",
    "properties": {
        "value": { "type": "number", "unit": "Pa" }
    }
}
```

In this example, the `value` property has a `unit` attribute that specifies the
unit of measurement for the property. The unit of measurement is specified as a
string value. In this case, the unit of measurement is "Pa" for Pascals.

### 5.4. Example: Using the `currency` Keyword

The [JSON Structure Symbols, Scientific Units, and Currencies][JSTRUCT-UNITS]
companion specification also introduces the `currency` keyword to provide a
standard way to specify the currency for monetary properties. The `currency`
keyword allows schema authors to specify the currency for monetary properties
and provides a standard way to encode and decode monetary values with
currencies.

Here is an example of how to use the `currency` keyword:

```json
{
    "$schema": "https://json-structure.org/meta/extended/v0/#",
    "$uses": ["JSONStructureUnits"],
    "type": "object",
    "name": "Price",
    "properties": {
        "value": { "type": "decimal", "precision": 20, "scale": 2, "currency": "USD" }
    }
}
```

In this example, the `value` property has a `currency` attribute that specifies
the currency for the property. The currency is specified as a string value. In
this case, the currency is "USD" for US Dollars.

## 6. Using Validation

The companion specifications for conditional composition and validation provide
additional constructs for defining conditional validation rules and composing
that resemble those found in prior versions of JSON Schema. However, those have
been split out into optional extensions to keep the core schema language simple.

### 6.1. Example: Using Conditional Composition

The [JSON Structure Conditionals][JSTRUCT-COMPOSITION] companion specification
introduces conditional composition constructs for combining multiple schema
definitions. In particular, this specification defines the semantics, syntax,
and constraints for the keywords `allOf`, `anyOf`, `oneOf`, and `not`, as well
as the `if`/`then`/`else` conditional construct.

The specification has several examples that show how to use the conditional
composition keywords.

### 6.2. Example: Using Validation Rules

The [JSON Structure Validation][JSTRUCT-VALIDATION] companion specification
introduces additional validation rules for JSON data.

---

[JSTRUCT-ALTNAMES]: https://github.com/json-structure/altername-names
[JSTRUCT-COMPOSITION]: https://github.com/json-structure/conditional-composition
[JSTRUCT-IMPORT]: https://github.com/json-structure/import
[JSTRUCT-UNITS]:https://github.com/json-structure/units
[JSTRUCT-VALIDATION]: https://github.com/json-structure/validation
[JSTRUCT-CORE]: https://github.com/json-structure/core

