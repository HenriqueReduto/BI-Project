# Reproduce the raw-data exploration

From the BI Project root:

```powershell
python -m pip install -r requirements-analysis.txt
python scripts/profile_raw_data.py
```

Use an existing suitable Python environment; dependencies are the tested pandas/numpy versions, not Fabric runtime requirements. The installation command is needed only if these versions are absent. This run used Codex's bundled Python environment, with no installation into the project.

The script resolves the project root from its own location, so it can also run from another working directory. Optional arguments: `--project <project-folder>`, `--output <analysis-folder>`, and `--chunksize 100000`. Rerunning replaces generated results in the analysis output folder. It never writes to `data/raw`.

## Results

Default output: `outputs/raw-data-analysis/`.

- `report.md`: concise findings and project-guideline assessment.
- `report.html`: searchable, sortable field explorer with all feature interpretations and statistics.
- `column_profile.csv`: one record per dataset/field, with missingness, distinct counts, applicable mean/median, ranges, parse failures, potential outliers, and semantic checks.
- `profile.json`: complete machine-readable evidence, value frequencies, duplicate-key checks, date ranges, raw SHA-256 hashes, archive/extraction equality, and environment versions.
- `room_type_summary.csv`, `geography_summary.csv`, `reviews_by_year.csv`: compact exploratory breakdowns.

## Method and limits

All CSV records and GeoJSON features are processed, without sampling. Original gzip files are checked against their decompressed copies instead of counted as extra datasets. Summary exports are profiled separately but overlap the detailed exports. Statistics use exact frequency tables in temporary SQLite storage, so memory usage is bounded by a chunk plus field-level distinct numeric values. Temporary disk usage grows with the input's cardinality; allow several GB of scratch space. Scratch tables are removed after use.

Empty fields count as missing. Whitespace-only fields are tracked separately. Mean/median are meaningful for numeric measures and coordinates; identifiers, text, dates, and boolean categories are labelled N/A. Percentages remain on the 0–100 scale. Quartiles/medians use exact linear interpolation; outliers use 1.5×IQR and require interpretation. Currency symbols are formatting, not sufficient evidence of currency. Raw text distinct counts are exact; top values are displayed for compact fields, with complete category counts when there are at most 50 categories. Large free text, names, URLs and geometry values are not reproduced in the report.

This is exploratory Python code, not a replacement for the assignment's Microsoft Fabric ETL. Fabric implementation, the four lab-prescribed quality checks, teacher feedback, and submission evidence remain separate requirements. The public legacy data dictionary does not document all newer fields; field interpretations that lack confirmation are explicitly marked.

Source references: [Inside Airbnb catalogue](https://insideairbnb.com/get-the-data/), [data dictionary](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit), and [assumptions](https://insideairbnb.com/data-assumptions/), consulted 20 October 2026; assignment guide saved in `docs/source/`.
