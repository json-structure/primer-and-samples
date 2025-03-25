# JSON Structure Primer

> Author: Clemens Vasters, Microsoft, February 2025, clemensv@microsoft.com

This primer introduces _JSON Structure_, a modern,
strictly typed schema language that builds on familiar concepts from
prior JSON Schema drafts, but has been entirely refactored.

JSON Structure focuses on defining data types with clear, deterministic
constraints while supporting extensions for precise representations of numbers,
dates, and more. 

Conditional validation of JSON data against schemas with composition constructs
like `anyOf` or `allOf` has been split out into optional extensions, allowing
simple data definitions to remain lightweight and easy to understand.

Common programming language concepts like reuse and composition are supported
directly in the schema language without dragging in the entire complexity of
object-oriented programming.

## Table of Contents

- [JSON Structure Primer](#json-structure-primer)
  - [Table of Contents](#table-of-contents)
  - [1. Wait. What? Why?](#1-wait-what-why)
  - [2. Key Concepts](#2-key-concepts)
    - [2.1. Differences to JSON Schema Drafts](#21-differences-to-json-schema-drafts)
    - [2.2. Extensibility Model](#22-extensibility-model)
      - [2.2.1. Extensible Types](#221-extensible-types)
      - [2.2.2. Add-in Types](#222-add-in-types)
    - [2.3. Reusing Types across different Schema Documents](#23-reusing-types-across-different-schema-documents)
    - [2.4. Core and Companion Specifications](#24-core-and-companion-specifications)
    - [2.5. Meta-Schemas](#25-meta-schemas)
  - [3. Using Structure Core](#3-using-structure-core)
    - [3.1. Example: Declaring a simple object type](#31-example-declaring-a-simple-object-type)
    - [3.2. Example: Declaring Primitive and Extended Types](#32-example-declaring-primitive-and-extended-types)
  - [4. Example: Declaring inline compound types](#4-example-declaring-inline-compound-types)
    - [4.1. Example: Declaring reusable types in `$defs`](#41-example-declaring-reusable-types-in-defs)
    - [4.2. Example: Structuring types with namespaces](#42-example-structuring-types-with-namespaces)
    - [4.3. Example: Using an Array Type](#43-example-using-an-array-type)
    - [4.4. Example: Declaring Maps](#44-example-declaring-maps)
    - [4.5. Example: Declaring Sets](#45-example-declaring-sets)
  - [5. Using Companion Specifications](#5-using-companion-specifications)
    - [5.1. Example: Using the `altnames` Keyword](#51-example-using-the-altnames-keyword)
    - [5.2. Example: Using the `altenums` Keyword](#52-example-using-the-altenums-keyword)
    - [5.3. Example: Using the `unit` Keyword](#53-example-using-the-unit-keyword)
    - [5.4. Example: Using the `currency` Keyword](#54-example-using-the-currency-keyword)
  - [6. Using Validation](#6-using-validation)
    - [6.1. Example: Using Conditional Composition](#61-example-using-conditional-composition)
    - [6.2. Example: Using Validation Rules](#62-example-using-validation-rules)

## 1. Wait. What? Why?

JSON Schema has been in development since ca. 2009 and has gone through several
iterations. Yet, there is still no IETF RFC anyone could really lean on as a
standard. Practitioners are largely using "Draft 7" of JSON Schema and the
subsequent releases have seen comparatively little adoption. 

The quality of the specs in terms of clarity and precision has been a major
issue and the JSON Schema project has stood up a website that explains the spec
in more detail than the spec itself. 

Structured metadata is becoming rapidly more important in the world of APIs and
LLMs. Large language models can operate better in structured data if they are
fed with rich context information and schema documents can provide such context.

JSON Schema should play a big role in this context, but its complexity and
ambiguity and the lack of a finalized standard are major obstacles. Efforts like
OpenAPI lean on subsets of JSON Schema and had to invent their own extensions to
cover gaps. There are no two implementations of JSON Schema code generators that
agree on the output mapping of conditional JSON Schema structures to code,
including those for OpenAPI. 

Worse yet, all of these tools (need to) give up on complex JSON Schema
constructs at some point and that point is different for each implementation.
It's close to impossible to write JSON Schemas that can be used reliably for
code generation in a cross-platform and cross-language way unless you scope out
a substantial portion of the JSON Schema language.

There are two major use-case scenarios for JSON Schema and schema languages in
general:

1. Users want to validate JSON data against a schema to ensure that the data
   conforms to a specific structure and set of constraints.
2. Users want to declare data types and structures in a machine-readable format
   that can be used to generate code, documentation, or other artifacts in a
   cross-platform, cross-language way.

JSON Schema has enormously powerful facilities for the first use-case right in
its core. All that power comes at the expense of the second use-case.

The existing drafts of JSON Schema define a pattern-matching language for schema
processors that is applied to JSON data as it is being validated. It is not a
data definition language. It is a validation language that embeds elements that
only look like data definition capabilities. An `object` declaration in JSON
Schema is a matching expression for a JSON object that contains the properties
defined in the schema; it does not define an object type.

Conditional composition constructs like `allOf`, `anyOf`, `oneOf`, `not`, and
`if`/`then`/`else` are defined in the core schema language. As powerful as they
are, conditional composition of data types is generally not a thing in databases
or programming languages, which means that any use of these constructs makes
mapping from and to code and databases hard and in many cases impossible while
preserving the schema semantics.

JSON Schema allows for `$ref` to reference arbitrary JSON nodes (any of which
are schemas) from the same or external document, which adds to the complexity. A
single JSON Schema might have dozens of external links to content, strewn across
the document, making it very difficult to understand as well as hard and
potentially unsafe to process. 

There are also confusing conflicts and overlaps. For instance, JSON Schema has a
concept of a type union that can only be used for primitive types. Users
frequently side-step that limitation through a `oneOf` construct that behaves
equivalent to a type union for validation and thus there are factually two type
union constructs.

Enumerations are first-class constructs in many programming languages and
generally map symbols to values of a single type. In JSON Schema, enumerations
are constraints applied to schemas that are not constrained to the declared type
of the same schema and values can be of mixed types.

There are further issues with the JSON Schema spec like the confusing existence
of embedded subschemas or why "vocabularies" for meta-schemas are special-cased
and aren't just another schema. This document is not meant to be an exhaustive
list of problems.

JSON Schema, as it stands, is a powerful JSON validation language, but a very
poor data definition language. 

For APIs, databases, LLMs, and code generation, the industry needs a great data
definition language that can also be used for validation. The priorities for the
vast majority of practical future applications of JSON Schema are upside down
from the current state of the spec.

This set of documents, _JSON Structure_ is a proposal to completely
refactor JSON Schema into:

1. a data definition language that maps from and to code and databases in a
   straightforward way and also takes typical type reuse and extensibility
   patterns into account. 
2. a set of optional extensions that provide the powerful validation capabilities
   that JSON Schema is known for.

In addition, JSON Structure has a vastly expanded built-in type system that is
not limited to the JSON primitives and includes many extended types that are
relevant for modern data processing. The type system also directly addresses
common pitfalls of the JSON primitives, such as the limited range and precision
of numbers.

Optional extensions directly support multi-language documentation and alternate
names and descriptions for properties and types as well as annotations for
scientific units and currencies based on international standards.

## 2. Key Concepts

JSON Structure is designed to look and feel very much like the JSON Schema
drafts you already know, but some rules have been tightened up to make it easier to
understand and use. Therefore, existing JSON Schema documents may need to be
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
- **Namespaces:** Namespaces are a formal part of the schema language, allowing
  for more modular and deterministic schema definitions. Namespaces are used to
  scope type definitions.
- **Cross-Referencing:** The `$ref` keyword has been limited to referencing
  named types that exist within the same document. It can no longer reference
  and insert arbitrary JSON nodes and it can no longer reference external
  documents. To reuse types from other documents, you now need to use the
  `$import` keyword from the optional [import][JSTRUCT-IMPORT] spec to
  import the types you need. Once imported, you can reference types with `$ref`.

### 2.2. Extensibility Model

JSON Structure is designed to be extensible. Any schema can be extended
with custom keywords given that those do not conflict with the core schema
language or companion specifications that are "activated" for the schema
document. It's recommended for custom keywords to have a compnay- or
project-specific prefix to avoid such collisions. It's not required to declare a
formal meta-schema to use custom keywords, but it's recommended to do so.

JSON Structure is designed to be modular. The core schema language is
defined in the [JSON Structure Core][JSTRUCT-CORE] document. Companion
specifications provide additional features and capabilities that can be used to
extend the core schema language. 

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
however. _Address_ extends _AddressBase_ without adding any additional properties.

Example:

```json
{
    "$schema": "https://json-structure.github.io/meta/core//v0/#",
    "$defs" : {
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
        "$extends": "#/$defs/AddressBase",
        "properties": {
            "street": { "type": "string" }
        }
      },
      "PostOfficeBoxAddress": {
        "type": "object",
        "$extends": "#/$defs/AddressBase",
        "properties": {
            "poBox": { "type": "string" }
        }
      },
      "Address": {
        "type": "object",
        "$extends": "#/$defs/AddressBase"
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

A _add-in type_ is declared as `abstract` and `$extends` a specific type that does
not need to be abstract. For example, a add-in type _DeliveryInstructions_ might be
applied to any _StreetAddress_ types in a document:

```json
{
    "$schema": "https://json-structure.github.io/meta/core//v0/#",
    "$id": "https://schemas.vasters.com/Addresses",
    "$root": "#/$defs/StreetAddress",
    "$offers": {
        "DeliveryInstructions": "#/$defs/DeliveryInstructions"
    },
    "$defs" : {
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
        "$extends": "#/$defs/StreetAddress",
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

  1. The `$ref` keyword can only reference named types that exist within the same
     document. It can no longer reference and insert arbitrary JSON nodes and it
     can no longer reference external documents. 
  2. To reuse types from other documents, you now need to use the `$import`
     keyword from the optional [import][JSTRUCT-IMPORT] spec to import
     the types you need into the scope of the schema document. Once imported,
     you use the imported types as if they were declared in the document. To
     avoid conflicts, you can import external types into a namespace.
  3. Since types are imported and then referenced as if they were declared in
     the document, it's also possible and permitted to "shadow" imported types
     with local definitions by explicitly declaring a type with the same name
     and namespace as as the imported type.

### 2.4. Core and Companion Specifications

The following documents are part of this JSON Structure proposal:

- [JSON Structure Core][JSTRUCT-CORE]: Defines the core schema language for
  declaring data types and structures.
- [JSON Structure Alternate Names and Descriptions][JSTRUCT-ALTNAMES]: Provides
  a mechanism for declaring alternate names and symbols for types and properties,
  including for the purposes of internationalization.
- [JSON Structure Symbols, Scientific Units, and Currencies][JSTRUCT-UNITS]: 
  Defines keywords for specifying symbols, scientific units, and currency codes 
  on types and properties.
- [JSON Structure Conditional Composition][JSTRUCT-COMPOSITION]: Defines a set
  of conditional composition rules for evaluating schemas.
- [JSON Structure Validation][JSTRUCT-VALIDATION]: Specifies extensions to
  the core schema language for declaring validation rules.
- [JSON Structure Import][JSTRUCT-IMPORT]: Defines a mechanism for importing
  external schemas and definitions into a schema document.

### 2.5. Meta-Schemas

Meta-schemas are JSON Structure documents that define the structure and constraints
of schema documents themselves. Meta-schemas do not have special constructs
beyond what is available in the core schema language.

A meta-schema is referenced in a schema document using the `$schema` keyword.
The meta-schema defines the constraints that the schema document must adhere to.

The value of the `$schema` keyword is a URI that corresponds to the `$id`
declared in the meta-schema document. The URI should be a resolvable URL that
points to the meta-schema document, but for well-known meta-schemas, a schema
processor will typically not actually fetch the meta-schema document. Instead,
the schema processor will use the URI to identify the meta-schema and validate
the schema document against its copy of the meta-schema.

A meta-schema can build on another meta-schema by `$import`ing all of its
definitions and then adding additional definitions or constraints or 
by shadowing definitions from the imported meta-schema.

The ["core" meta-schema](./json-schema-core-metaschema-core.json) formally
defines the elements described in the [JSON Structure Core][JSTRUCT-CORE]
document. The "$id" of the core meta-schema is
`https://json-structure.github.io/meta/core/v0`.

The ["extended" meta-schema](./json-schema-metaschema-extended.json) extends the
core meta-schema with all additional features and capabilities provided by the
companion specifications and offers those features to schema authors. The "$id"
of the extended meta-schema is
`https://json-structure.github.io/meta/extended/v0`.

The ["validation" meta-schema](./json-schema-metaschema-validation.json) enables
all add-ins defined in the extended meta-schema.

## 3. Using Structure Core 

This section introduces JSON Structure by example.

### 3.1. Example: Declaring a simple object type

Here is an example of a simple object type definition:

```json
{
    "$schema": "https://json-structure.github.io/meta/core//v0/#",
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

Below is an example schema that defines a simple profile with a few more extended
types:

```json
{
    "$schema": "https://json-structure.github.io/meta/core//v0/#",
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
    "$schema": "https://json-structure.github.io/meta/core//v0/#",
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

### 4.1. Example: Declaring reusable types in `$defs`

To define reusable types, you can use the `$defs` keyword to define types that
can be referenced by other types in the same document. Here is an example:

```json
{
    "$schema": "https://json-structure.github.io/meta/core//v0/#",
    "type": "object",
    "name": "UserProfile",
    "properties": {
        "username": { "type": "string" },
        "dateOfBirth": { "type": "date" },
        "lastSeen": { "type": "datetime" },
        "score": { "type": "int64" },
        "balance": { "type": "decimal", "precision": 20, "scale": 2 },
        "isActive": { "type": "boolean" },
        "address": { "type" : { "$ref": "#/$defs/Address" } }
    },
    "required": ["username", "birthdate"],
    "$defs": {
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

In this example, the `Address` type is declared in the `$defs` section and can be
referenced by other types in the same document using the `$ref` keyword. Mind
that the `$ref` keyword can now only reference types declared in the `$defs`
section of the same document. The keyword can only be used where a type is
expected.

### 4.2. Example: Structuring types with namespaces

Namespaces are used to scope type definitions. Here is an example of how to use
namespaces to structure your types, with two differing `Address` types:

```json
{
    "$schema": "https://json-structure.github.io/meta/core//v0/#",
    "type": "object",
    "name": "UserProfile",
    "properties": {
        "username": { "type": "string" },
        "dateOfBirth": { "type": "date" },
        "networkAddress": { "type" : { "$ref": "#/$defs/Network/Address" } },
        "physicalAddress": { "type": { "$ref": "#/$defs/Physical/Address" } }
    },
    "required": ["username", "birthdate"],
    "$defs": {
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

This example shows how to declare an array of strings, which is not much different
from defining an object:

```json
{
    "$schema": "https://json-structure.github.io/meta/core//v0/#",
    "type": "array",
    "items": { "type": "string" }
}
```

You can also declare an array of a locally declared compound type, but you can not
reference the type from elsewhere in the schema:

```json
{
    "$schema": "https://json-structure.github.io/meta/core//v0/#",
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
    "$schema": "https://json-structure.github.io/meta/core//v0/#",
    "type": "array",
    "items": { "type" : { "$ref": "#/$defs/Person" } },
    "$defs": {
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
    "$schema": "https://json-structure.github.io/meta/core//v0/#",
    "type": "map",
    "values": { "type": { "$ref": "#/$defs/Color" } },
    "$defs": {
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
    "$schema": "https://json-structure.github.io/meta/core//v0/#",
    "type": "set",
    "items": { "type": "string" }
}
```

Sets differ from arrays in that they are unordered and contain only unique
elements. The schema above would match the following instance data:

```json
["apple", "banana", "cherry"]
```

## 5. Using Companion Specifications

The JSON Structure Core specification is designed to be extensible through companion
specifications that provide additional features and capabilities. 

The extended schema that includes all companion specifications is identified by
the `https://json-structure.github.io/meta/extended/v0` URI. Each
companion specification is identified by a unique identifier that can be used in
the `$uses` attribute to activate the companion specification for the schema
document.

The feature identifiers for the companion specifications are:
- `Altnames`: Alternate names and descriptions for properties and types.
- `Units`: Symbols, scientific units, and currencies for numeric properties.
- `Conditionals`: Conditional composition and validation rules.
- `Imports`: Importing types from other schema documents.
- `Validation`: Validation rules for JSON data.

### 5.1. Example: Using the `altnames` Keyword

The [JSON Structure Alternate Names and Descriptions][JSTRUCT-ALTNAMES] companion
specification introduces the `altnames` keyword to provide alternate names for
properties and types. Alternate names provide additional mappings that schema
processors may use for encoding, decoding, or user interface display.

Here is an example of how to use the `altnames` keyword:

```json
{
    "$schema": "https://json-structure.github.io/meta/extended//v0/#",
    "$uses": ["Altnames"],
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

The `json` key is used to specify alternate names for JSON encoding, meaning that if
the schema is used to encode or decode JSON data, the alternate key MUST be used
instead of the name in the schema.

Keys beginning with `lang:` are reserved for providing localized alternate names that
can be used for user interface display. Additional keys can be used for custom
purposes, subject to no conflicts with reserved keys or prefixes.

### 5.2. Example: Using the `altenums` Keyword

The [JSON Structure Alternate Enumerations][JSTRUCT-ALTNAMES] companion
specification introduces the `altenums` keyword to provide alternative
representations for enumeration values defined by a type using the `enum`
keyword. Alternate symbols allow schema authors to map internal enum values to
external codes or localized display symbols.

Here is an example of how to use the `altenums` keyword:

```json
{
    "$schema": "https://json-structure.github.io/meta/extended//v0/#",
    "$uses": ["Altnames"],
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
    "$schema": "https://json-structure.github.io/meta/extended//v0/#",
    "$uses": ["Units"],
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
keyword allows schema authors to specify the currency for monetary properties and
provides a standard way to encode and decode monetary values with currencies.

Here is an example of how to use the `currency` keyword:

```json
{
    "$schema": "https://json-structure.github.io/meta/extended//v0/#",
    "$uses": ["Units"],
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

The [JSON Structure Conditionals][JSTRUCT-COMPOSITION] companion
specification introduces conditional composition constructs for combining multiple
schema definitions. In particular, this specification defines the semantics,
syntax, and constraints for the keywords `allOf`, `anyOf`, `oneOf`, and `not`,
as well as the `if`/`then`/`else` conditional construct.

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

