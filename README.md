# user_display — High-performance, modular user display system

This repository demonstrates an optimized, modular replacement for a chaotic baseline `user_display_original.py`.

Highlights
- Thread-safe `UserStore` with O(1) lookups and snapshotting
- Extensible formatters (compact, json, table)
- Flexible filters (regex, composite) and plugin registration
- Validation with soft-recovery and metrics
- Tests including concurrency and optional 50k performance test

Usage
1. Install dev requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate; pip install -r requirements.txt
```

2. Run tests:

```powershell
.\run_tests.ps1
```

Performance tests
- The 50k performance test is disabled by default; enable it with RUN_PERF=1 in environment.

Design
- user_display/: modular package (store, filters, formatters, validation)
- user_display_optimized.py: compatibility wrapper that preserves the public API
