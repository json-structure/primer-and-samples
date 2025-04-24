# encoding: utf-8
"""
test_json_structure_schema_validator.py

Pytest-based test suite for the JSON Structure schema validator.
It includes both valid and invalid schemas that probe corner conditions,
including testing of union types, $ref, $extends, namespaces (including empty namespaces),
JSON pointers, enum/const usage, and the --metaschema parameter (allowing '$' in property names).
"""

import json
import pytest
from json_structure_schema_validator import validate_json_structure_schema_core

# =============================================================================
# Valid Schemas (7 Cases)
# =============================================================================

# Case 1: Minimal valid schema with 'any' type.
VALID_MINIMAL = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/minimal",
    "name": "MinimalSchema",
    "type": "any"
}

# Case 2: Valid object schema with properties and required field.
VALID_OBJECT = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/object",
    "name": "Person",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "int32"}
    },
    "required": ["name"]
}

# Case 3: Valid schema using $ref to a type declared in definitions.
VALID_REF = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/ref",
    "name": "RefSchema",
    "type": {"$ref": "#/definitions/SomeType"},
    "definitions": {
        "SomeType": {
            "name": "SomeType",
            "type": "string"
        }
    }
}

# Case 4: Valid union type combining a primitive and a $ref.
VALID_UNION = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/union",
    "name": "UnionSchema",
    "type": ["string", {"$ref": "#/definitions/OtherType"}],
    "definitions": {
        "OtherType": {
            "name": "OtherType",
            "type": "int32"
        }
    }
}

# Case 5: Valid object type using $extends; properties are optional in extending type.
VALID_EXTENDS = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/extends",
    "name": "ExtendedSchema",
    "type": "object",
    "$extends": "#/definitions/BaseType",
    "definitions": {
        "BaseType": {
            "name": "BaseType",
            "type": "object",
            "properties": {
                "baseProp": {"type": "string"}
            }
        }
    }
}

# Case 6: Valid schema with property name containing '$', allowed with metaschema flag.
VALID_ALLOW_DOLLAR = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/allow_dollar",
    "name": "AllowDollarSchema",
    "type": "object",
    "properties": {
        "$custom": {"type": "string"}
    }
}

# Case 7: Valid empty namespace: no 'type' or '$ref' so it is a non-schema (namespace)
VALID_NAMESPACE_EMPTY = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/empty_namespace",
    "name": "EmptyNamespace"
}

# Case 8: Valid tuple type with implicit required properties and tuple order
VALID_TUPLE = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/tuple",
    "name": "PersonTuple",
    "type": "tuple",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "int32"}
    },
    "tuple": ["name", "age"]
}

VALID_SCHEMAS = [
    VALID_MINIMAL,
    VALID_OBJECT,
    VALID_REF,
    VALID_UNION,
    VALID_EXTENDS,
    VALID_ALLOW_DOLLAR,  # must be validated with allow_dollar=True
    VALID_NAMESPACE_EMPTY,
    VALID_TUPLE,
]

# =============================================================================
# Invalid Schemas (20 Cases)
# =============================================================================

# Case 1: Missing required '$schema' keyword.
INVALID_MISSING_SCHEMA = {
    "$id": "https://example.com/schema/missing_schema",
    "name": "MissingSchema",
    "type": "any"
}

# Case 2: Missing required '$id' keyword.
INVALID_MISSING_ID = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "name": "MissingID",
    "type": "any"
}

# Case 3: Both 'type' and '$root' present at the root.
INVALID_BOTH_TYPE_AND_ROOT = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/both",
    "$root": "#/definitions/SomeRoot",
    "type": "any"
}

# Case 4: Object type missing 'properties' and not using '$extends'.
INVALID_NO_PROPERTIES = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/no_properties",
    "name": "NoPropsObject",
    "type": "object"
}

# Case 5: Union with inline compound type (not allowed).
INVALID_UNION_INLINE = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/invalid_union",
    "name": "InvalidUnion",
    "type": [
        "string",
        {"type": "object", "properties": {"foo": {"type": "int32"}}}
    ]
}

# Case 6: $ref property is not a string.
INVALID_REF_NOT_STRING = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/ref_not_string",
    "name": "RefNotString",
    "type": {"$ref": 123}
}

# Case 7: $ref pointer does not resolve (non-existent).
INVALID_BAD_REF = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/bad_ref",
    "name": "BadRef",
    "type": {"$ref": "#/definitions/NonExistent"}
}

# Case 8: definitions is not an object.
INVALID_DEFS_NOT_OBJECT = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/defs_not_object",
    "definitions": "not an object"
}

# Case 9: 'required' keyword used in a non-object type.
INVALID_REQUIRED_NON_OBJECT = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/required_non_object",
    "name": "RequiredNonObject",
    "type": "string",
    "required": ["someProp"]
}

# Case 10: 'additionalProperties' used in a non-object type.
INVALID_ADDITIONAL_NON_OBJECT = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/additional_non_object",
    "name": "AdditionalNonObject",
    "type": "int32",
    "additionalProperties": False
}

# Case 11: 'abstract' keyword not boolean.
INVALID_ABSTRACT_NOT_BOOL = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/abstract_not_bool",
    "name": "AbstractNotBool",
    "type": "string",
    "abstract": "true"
}

# Case 12: $extends pointer does not resolve.
INVALID_EXTENDS_BAD_POINTER = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/extends_bad",
    "name": "ExtendsBad",
    "type": "object",
    "$extends": "#/nonexistent"
}

# Case 13: 'properties' is not an object.
INVALID_PROPERTIES_NOT_OBJECT = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/props_not_object",
    "name": "PropsNotObj",
    "type": "object",
    "properties": ["not", "an", "object"]
}

# Case 14: 'enum' is not a list.
INVALID_ENUM_NOT_LIST = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/enum_not_list",
    "name": "EnumNotList",
    "type": "string",
    "enum": "not a list"
}

# Case 15: 'enum' used with a compound type.
INVALID_ENUM_COMPOUND = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/enum_compound",
    "name": "EnumCompound",
    "type": "object",
    "enum": ["a", "b"]
}

# Case 16: 'const' used with a compound type.
INVALID_CONST_COMPOUND = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/const_compound",
    "name": "ConstCompound",
    "type": "object",
    "const": "some value"
}

# Case 17: $offers is not an object.
INVALID_OFFERS_NOT_OBJECT = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/offers_not_obj",
    "name": "OffersNotObj",
    "type": "any",
    "$offers": "should be an object"
}

# Case 18: $offers key is not a string.
INVALID_OFFERS_KEY_NOT_STRING = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/offers_key_not_str",
    "name": "OffersKeyNotStr",
    "type": "any",
    "$offers": {123: "#/definitions/SomeType"},
    "definitions": {
        "SomeType": {
            "name": "SomeType",
            "type": "string"
        }
    }
}

# Case 19: $offers value list contains a non-string.
INVALID_OFFERS_VALUE_LIST_NONSTRING = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/offers_value_list_nonstr",
    "name": "OffersValueListNonStr",
    "type": "any",
    "$offers": {"OfferKey": ["#/definitions/SomeType", 123]},
    "definitions": {
        "SomeType": {
            "name": "SomeType",
            "type": "string"
        }
    }
}

# Case 20: $ref pointer that does not start with '#'
INVALID_REF_POINTER_NO_HASH = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/ref_no_hash",
    "name": "RefNoHash",
    "type": {"$ref": "invalid_pointer"}
}

# Case 21: Invalid definitions section without a top-level map
INVALID_DEFS_NO_MAP = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/defs_no_map",
    "name": "DefsNoMap",
    "type": "object",
    "definitions": "not a map"
}

#Case 22: Invalid definitions section with a type definition at the root of definitions
INVALID_DEFS_ROOT_TYPE = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/defs_root_type",
    "name": "DefsRootType",
    "type": "object",
    "definitions": {
        "name": "RootType",
        "type": "string"
    }
}

#Case 23: Not an object
INVALID_NOT_OBJECT = "test"

# Case 24: $schema is not an absolute URI.
INVALID_NOT_ABSOLUTE_URI = {
    "$schema": "not an absolute URI",
}

# Case 25: $schema is not a string.
INVALID_NOT_STRING = {
    "$schema": 123,
}

# Case 26: Tuple type missing 'tuple' keyword.
INVALID_TUPLE_MISSING_KEYWORD = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/invalid_tuple_missing",
    "name": "MissingTupleKeyword",
    "type": "tuple",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "int32"}
    }
}

# Case 27: 'tuple' keyword is not an array of strings.
INVALID_TUPLE_NOT_ARRAY = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/invalid_tuple_not_array",
    "name": "TupleNotArray",
    "type": "tuple",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "int32"}
    },
    "tuple": "name,age"
}

# Case 28: 'tuple' contains non-string elements.
INVALID_TUPLE_NONSTRING_ITEM = {
    "$schema": "https://json-structure.org/meta/core/v0/#",
    "$id": "https://example.com/schema/invalid_tuple_nonstring",
    "name": "TupleNonString",
    "type": "tuple",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "int32"}
    },
    "tuple": ["name", 42]
}

INVALID_SCHEMAS = [
    INVALID_MISSING_SCHEMA,
    INVALID_MISSING_ID,
    INVALID_BOTH_TYPE_AND_ROOT,
    INVALID_NO_PROPERTIES,
    INVALID_UNION_INLINE,
    INVALID_REF_NOT_STRING,
    INVALID_BAD_REF,
    INVALID_DEFS_NOT_OBJECT,
    INVALID_REQUIRED_NON_OBJECT,
    INVALID_ADDITIONAL_NON_OBJECT,
    INVALID_ABSTRACT_NOT_BOOL,
    INVALID_EXTENDS_BAD_POINTER,
    INVALID_PROPERTIES_NOT_OBJECT,
    INVALID_ENUM_NOT_LIST,
    INVALID_ENUM_COMPOUND,
    INVALID_CONST_COMPOUND,
    INVALID_OFFERS_NOT_OBJECT,
    INVALID_OFFERS_KEY_NOT_STRING,
    INVALID_OFFERS_VALUE_LIST_NONSTRING,
    INVALID_REF_POINTER_NO_HASH,
    INVALID_DEFS_NO_MAP,
    INVALID_DEFS_ROOT_TYPE,
    INVALID_NOT_OBJECT,
    INVALID_NOT_ABSOLUTE_URI,
    INVALID_NOT_STRING,
    INVALID_TUPLE_MISSING_KEYWORD,
    INVALID_TUPLE_NOT_ARRAY,
    INVALID_TUPLE_NONSTRING_ITEM
]

# =============================================================================
# Pytest Test Functions
# =============================================================================

@pytest.mark.parametrize("schema", VALID_SCHEMAS)
def test_valid_schemas(schema):
    """
    Test that valid schemas produce no errors.
    For VALID_ALLOW_DOLLAR, the allow_dollar flag is set.
    """
    source_text = json.dumps(schema)
    # Enable allow_dollar flag if the schema has a property with a '$' at the start
    allow_dollar = any(key.startswith('$') for key in schema.get("properties", {}))
    errors = validate_json_structure_schema_core(schema, source_text, allow_dollar=allow_dollar)
    assert errors == []

@pytest.mark.parametrize("schema", INVALID_SCHEMAS)
def test_invalid_schemas(schema):
    """
    Test that invalid schemas produce one or more errors.
    """
    source_text = json.dumps(schema)
    errors = validate_json_structure_schema_core(schema, source_text)
    assert errors != []

# Additional test: Check that property names with '$' are rejected when allow_dollar is False.
def test_dollar_property_rejected():
    schema = {
        "$schema": "https://json-structure.org/meta/core/v0/#",
        "$id": "https://example.com/schema/dollar_rejected",
        "name": "DollarRejected",
        "type": "object",
        "properties": {
            "$invalid": {"type": "string"}
        }
    }
    source_text = json.dumps(schema)
    errors = validate_json_structure_schema_core(schema, source_text, allow_dollar=False)
    assert any("does not match" in err for err in errors)

# Additional test: Valid $offers structure.
def test_valid_offers():
    schema = {
        "$schema": "https://json-structure.org/meta/core/v0/#",
        "$id": "https://example.com/schema/offers_valid",
        "name": "OffersValid",
        "type": "any",
        "$offers": {
            "CustomOffer": "#/definitions/OfferType"
        },
        "definitions": {
            "OfferType": {
                "name": "OfferType",
                "type": "string"
            }
        }
    }
    source_text = json.dumps(schema)
    errors = validate_json_structure_schema_core(schema, source_text)
    assert errors == []
