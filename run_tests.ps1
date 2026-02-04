# One-click test runner for Windows PowerShell
python -m pip install -r requirements.txt
pytest -q

if ($env:RUN_PERF -eq '1') {
    pytest tests/test_performance.py -q
}