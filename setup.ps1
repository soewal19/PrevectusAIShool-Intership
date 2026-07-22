
# Setup script for Claude Code Usage Analytics Platform

Write-Host "Setting up Claude Code Usage Analytics Platform..." -ForegroundColor Cyan

# Step 1: Create virtual environment (if not exists)
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Step 2: Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.venv\Scripts\Activate.ps1

# Step 3: Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Step 4: Create output dir and generate sample data
$outputDir = "output"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}
Write-Host "Generating sample telemetry data..." -ForegroundColor Yellow
python src/scripts/generate_fake_data.py --num-users 10 --num-sessions 50 --days 7 --output-dir $outputDir --seed 42

# Step 5: Ingest data into DuckDB
Write-Host "Ingesting and validating data..." -ForegroundColor Yellow
$env:POLARS_SKIP_CPU_CHECK="1"
python -c "from src.infrastructure.duckdb_repository import DuckDBTelemetryRepository; repo = DuckDBTelemetryRepository(); errors = repo.ingest_from_files('output/telemetry_logs.jsonl', 'output/employees.csv'); print('Data ingestion complete!'); print('Errors:', errors[:10] if errors else 'None')"

Write-Host ""
Write-Host "Setup complete! 🎉" -ForegroundColor Green
Write-Host ""
Write-Host "To start the dashboard:" -ForegroundColor Cyan
Write-Host "  .venv\Scripts\Activate.ps1"
Write-Host "  streamlit run src/presentation/dashboard.py"
Write-Host ""
