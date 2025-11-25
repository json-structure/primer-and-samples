# Test all schema and instance files
Write-Host "Testing JSON Structure Schemas and Instances" -ForegroundColor Yellow
Write-Host "=" * 50

# Test all schemas first
Write-Host "`nTesting Schemas:" -ForegroundColor Cyan
$schemas = @(
    "01-basic-person\schema.struct.json",
    "02-address\schema.struct.json", 
    "03-financial-types\schema.struct.json",
    "04-datetime-examples\schema.struct.json",
    "05-collections\schema.struct.json",
    "06-tuples\schema.struct.json",
    "07-unions\schema.struct.json",
    "08-namespaces\schema.struct.json",
    "09-extensions\schema.struct.json",
    "10-discriminated-unions\schema.struct.json",
    "11-sets-and-maps\schema.struct.json"
)

foreach ($schema in $schemas) {
    $result = python "..\py\json_structure_schema_validator.py" $schema 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $schema" -ForegroundColor Green
    } else {
        Write-Host "✗ $schema`: $result" -ForegroundColor Red
    }
}

# Test all instances
Write-Host "`nTesting Instance Files:" -ForegroundColor Cyan
$tests = @(
    @("01-basic-person\example1.json", "01-basic-person\schema.struct.json"),
    @("01-basic-person\example2.json", "01-basic-person\schema.struct.json"),
    @("01-basic-person\example3.json", "01-basic-person\schema.struct.json"),
    @("02-address\example1.json", "02-address\schema.struct.json"),
    @("02-address\example2.json", "02-address\schema.struct.json"),
    @("02-address\example3.json", "02-address\schema.struct.json"),
    @("03-financial-types\example1.json", "03-financial-types\schema.struct.json"),
    @("03-financial-types\example2.json", "03-financial-types\schema.struct.json"),
    @("03-financial-types\example3.json", "03-financial-types\schema.struct.json"),
    @("04-datetime-examples\example1.json", "04-datetime-examples\schema.struct.json"),
    @("04-datetime-examples\example2.json", "04-datetime-examples\schema.struct.json"),
    @("05-collections\example1.json", "05-collections\schema.struct.json"),
    @("05-collections\example2.json", "05-collections\schema.struct.json"),
    @("05-collections\example3.json", "05-collections\schema.struct.json"),
    @("06-tuples\example1.json", "06-tuples\schema.struct.json"),
    @("06-tuples\example2.json", "06-tuples\schema.struct.json"),
    @("06-tuples\example3.json", "06-tuples\schema.struct.json"),
    @("07-unions\example1.json", "07-unions\schema.struct.json"),
    @("07-unions\example2.json", "07-unions\schema.struct.json"),
    @("07-unions\example3.json", "07-unions\schema.struct.json"),
    @("08-namespaces\example1.json", "08-namespaces\schema.struct.json"),
    @("08-namespaces\example2.json", "08-namespaces\schema.struct.json"),
    @("08-namespaces\example3.json", "08-namespaces\schema.struct.json"),
    @("09-extensions\example1.json", "09-extensions\schema.struct.json"),
    @("09-extensions\example2.json", "09-extensions\schema.struct.json"),
    @("09-extensions\example3.json", "09-extensions\schema.struct.json"),
    @("10-discriminated-unions\example1.json", "10-discriminated-unions\schema.struct.json"),
    @("10-discriminated-unions\example2.json", "10-discriminated-unions\schema.struct.json"),
    @("10-discriminated-unions\example3.json", "10-discriminated-unions\schema.struct.json"),
    @("11-sets-and-maps\example1.json", "11-sets-and-maps\schema.struct.json"),
    @("11-sets-and-maps\example2.json", "11-sets-and-maps\schema.struct.json"),
    @("11-sets-and-maps\example3.json", "11-sets-and-maps\schema.struct.json")
)

foreach ($test in $tests) {
    $instance = $test[0]
    $schema = $test[1] 
    $result = python "..\py\json_structure_instance_validator.py" $instance $schema 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $instance" -ForegroundColor Green
    } else {
        Write-Host "✗ $instance`: $result" -ForegroundColor Red
    }
}

Write-Host "`nValidation Complete!" -ForegroundColor Yellow