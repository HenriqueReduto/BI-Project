# Austin Animal Center raw-data exploration

Active source: the two historical shelter CSVs in data/raw. The prior Inside Airbnb exploration is superseded; its code and historical validation are not evidence for these files.

## Verified full-file inspection - 26 October 2026
The standard-library CSV inspection read every record, counted exact tuples and Animal IDs, checked empty fields, and parsed DateTime using the intake US date format or Python ISO datetime parser. Date coverage reports the recorded wall-clock dates; it does not resolve timezone semantics. Current counts and file hashes are in ../validation/animal-shelter-profile.json; method and limitations are in ../validation/animal-shelter-analysis.md.

| Metric | Intakes | Outcomes |
|---|---:|---:|
| Records | 173,812 | 173,775 |
| Fields | 12 | 12 |
| Distinct Animal IDs | 156,287 | 156,237 |
| Animal IDs with multiple rows | 13,487 | 13,507 |
| Exact duplicate excess rows | 36 | 26 |
| Empty names | 49,991 | 49,784 |
| Empty outcome type | N/A | 46 |
| Empty outcome subtype | N/A | 94,115 |

155,423 Animal IDs occur in both files; 864 occur only in intakes and 814 only in outcomes. Shared IDs are not verified encounter matches. All event timestamps parsed in the preliminary inspection; 3,584 outcome strings contain explicit timezone offsets while intake strings do not. No timezone conversion has been validated.

## Implications
- Preserve original records and investigate exact duplicate candidates before removing any.
- Normalize literal NULL and category values; distinguish inapplicable subtypes from unknowns where justified.
- Age units vary; conversions require documented approximations.
- Reconstruct encounters rather than joining on Animal ID alone.
- Use linked sampling to meet the 30,000-row limit; final cohort and follow-up rules remain pending.
- Confirm primitive measures and meaningful hierarchies before committing the schema.

## Existing tooling
scripts/profile_raw_data.py and requirements-analysis.txt were created for the former Airbnb exploration. Their shelter-specific compatibility has not been validated. Do not present their old reports or script checks as current animal shelter evidence. The historical scripts/extract_csv_gz.py utility is absent from this checkout; the active source files are already CSVs. A reproducible shelter-specific profiling command is a next task.

## Sources
City of Austin historical [intakes](https://data.austintexas.gov/d/wter-evkm) and [outcomes](https://data.austintexas.gov/d/9t4d-g238), consulted 26 October 2026. Both catalogues state Public Domain. Original download date is unconfirmed. The newer ShelterBuddy datasets have different schemas and are outside this selection.

No Fabric ingestion, lab DQ execution, teacher readiness assessment, submission, or sharing is asserted.
