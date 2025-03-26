# JSON Structure Python Samples & Tools

This folder contains sample Python implementations and associated pytest-based
test suites targeting the JSON Structure Core specification.

## Contents

- **json_structure_schema_validator.py**  
  A command-line tool that validates JSON schemas according to the JSON
  Structure specification. It supports all extension specifications when enabled and also allows validating extension metadata schemas that introduce new `$`-prefixed keywords in property names (when enabled via `--metaschema`).

- **json_structure_instance_validator.py**  
  A validator for JSON document instances against JSON Structure schemas.  
  It supports all core constructs including abstract types, `$extends`,
  `$offers/$uses`, conditional composition, and additional validation addins.

## Test Suites

- **test_json_schema_validator_core.py**  
  Test cases ensuring full code coverage of the schema validator, verifying
  valid and invalid schema cases.

- **test_json_validator_core.py**  
  Test cases for the instance validator across a variety of JSON types, compound
  types, conditional rules, and addin constraints.

- **test_import.py**  
  A dedicated test for JSON Structure Import support, using temporary files and
  an import map to simulate external schema resolution.

## Usage

1. **Schema Validation:**  
   Run the schema validator via the command line:
   ```
   python json_structure_schema_validator.py [--metaschema] [--allowimport] [--importmap URI=filename ...] <path_to_json_file>
   ```
   - Use `--metaschema` to allow `$` in property names.
   - Use `--allowimport` and `--importmap` to enable external imports.

2. **Instance Validation:**  
   Validate an instance file against a schema by running:
   ```
   python json_structure_instance_validator.py <schema_file> <instance_file>
   ```

3. **Running Tests:**  
   Use pytest to run all tests:
   ```
   pytest
   ```

