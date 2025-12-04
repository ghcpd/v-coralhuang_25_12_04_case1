# User Display Module — Optimized & Modular

## Baseline problems
- O(n²) string concatenation; repeated JSON (de)serialization
- Random sleeps; randomized corruption and truncation
- Linear ID lookup; multi-pass filters
- Monolithic file; no validation/logging/metrics

## New architecture
```
user_display/
  __init__.py
  config.py          # env overrides, freeze mode
  logging_utils.py   # structured JSON logs
  metrics.py         # counters + timings
  errors.py
  plugins.py         # registries + entry-point loader
  index.py           # sharded hash index
  store.py           # thread-safe MVCC-like snapshots, caching
  formatters/
    base.py | compact.py | json_fmt.py | table.py
  filters/
    base.py | regex_filter.py | composite_filter.py
  validation/
    base.py | default.py
user_display_optimized.py  # API-compatible wrapper
```

## Features
- O(1) ID lookup via sharded hash index
- Buffered formatting (StringIO); multiple modes: `compact`, `json`, `table`
- Field selection and conditional regex (`regex:<field>`)
- Pluggable filters/formatters/validators via registry + entry points
- Validation with soft recovery; `_last_login_ts` pre-parsed
- Filter result caching (LRU) and optional parallel filtering (threads)
- Snapshots/clones for consistent concurrent reads
- Structured logging + metrics snapshot

## Usage examples
```python
from user_display_optimized import display_users, filter_users, get_user_by_id

out = display_users(users, show_all=True, formatter="compact")
admin = get_user_by_id(users, 42)
actives = filter_users(users, {"status": "Active", "regex:email": "@example.com$"}, parallel=True)
```

## Plugins
- Register programmatically: `register_formatter("custom", factory)`
- Optional entry points: `user_display.formatters` / `filters` / `validators` groups

## Performance benchmarking
Targets (50k users): Display <120 ms; Filter <15 ms; Lookup <0.5 ms.
Run `pytest -m performance -q` or `./run_tests.ps1` (Windows) to collect timings (with slack for CI variability).

## Development
- Install deps: `pip install -r requirements.txt`
- Run all tests: `pytest -q`
- One-click script: `run_tests.ps1`

## Notes
- `DefaultValidator` soft-fills missing fields unless `strict=True`.
- `export_users_to_string` emits JSON payload between `EXPORT_BEGIN/END` markers.
- `UserStore.display_users` accepts `include_metrics=True` to append metrics snapshot.
