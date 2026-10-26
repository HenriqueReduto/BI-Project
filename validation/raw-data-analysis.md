> HISTORICAL / SUPERSEDED: the following 20 October 2026 checks describe the former Airbnb source. They do not validate the shelter CSVs. Refer to animal-shelter-analysis.md and animal-shelter-profile.json for current evidence. The old linked output files are absent from this checkout.

# Local EDA verification — 20 October 2026

- PASS: seven logical files, 128 fields, all rows processed.
- PASS: original gzip payloads equal extracted CSVs (SHA-256).
- PASS: raw-file SHA-256 hashes unchanged before/after analysis.
- PASS: numeric parsing and weighted quantiles checked on independent NumPy examples.
- PASS: complete script exercised on a small fixture including empty date/numeric fields and GeoJSON.
- PASS: full-data listing row/ID counts and price missingness, mean, median, and IQR count matched independent direct pandas calculations.
- Full metrics: ../outputs/raw-data-analysis/profile.json. Human report: ../outputs/raw-data-analysis/report.md.
- NOT RUN: Fabric load/SQL/ETL, lab-defined DQ checks, Moodle submission or sharing.
- Local profiling checks are not the required four lab quality checks.
