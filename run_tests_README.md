# One-Click Test Runner

A PowerShell script to setup environment and run all tests with performance metrics.

## Usage

```powershell
.\run_tests.ps1
```

## What It Does

1. Creates or activates a Python virtual environment
2. Installs dependencies from requirements.txt
3. Runs all tests in tests/ directory
4. Collects and displays performance metrics
5. Generates a summary report

## Output

- Test results with pass/fail status
- Performance metrics (display, filter, lookup times)
- Coverage information (if enabled)
- Detailed error logs for failed tests
