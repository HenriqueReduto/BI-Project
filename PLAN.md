# BI I project plan

## Objective
Design, implement, validate, and explain a Microsoft Fabric star-schema warehouse that meets the saved BI I Project Guide v1.1.

## Current state
- [x] Save the assignment guide and initialize the local operating structure.
- [x] Record requirements, deadlines, open questions, and report structure.
- [x] Add AIREADME.md explaining the project-specific agent workflow.
- [x] Add scripts/extract_csv_gz.py and extract the three supplied gzip CSVs into data/raw with distinct .extracted.csv names, preserving originals.
- [ ] Identify group, business scenario, source dataset, and Fabric workspace.
No dataset, model, SQL implementation, ETL pipeline, or Fabric execution is complete.

## Delivery 1 — 1 November 2026, 23:59 (guide p.9)
- [ ] Confirm group of 1–4 students and required identification/naming.
- [ ] Select eligible source data; preserve provenance and usage terms.
- [ ] Profile rows, dates, attributes, measures, cleansing needs, and candidate hierarchies.
- [ ] Define organization/problem and explained business needs/questions.
- [ ] Ingest source data into Fabric Lakehouse; sample where necessary.
- [ ] Complete report chapters 1–2 and source documentation.
- [ ] Validate against docs/requirements.md; prepare report PDF and workspace access for all lab teachers.
Evidence: source manifest/profile, Lakehouse load results, chapters 1–2, submission/access checklist.

## Delivery 2 — 29 November 2026, 23:59 (guide p.9)
- [ ] Incorporate feedback and confirm fact grain and measure semantics.
- [ ] Design star schema with ≥5 dimensions including Date, ≥5 hierarchies averaging 3 levels, and ≥2 distinct primitive measures.
- [ ] Implement the EMPTY warehouse with Fabric SQL scripts; staging is excluded from this delivery.
- [ ] Document keys/relationships and business-question coverage; create schema diagram.
- [ ] Add report chapter 4 to chapters 1–2; verify schema and empty-table evidence.
Evidence: diagram, model specification, SQL, Fabric schema checks, zero-row checks, report PDF/access checklist.

## Delivery 3 — date unresolved
Due at 23:59 on the last Saturday before the BI I first-call exam. Confirm the exam date and course timezone before calculating a date.
- [ ] Build staging as a separate database from the warehouse.
- [ ] Build independent staging and warehouse ETL pipelines, using both ≥1 Copy Data and ≥1 Dataflow.
- [ ] Confirm and implement the FOUR lab-taught data quality checks; store results in a staging LOG table.
- [ ] Implement justified cleansing, surrogate keys/lookups, and complete staging-to-DW loads.
- [ ] Document up to four original ETL developments and dataset readiness feedback.
- [ ] Execute full ETL in Fabric; retain loaded staging, warehouse, and quality results.
- [ ] Validate volumes, date coverage, grain, relationships, measures, quality logging, and self-contained rerun.
- [ ] Complete all eight report chapters and prepare final delivery evidence.
Evidence: execution logs, reconciliations, DQ LOG results, screenshots/diagrams, final report and access checklist.

## Checkpoints and exclusions
GitHub publication requested on 20 October 2026: prepare Git LFS for raw data, preserve the initial local commit on a backup branch, publish `main` to `HenriqueReduto/BI-Project`, and verify the remote commit and LFS objects. Execution evidence: `validation/github-publication.md`.

Confirm dataset/business decisions before implementing a model. Resolve lab-specific conventions before asserting compliance. Keep external services out of submitted ETL. Do not submit, share, provision paid resources, or delete Fabric objects without applicable authorization.

## Active local data exploration
- [x] Inspect raw schemas and source documentation; preserve raw inputs.
- [x] Profile all fields and full row populations; verify keys, date coverage, and raw hashes.
- [x] Save reproducible code and a concise readiness report; record limitations and next decisions.

Local EDA evidence: outputs/raw-data-analysis/report.md and profile.json. Seven logical files / 128 fields were profiled; gzip payloads matched extracted files and raw hashes were unchanged. Candidate source is Inside Airbnb Lisbon-region data; final business scenario, fact grain, primitive measures, hierarchy design, linked sampling, and teacher acceptance remain pending. No Fabric implementation is asserted.

Local EDA evidence: outputs/raw-data-analysis/report.md and profile.json. Seven logical files / 128 fields were profiled; gzip payloads matched extracted files and raw hashes were unchanged. Candidate source is Inside Airbnb Lisbon-region data; final business scenario, fact grain, primitive measures, hierarchy design, linked sampling, and teacher acceptance remain pending. No Fabric implementation is asserted.

