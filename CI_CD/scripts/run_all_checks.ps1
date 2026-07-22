
# Run all quality checks
Write-Host "Starting all quality checks..." -ForegroundColor Cyan

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Run linting
&amp; "$scriptPath\run_linting.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Linting failed!" -ForegroundColor Red
    exit 1
}

# Run type checking
&amp; "$scriptPath\run_typecheck.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Type checking failed!" -ForegroundColor Red
    exit 1
}

# Run tests
&amp; "$scriptPath\run_tests.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Tests failed!" -ForegroundColor Red
    exit 1
}

Write-Host "All checks passed! 🎉" -ForegroundColor Green

