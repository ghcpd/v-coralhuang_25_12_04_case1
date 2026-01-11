param(
    [switch]$perf
)

Write-Host "Setting up virtualenv and installing requirements (if missing)"
if (-not (Test-Path -Path .venv)) {
    python -m venv .venv; if ($LASTEXITCODE -ne 0) { Write-Error "Failed: creating venv"; exit 1 }
}
. .\.venv\Scripts\Activate
pip install -q -r requirements.txt

$env:RUN_PERF = $false
if ($perf) { $env:RUN_PERF = "1" }

Write-Host "Running pytest..."
pytest -q
