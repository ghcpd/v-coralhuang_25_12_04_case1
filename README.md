# user_display - refactor

This repository contains a modular refactor of `user_display_original.py` into a package designed for performance and extensibility.

Structure:
- `user_display/` - package with store, filters, formatters, validation, metrics, logging
- `user_display_optimized.py` - compatibility wrapper exposing original API

Usage examples in `tests/` and `run_tests.ps1` for Windows.

Performance targets are included in tests. Please run `python -m pip install -r requirements.txt` then `.\

un_tests.ps1` on Windows.