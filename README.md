# Animal Welfare and Shelter Operations

Business Intelligence I | 2026-2027 | Austin Animal Center

**How could data improve animal welfare and shelter operations?**

This project explores how animal intake and outcome records can help a shelter understand demand, identify long waits, investigate repeat visits, and improve operational planning. The intended result is a Microsoft Fabric star-schema data warehouse, supported by staging, ETL processes, data-quality logging, and a project report.

Data can identify where attention may be needed. These records alone do not measure animal wellbeing or demonstrate that an intervention improved it.

## Data sources

The original CSVs are stored in `data/raw/` and must remain unchanged.

| Dataset | Records | Distinct animals | Observed event coverage |
|---|---:|---:|---|
| Austin Animal Center Intakes | 173,812 | 156,287 | 1 October 2013 - 4 May 2025 |
| Austin Animal Center Outcomes | 173,775 | 156,237 | 1 October 2013 - 5 May 2025 |

Each file contains 12 columns. Intakes describe arrivals, intake reasons, conditions, locations, and animal characteristics. Outcomes describe recorded departures, outcome categories, and animal characteristics at outcome.

Publisher: City of Austin. Historical catalogues: [Intakes](https://data.austintexas.gov/d/wter-evkm) and [Outcomes](https://data.austintexas.gov/d/9t4d-g238). Both catalogues state Public Domain. See [SOURCES.md](SOURCES.md) for the source manifest and download-date limitations.

## Business questions

- When does intake demand peak, and which animal groups contribute most?
- Which groups have longer observed shelter stays?
- How do adoption, transfer, and return-to-owner outcomes vary across groups and time?
- How are intake reason and condition associated with duration and outcomes?
- How often do animals have repeat recorded intakes?

These questions could support staffing, foster outreach, reunion activity, and staff-led case reviews. Proposed actions require current operational data and follow-up evaluation before claiming an improvement.

## Choosing the project period

The analysis window is **not finalized**. The following raw counts show that 2023-2025 fits the assignment's 30,000-row limit per source dataset:

| Year | Intake records | Outcome records |
|---|---:|---:|
| 2023 | 11,227 | 11,151 |
| 2024 | 11,817 | 11,822 |
| 2025, partial through early May | 3,748 | 3,609 |
| **2023-2025 total** | **26,792** | **26,582** |

Counts use each event's own date, before duplicate treatment or encounter matching. They are not counts of linked shelter stays.

The latest recommendation is to use **2023-2024 intakes as the main cohort**, retaining relevant outcomes through the available 2025 cutoff as follow-up. This provides two complete intake years. There are 23,044 raw intakes dated 2023-2024; the linked outcome extract must still be constructed and counted.

If 2025 intakes are included, report them as a partial year. Compare equivalent calendar periods rather than full-year totals, and retain unresolved encounters separately. Animals admitted shortly before the cutoff may have no observed outcome yet; excluding them could make stays appear shorter.

Earlier documents also describe a 2022-2023 candidate cohort. Neither proposal has been generated as a final extract or approved by the teacher.

## Proposed warehouse and ETL approach

Declare the fact grain before finalizing tables:

| Proposed fact | One row represents | Purpose |
|---|---|---|
| Shelter encounter | One reconstructed intake encounter, with an outcome where reliably matched | Time-in-care and encounter analysis |
| Intake event, optional | One validated recorded arrival | Intake demand |
| Outcome event, optional | One validated recorded outcome | Departure classifications |

Candidate dimensions include Date, Animal, Animal Classification, Intake Reason, Intake Condition, Outcome, Age Band, and Sex/Reproductive Status. Final table boundaries, keys, measures, and hierarchies remain proposals.

**Animal ID identifies an animal, not a visit.** Animals can enter the shelter more than once. Joining the files only on Animal ID can multiply records and pair unrelated visits. Match encounters chronologically, retain source lineage, and flag ambiguous or unmatched events. Age and reproductive status must reflect the relevant event.

The proposed Fabric flow is:

`Lakehouse sources -> separate staging database and quality LOG -> warehouse dimensions and facts`

Staging and warehouse loads require independent pipelines. The assignment requires both Copy Data and Dataflows, plus the four lab-defined data-quality checks. Local exploration does not replace the required Fabric implementation.

## Data-quality and interpretation rules

- Preserve full raw files; put documented cohort extracts and transformations in `data/processed/`.
- Investigate the 36 intake and 26 outcome exact duplicate excess rows before final treatment.
- Handle missing names as optional descriptors; use stable identifiers for linkage.
- Distinguish blank outcome types and subtypes from recorded categories and inapplicable values.
- Standardize age units with documented approximation rules; investigate negative or unparsed ages.
- Resolve mixed timestamp representations before accepting elapsed-time calculations.
- Keep unmatched and ambiguous encounters visible; an unmatched intake is not proof of current shelter occupancy.
- Interpret long stays alongside outcomes and case mix. Faster departure alone is not evidence of better welfare.

Final fact volume depends on matching, selection, and exclusions. Enough raw rows do not automatically establish a compliant warehouse.

## Folder guide

| Location | Purpose |
|---|---|
| `data/raw/` | Original shelter CSVs |
| `data/processed/` | Derived extracts and transformations |
| `docs/` | Project brief, requirements, analysis notes, and model/ETL specification |
| `docs/source/` | Saved assignment guide |
| `scripts/` | Local utilities; verify their source-specific compatibility before use |
| `sql/` | Staging and warehouse SQL as it is developed |
| `fabric/` | Fabric artifact exports and supporting configuration |
| `report/` | Report structure and source drafts |
| `validation/` | Actual checks, profiles, and execution evidence |
| `outputs/` | Finished project deliverables |
| `memory/` | Dated project decisions |

## Start here

- [PLAN.md](PLAN.md): delivery milestones and current tasks.
- [Project brief](docs/project-brief.md): business questions and selected source.
- [Requirements](docs/requirements.md): assignment criteria and unresolved clarifications.
- [Model and ETL](docs/model-and-etl.md): proposed design and matching considerations.
- [Raw-data analysis](docs/raw-data-analysis.md): verified preliminary source findings.
- [Validation checklist](validation/acceptance-checklist.md): evidence still required.
- [AIREADME.md](AIREADME.md): how the AI-assisted workflow operates.

Some utilities and validation records belong to the former Airbnb exploration. They are historical, not evidence that the shelter files have passed those checks. In particular, `scripts/profile_raw_data.py` has not been validated as a shelter-specific profiling tool.

## Current status and next steps

As of 26 October 2026, the shelter source is selected and preliminary full-file inspection and a proposed model are documented. A separate initial-analysis PDF has also been produced in the current Codex chat's outputs; it has not been copied into this project's `outputs/` folder. No Fabric implementation or successful ETL run is asserted.

Next steps:

1. Finalize the business questions and analysis period.
2. Validate encounter matching, timestamp interpretation, and unresolved cases.
3. Confirm two acceptable primitive measures and five meaningful hierarchies averaging three levels.
4. Generate linked source extracts and verify row limits and observation boundaries.
5. Load the selected sources into Fabric Lakehouse and prepare report chapters 1-2.
6. Implement and validate the warehouse and ETL according to the delivery plan.

Group details, report language, Fabric access, teacher feedback, and exact lab conventions remain pending. Keep credentials out of project files and reports.

The assignment guide lists Delivery 1 on **1 November 2026 at 23:59** and Delivery 2 on **29 November 2026 at 23:59**. Delivery 2 requires an empty warehouse. The final delivery date depends on the first-call exam date; confirm that date and the course timezone. See PLAN.md and docs/requirements.md for the authoritative delivery checklist.
