# Security Skills Benchmarks

Wave 5 benchmark fixtures are synthetic, deterministic conformance cases for the research-case validator and advisory skill router. They do not execute exploit payloads or target live external systems.

- `cases/` contains six reviewed fixtures in each benchmark category.
- `suites/core.json` includes all 36 fixtures.
- `suites/portability.json` is a 12-fixture cross-platform smoke subset.

Run `python scripts/validate_benchmarks.py` before executing suites.
