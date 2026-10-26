# Animal shelter inspection and documentation validation - 26 October 2026

## Actual local inspection
- PASS: read both complete raw CSVs with Python standard-library csv.DictReader; counted rows, IDs, exact tuple duplicates, empty strings, parsed event dates, and per-year totals.
- PASS: intake records 173,812; outcome records 173,775; both contain 12 fields.
- PASS: event timestamp parsing completed with no failures using the recorded US intake format and ISO outcome format. This does not establish timezone correctness.
- PASS: SHA-256 hashes before and after this check match for each raw input; no raw records were edited.
- Evidence: animal-shelter-profile.json retains counts, fields, date ranges, missingness, hashes, and cross-file ID overlap.
- Method limitation: ad hoc full-file inspection, not an installed repeatable shelter profiling tool. It loads files into memory; it does not reconstruct encounters or establish source completeness. IDs in common do not prove event matches.

## Documentation migration
Updated the active plan, brief, model/ETL proposal, analysis guide, owner README, project instructions, and decision memory for the selected shelter source. Previous Airbnb validation remains labelled historical. Raw inputs, old analysis scripts, assignment requirements, and Git publication history are preserved.

## Not run / unresolved
Encounter matching; timezone interpretation; teacher acceptance of measures and hierarchies; linked sampling; shelter-specific profiling-tool validation; Fabric ingestion/SQL/ETL; exact lab DQ checks; submission and access changes. Proposed transformations and models are not execution evidence.
