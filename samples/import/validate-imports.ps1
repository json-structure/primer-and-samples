# Test JSON Structure Import Extension Examples
Write-Host "Testing JSON Structure Import Extension Examples" -ForegroundColor Yellow
Write-Host "=" * 60

# Test library schemas first 
Write-Host "`nTesting Library Schemas:" -ForegroundColor Cyan
$libraries = @(
    "02-namespace-import\person-library\schema.struct.json",
    "02-namespace-import\financial-library\schema.struct.json"
)

foreach ($lib in $libraries) {
    $result = python "..\py\json_structure_schema_validator.py" --extended --allowimport $lib 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $lib" -ForegroundColor Green
    } else {
        Write-Host "✗ $lib`: $result" -ForegroundColor Red
    }
}

# Test import example schemas
Write-Host "`nTesting Import Example Schemas:" -ForegroundColor Cyan
$importSchemas = @(
    "01-root-import\schema.struct.json",
    "02-namespace-import\schema.struct.json", 
    "03-importdefs-only\schema.struct.json",
    "04-shadowing\schema.struct.json"
)

# No longer need import maps since using relative paths
foreach ($schema in $importSchemas) {
    $result = python "..\py\json_structure_schema_validator.py" --extended --allowimport $schema 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $schema" -ForegroundColor Green
    } else {
        Write-Host "✗ $schema`: $result" -ForegroundColor Red
    }
}

# Test example instances
Write-Host "`nTesting Example Instances:" -ForegroundColor Cyan
$instances = @(
    @("01-root-import\example.json", "01-root-import\schema.struct.json"),
    @("02-namespace-import\example.json", "02-namespace-import\schema.struct.json"),
    @("03-importdefs-only\example.json", "03-importdefs-only\schema.struct.json"),
    @("04-shadowing\example.json", "04-shadowing\schema.struct.json")
)

foreach ($test in $instances) {
    $instance = $test[0]
    $schema = $test[1]
    $result = python "..\py\json_structure_instance_validator.py" --extended $instance $schema 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $instance" -ForegroundColor Green
    } else {
        Write-Host "✗ $instance`: $result" -ForegroundColor Red
    }
}

Write-Host "`nImport Extension Validation Complete!" -ForegroundColor Yellow