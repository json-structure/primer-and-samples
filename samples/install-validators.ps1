# Install JSON Structure validators from the SDK
# This installs the json-structure package which provides:
#   - json-structure-check (schema validator)  
#   - json-structure-validate (instance validator)
# Or use via: python -m json_structure.schema_validator / python -m json_structure.instance_validator

Write-Host "Installing JSON Structure Validators" -ForegroundColor Yellow
Write-Host "=" * 50

# Get the path to the SDK python package (relative to this script)
$sdkPath = Resolve-Path (Join-Path $PSScriptRoot "..\..\sdk\python") -ErrorAction SilentlyContinue

if ($sdkPath -and (Test-Path $sdkPath)) {
    Write-Host "Installing from local SDK: $sdkPath" -ForegroundColor Cyan
    pip install -e $sdkPath
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Installation successful!" -ForegroundColor Green
        Write-Host "`nAvailable commands:" -ForegroundColor Yellow
        Write-Host "  python -m json_structure.schema_validator <schema.json>" -ForegroundColor White
        Write-Host "  python -m json_structure.instance_validator <instance.json> <schema.json>" -ForegroundColor White
        Write-Host "`nOr if scripts are in PATH:" -ForegroundColor Yellow
        Write-Host "  json-structure-check <schema.json>" -ForegroundColor White
        Write-Host "  json-structure-validate <instance.json> <schema.json>" -ForegroundColor White
    } else {
        Write-Host "✗ Installation failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "SDK not found locally, installing from PyPI..." -ForegroundColor Yellow
    pip install json-structure
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Installation successful!" -ForegroundColor Green
    } else {
        Write-Host "✗ Installation failed!" -ForegroundColor Red
        exit 1
    }
}
