# JSON Structure Core Examples

This directory contains comprehensive examples of JSON Structure schemas and instances that demonstrate the features of the JSON Structure Core specification.

## Directory Structure

```
core/
├── 01-basic-person/                    # Simple object schema with primitive types
│   ├── schema.struct.json
│   ├── example1.json
│   ├── example2.json
│   └── example3.json
├── 02-address/                         # Object with required/optional fields and enums
│   ├── schema.struct.json
│   ├── example1.json
│   ├── example2.json
│   └── example3.json
├── 03-financial-types/                 # Complex schema with decimal types and nested objects
│   ├── schema.struct.json
│   ├── example1.json
│   ├── example2.json
│   └── example3.json
├── 04-datetime-examples/               # DateTime types with UUID and duration
│   ├── schema.struct.json
│   ├── example1.json
│   └── example2.json
├── 05-collections/                     # Arrays, sets, maps, and product catalogs
│   ├── schema.struct.json
│   ├── example1.json
│   ├── example2.json
│   └── example3.json
├── 06-tuples/                         # Tuple types with fixed-order elements
│   ├── schema.struct.json
│   ├── example1.json
│   ├── example2.json
│   └── example3.json
├── 07-unions/                         # Type unions for flexible data handling
│   ├── schema.struct.json
│   ├── example1.json
│   ├── example2.json
│   └── example3.json
├── 08-namespaces/                     # Namespace organization and type definitions
│   ├── schema.struct.json
│   ├── example1.json
│   ├── example2.json
│   └── example3.json
├── 09-extensions/                     # Schema inheritance and extension patterns
│   ├── schema.struct.json
│   ├── example1.json
│   ├── example2.json
│   └── example3.json
├── 10-discriminated-unions/           # Tagged unions with discriminators
│   ├── schema.struct.json
│   ├── example1.json
│   ├── example2.json
│   └── example3.json
├── 11-sets-and-maps/                  # Collection types with complex elements
│   ├── schema.struct.json
│   ├── example1.json
│   ├── example2.json
│   └── example3.json
└── validate-all.ps1                   # PowerShell script to validate all schemas and instances
```

## Schema Examples Overview

### 1. Basic Person (`01-basic-person/`)
- **Demonstrates**: Primitive types (`string`, `date`, `boolean`)
- **Features**: Required fields, optional fields, type annotations
- **Real-world use**: User profiles, contact information

### 2. Address (`02-address/`) 
- **Demonstrates**: Enumerations, required vs optional properties
- **Features**: Country code validation, additional properties control
- **Real-world use**: Shipping addresses, location data

### 3. Financial Types (`03-financial-types/`)
- **Demonstrates**: High-precision `decimal` type, nested object references
- **Features**: Currency handling, precision/scale annotations, complex business documents
- **Real-world use**: Invoicing systems, financial calculations

### 4. DateTime Examples (`04-datetime-examples/`)
- **Demonstrates**: Date/time types (`date`, `datetime`, `duration`), UUID types
- **Features**: Time zone handling, recurrence patterns, event scheduling
- **Real-world use**: Calendar applications, scheduling systems

### 5. Collections (`05-collections/`)
- **Demonstrates**: Collection types (`array`, `set`, `map`)
- **Features**: Product catalogs, lookup maps, unique sets
- **Real-world use**: E-commerce catalogs, inventory systems

### 6. Tuples (`06-tuples/`)
- **Demonstrates**: Fixed-position tuple types
- **Features**: Geographic coordinates, scientific data, color values
- **Real-world use**: Data analytics, mapping applications, scientific datasets

### 7. Unions (`07-unions/`)
- **Demonstrates**: Type unions for handling multiple data formats
- **Features**: Document processing, error handling, flexible input/output
- **Real-world use**: API responses, document processing pipelines

### 8. Namespaces (`08-namespaces/`)
- **Demonstrates**: Namespace organization for modular schemas
- **Features**: Type organization, namespace prefixes, clean architecture
- **Real-world use**: Large-scale schema organization, enterprise data models

### 9. Extensions (`09-extensions/`)
- **Demonstrates**: Schema inheritance using `$extends` keyword
- **Features**: Abstract base types, concrete implementations, code reuse
- **Real-world use**: Object-oriented data modeling, type hierarchies

### 10. Discriminated Unions (`10-discriminated-unions/`)
- **Demonstrates**: Tagged unions with discriminator properties
- **Features**: Type discrimination, polymorphic data, variant types
- **Real-world use**: Event systems, message processing, API responses

### 11. Sets and Maps (`11-sets-and-maps/`)
- **Demonstrates**: Advanced collection types with complex elements
- **Features**: Unique sets, key-value mappings, structured collections
- **Real-world use**: Configuration management, lookup tables, unique constraints

## JSON Structure Features Demonstrated

### Type System
- **Primitive types**: `string`, `number`, `boolean`, `null`
- **Extended primitives**: `int32`, `uint32`, `int64`, `uint64`, `decimal`, `date`, `datetime`, `time`, `duration`, `uuid`, `uri`, `binary`, `jsonpointer`
- **Compound types**: `object`, `array`, `set`, `map`, `tuple`, `choice`, `any`

### Schema Features
- **Type references**: `$ref` for reusable types
- **Namespaces**: Organized type definitions
- **Annotations**: `description`, `examples`, `maxLength`, `precision`, `scale`
- **Constraints**: `required`, `enum`, `const`, `additionalProperties`

### Advanced Features
- **Type unions**: Multiple type choices
- **Reusable definitions**: Modular schema design
- **Rich metadata**: Comprehensive documentation

## Validation

All schemas and instances have been validated using the official JSON Structure validators:

```powershell
# Validate all schemas and instances
.\validate-all.ps1
```

### Manual Validation Examples

```bash
# Validate a schema
python ..\py\json_structure_schema_validator.py 01-basic-person\schema.struct.json

# Validate an instance against its schema  
python ..\py\json_structure_instance_validator.py 01-basic-person\example1.json 01-basic-person\schema.struct.json
```

## Key Design Principles Demonstrated

1. **Strict Typing**: Every field has a precise type definition
2. **Modularity**: Reusable type definitions in namespaces
3. **Determinism**: Clear, unambiguous schema specifications
4. **Rich Type System**: Beyond basic JSON types for real-world data modeling
5. **Self-Documentation**: Comprehensive descriptions and examples
6. **Validation-Ready**: All examples validate against their schemas

## Usage in Applications

These examples can serve as:
- **Templates** for creating new JSON Structure schemas
- **Learning materials** for understanding JSON Structure concepts
- **Test cases** for JSON Structure implementations
- **Reference implementations** for common business scenarios

## Extension Points

The schemas demonstrate extensibility through:
- Custom annotations (following the `$` prefix convention)
- Namespace organization for modular design
- Type composition and references
- Rich metadata for tooling integration

---

*These examples conform to the JSON Structure Core specification by C. Vasters (Microsoft, 2025)*