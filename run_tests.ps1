param([switch]$Performance)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venv = Join-Path $root ".venv"

if (!(Test-Path $venv)) {
    python -m venv $venv
}

. "$venv\Scripts\Activate.ps1"

pip install --upgrade pip | Out-Null
pip install -r "$root\requirements.txt" | Out-Null

$pytestArgs = @("-q")
if ($Performance) {
    $env:RUN_PERF_TESTS = "1"
    $pytestArgs += "-m"
    $pytestArgs += "performance"
}

pytest @pytestArgs
