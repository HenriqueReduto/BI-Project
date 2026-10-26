# BI I project plan

## Objective
Design, implement, validate, and explain a Microsoft Fabric star-schema warehouse that meets the saved BI I Project Guide v1.1.

## Current state
- [x] Save the assignment guide and initialize the local operating structure.
- [x] Record requirements, deadlines, open questions, and report structure.
- [x] Add AIREADME.md explaining the project-specific agent workflow.
- [x] Historical setup: add the gzip extraction utility for the former source; it is not needed for the current shelter CSVs.
- [x] Select Austin Animal Center historical intakes/outcomes as the active source (user instruction, 26 October 2026).
- [x] Record preliminary full-file shelter profiling and proposed business/model design.
- [ ] Confirm group, final business questions, Fabric workspace, and report language.
The source is selected and a model is proposed. SQL implementation, ETL pipelines, and Fabric execution remain incomplete.

## Delivery 1 — 1 November 2026, 23:59 (guide p.9)
- [ ] Confirm group of 1–4 students and required identification/naming.
- [x] Select shelter source files and record official provenance/usage terms; teacher acceptance and original download date remain pending.
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
GitHub publication completed on 20 October 2026: `main` published to `HenriqueReduto/BI-Project`, with all 10 raw-data LFS objects uploaded (1.4 GB reported). The initial local commit is preserved on a local backup branch. Execution evidence: `validation/github-publication.md`.

Confirm dataset/business decisions before implementing a model. Resolve lab-specific conventions before asserting compliance. Keep external services out of submitted ETL. Do not submit, share, provision paid resources, or delete Fabric objects without applicable authorization.

## Active animal shelter work - 26 October 2026
- [x] Replace active Airbnb references with the selected historical Austin Animal Center datasets.
- [x] Inspect both complete CSVs for counts, IDs, duplicates, missingness, and event date coverage.
- [x] Record a proposed business brief and model/ETL approach, with unresolved requirements explicit.
- [ ] Implement reproducible shelter-specific profiling; existing Airbnb analysis tooling remains unvalidated for this source.
- [ ] Test encounter matching, timestamp semantics, and ambiguous/unmatched event handling.
- [ ] Confirm two distinct primitive measures and five defensible hierarchies with teacher guidance.
- [ ] Select a linked multi-year cohort with each source extract at most 30,000 rows; validate follow-up coverage.
- [ ] Finalize business questions and schema, then prepare Delivery 1 Lakehouse sources and chapters 1-2.

Current evidence: docs/raw-data-analysis.md, validation/animal-shelter-analysis.md, and validation/animal-shelter-profile.json. Historical Airbnb validation is retained under validation/raw-data-analysis.md and does not validate the shelter source. No current Fabric implementation is asserted.
