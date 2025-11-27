# encoding: utf-8
"""
test_test_assets.py

Pytest-based test suite for validating schemas and instances from the
sdk/test-assets directory. These tests verify that:
1. All invalid schemas in test-assets/schemas/invalid/ fail validation
2. All invalid instances in test-assets/instances/invalid/ fail validation against their schemas

NOTE: Some test cases require validator features not yet implemented. These are tracked
in the KNOWN_*_GAPS sets and will be skipped until the corresponding validation logic is added.
"""

import json
import os
import pytest
from pathlib import Path
from json_structure_schema_validator import validate_json_structure_schema_core
from json_structure_instance_validator import JSONStructureInstanceValidator

# =============================================================================
# Path Configuration
# =============================================================================

# Find the test-assets directory relative to this file
SCRIPT_DIR = Path(__file__).parent
TEST_ASSETS_DIR = SCRIPT_DIR.parent.parent.parent / "sdk" / "test-assets"
SAMPLES_DIR = SCRIPT_DIR.parent / "core"

# Alternative paths if running from different locations
if not TEST_ASSETS_DIR.exists():
    TEST_ASSETS_DIR = Path("sdk/test-assets")
if not TEST_ASSETS_DIR.exists():
    TEST_ASSETS_DIR = Path("../../../sdk/test-assets")

if not SAMPLES_DIR.exists():
    SAMPLES_DIR = Path("primer-and-samples/samples/core")
if not SAMPLES_DIR.exists():
    SAMPLES_DIR = Path("../core")

# =============================================================================
# Known Validation Gaps
# =============================================================================

# Schema validation edge cases not yet implemented in the Python validator
KNOWN_SCHEMA_GAPS = {
    # All schema validations now pass - keeping this for future use
}

# Instance validation edge cases not yet implemented in the Python validator
KNOWN_INSTANCE_GAPS = {
    # All instance validations now pass with extended=True - keeping this for future use
}


def load_json(path: Path) -> dict:
    """Load and parse a JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


# =============================================================================
# Invalid Schema Tests
# =============================================================================

def get_invalid_schema_files():
    """Get all invalid schema files from test-assets/schemas/invalid/."""
    invalid_schemas_dir = TEST_ASSETS_DIR / "schemas" / "invalid"
    if not invalid_schemas_dir.exists():
        return []
    return list(invalid_schemas_dir.glob("*.struct.json"))


@pytest.mark.parametrize("schema_path", get_invalid_schema_files(), 
                         ids=lambda p: p.stem if hasattr(p, 'stem') else str(p))
def test_invalid_schemas_fail_validation(schema_path):
    """Each schema in test-assets/schemas/invalid/ should fail validation."""
    if schema_path.name in KNOWN_SCHEMA_GAPS:
        pytest.skip(f"Skipping {schema_path.name} - validation not yet implemented")
    
    schema = load_json(schema_path)
    # validate_json_structure_schema_core returns a list of errors (empty = valid)
    errors = validate_json_structure_schema_core(schema)
    
    assert len(errors) > 0, (
        f"Schema {schema_path.name} should be invalid but passed validation. "
        f"Description: {schema.get('description', 'No description')}"
    )


# =============================================================================
# Invalid Instance Tests  
# =============================================================================

def get_invalid_instance_files():
    """Get all invalid instance files from test-assets/instances/invalid/."""
    invalid_instances_dir = TEST_ASSETS_DIR / "instances" / "invalid"
    if not invalid_instances_dir.exists():
        return []
    
    instances = []
    for sample_dir in invalid_instances_dir.iterdir():
        if sample_dir.is_dir():
            for instance_file in sample_dir.glob("*.json"):
                instances.append((sample_dir.name, instance_file))
    return instances


def get_sample_schema(sample_name: str) -> dict:
    """Load the schema for a given sample directory name."""
    schema_path = SAMPLES_DIR / sample_name / "schema.struct.json"
    if not schema_path.exists():
        pytest.skip(f"Sample schema not found: {schema_path}")
    return load_json(schema_path)


@pytest.mark.parametrize("sample_name,instance_path", get_invalid_instance_files(),
                         ids=lambda x: f"{x[0]}/{x[1].stem}" if isinstance(x, tuple) else str(x))
def test_invalid_instances_fail_validation(sample_name, instance_path):
    """Each instance in test-assets/instances/invalid/ should fail validation against its schema."""
    test_key = f"{sample_name}/{instance_path.name}"
    if test_key in KNOWN_INSTANCE_GAPS:
        pytest.skip(f"Skipping {test_key} - validation not yet implemented")
    
    schema = get_sample_schema(sample_name)
    instance = load_json(instance_path)
    
    # Remove the _description and _schema metadata fields before validation
    instance_data = {k: v for k, v in instance.items() if not k.startswith('_')}
    
    # validate_instance() returns a list of errors (empty = valid)
    # Use extended=True to enable validation addins (maxLength, pattern, etc.)
    validator = JSONStructureInstanceValidator(schema, extended=True)
    errors = validator.validate_instance(instance_data)
    
    assert len(errors) > 0, (
        f"Instance {instance_path.name} should be invalid against {sample_name} schema but passed. "
        f"Description: {instance.get('_description', 'No description')}"
    )


# =============================================================================
# Summary Tests
# =============================================================================

def test_invalid_schemas_directory_exists():
    """Verify the invalid schemas directory exists and has files."""
    invalid_schemas_dir = TEST_ASSETS_DIR / "schemas" / "invalid"
    if not invalid_schemas_dir.exists():
        pytest.skip("test-assets/schemas/invalid/ directory not found")
    
    schema_files = list(invalid_schemas_dir.glob("*.struct.json"))
    assert len(schema_files) > 0, "No invalid schema files found"
    print(f"\nFound {len(schema_files)} invalid schema files")


def test_invalid_instances_directory_exists():
    """Verify the invalid instances directory exists and has files."""
    invalid_instances_dir = TEST_ASSETS_DIR / "instances" / "invalid"
    if not invalid_instances_dir.exists():
        pytest.skip("test-assets/instances/invalid/ directory not found")
    
    instance_count = 0
    for sample_dir in invalid_instances_dir.iterdir():
        if sample_dir.is_dir():
            instance_count += len(list(sample_dir.glob("*.json")))
    
    assert instance_count > 0, "No invalid instance files found"
    print(f"\nFound {instance_count} invalid instance files")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
