# JSON Structure Import Extension Examples

This directory contains comprehensive examples demonstrating the JSON Structure Import Extension features. The Import Extension allows modular schema composition through the `$import` and `$importdefs` keywords.

## Examples Overview

The examples are organized in numbered directories, each containing a schema (`schema.struct.json`) and optionally example instances:

### Import Pattern Examples  
- **01-root-import/** - Direct root-level import of entire schemas
- **02-namespace-import/** - Namespace-qualified imports with prefixes (contains library schemas)
  - **person-library/** - Reusable person and contact information types
  - **financial-library/** - Reusable financial and payment types
- **03-importdefs-only/** - Importing only definitions without exposing root type
- **04-shadowing/** - Namespace shadowing and conflict resolution

## Key Features Demonstrated

### Import Mechanisms
- **`$import`**: Direct import of schemas with optional namespace prefixes
- **`$importdefs`**: Import only the definitions from external schemas
- **Namespace management**: Organize imported types under prefixed namespaces
- **Shadowing resolution**: Handle naming conflicts between imported schemas

### Advanced Patterns
- **Modular design**: Reusable library schemas for common types
- **Namespace organization**: Clean separation of imported type hierarchies
- **Local extensions**: Extending imported types with additional properties
- **Mixed imports**: Combining direct imports and definition-only imports
- **Relative paths**: Local file imports for development and testing

## Validation

Use the included PowerShell script to validate all examples:

```powershell
.\validate-imports.ps1
```

This script validates:
1. Library schemas for correctness
2. Import example schemas (schema validation may show URI errors with relative paths)
3. Example instances against their schemas (all pass validation)

## Technical Notes

- Import URIs now use relative paths for local development
- Library schemas are co-located with the examples that use them most
- All example instances validate successfully
- Schema validation may show warnings about relative URIs but functionality works correctly
- The reorganized structure demonstrates real-world modular schema development patterns