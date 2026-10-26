# Austin Animal Center model and ETL specification

Status: proposed design, 26 October 2026. No model or ETL has been implemented or verified in Fabric.

## Fact grain first
| Proposed table | One row represents | Candidate stored measures | Purpose |
|---|---|---|---|
| FactShelterStay | One reconstructed intake encounter, with an outcome where reliably matched | EncounterCount = 1; StayDuration for valid completed matches | Central encounter and duration analysis |
| FactIntake (optional) | One recorded intake event after documented duplicate treatment | IntakeCount = 1 | Complete intake event analysis |
| FactOutcome (optional) | One recorded outcome event after documented duplicate treatment | OutcomeCount = 1 | Complete outcome event analysis |

Animal ID identifies an animal, not an encounter. Assign warehouse event/encounter surrogate identifiers and retain source row lineage. Optional facts increase implementation scope and are not yet selected. Preserve unmatched events; an unmatched intake is not proof the animal remains in care.

## Candidate dimensions
Date (roles: intake and outcome), Animal, AnimalClassification, IntakeReason, IntakeCondition, Outcome, AgeBand, and SexReproductiveStatus. Final dimension boundaries and attributes remain pending. Age, sex/reproductive status, and potentially conflicting descriptors must reflect the event; avoid overwriting encounter history with a single latest animal value.

## Measures decision
Proposed main measures: encounter count and length of stay calculated from valid paired timestamps. Confirm that these satisfy the teacher's definition of two distinct primitive measures. Age is approximate and non-additive across animals; adoption flags and repeated count measures do not automatically establish compliance. Average duration and outcome rates are derived analytical measures with explicit denominators. Costs, treatment quantities, and weight are absent; do not invent them.

## Hierarchies
| Candidate | Ordered levels | Evidence / status |
|---|---|---|
| Date | Year > Quarter > Month > Date | Directly derivable; use unique year-month members |
| Animal classification | Animal type > standardized breed group > recorded breed | Requires a documented, unambiguous mapping; mixed breeds need a policy |
| Outcome | Outcome family > outcome type > subtype | Proposed enrichment; subtype often absent and labels may repeat under types |
| Geography | City > area > location | Conditional: free-text Found Location may not support reliable geographic levels |
| Age | Broad life stage > age band > standardized age category | Proposed mapping; nested boundaries and species-specific meanings need justification |

Only the Date path is currently straightforward. The other paths are hypotheses, not five verified hierarchies. Check meaningful parent-child relationships, missing members, unique member keys, and average depth. Additional static reference data may be needed; preserve provenance and make submitted ETL self-contained in Fabric.

## Proposed ETL mapping
| Input | Staging operation | Warehouse result | Validation |
|---|---|---|---|
| Both CSVs | Copy into separate staging database with source row lineage | Event/encounter facts | Reconcile counts and document rejected/duplicate records |
| DateTime | Parse formats and establish timezone policy | Date keys and duration inputs | Parse success, sequence checks, offset handling |
| Animal ID and ordered events | Reconstruct encounters; prevent outcome reuse | Encounter surrogate key and match status | No many-to-many expansion; review ambiguous sequences |
| Age upon Intake/Outcome | Parse numeric amount and unit; retain original | Standardized age and age-band keys | Approximation rules and valid ranges |
| Sex upon Intake/Outcome | Split sex/status and normalize literal NULL | Event-specific dimension keys | Allowed values and unknown handling |
| Breed, Color, intake/outcome categories | Documented normalization and reference mappings | Descriptive dimension keys | Mapping coverage and unmapped values |
| Date of Birth | Parse and compare where usable | Supporting age validation | Conflicts, implausible ages, missingness |

Do not join on Animal ID alone. Proposed matching orders events by animal and links an intake to a plausible subsequent outcome before the next intake, where unambiguous. Test ties, repeated intakes/outcomes, missing events, observation boundaries, and alternative sequences before accepting this rule. Retain original timestamp strings; mixed timezone representations need source interpretation before elapsed-time calculations.

## Pipelines and quality checks
Proposed flow: Lakehouse source extracts > independent STG pipeline > separate staging database and DQ LOG > independent DW pipeline > dimensions and facts. Use both Copy Data and Dataflows. Artifact names, exact four lab checks, LOG schema, rerun behavior, and recovery conventions await lab materials.

Candidate additional checks: count reconciliation, event lineage uniqueness, matching cardinality, non-negative durations, valid dates, referential integrity, required values, and category mapping coverage. These do not substitute for the four lab-prescribed checks.

## Delivery and execution
Delivery 2 requires an empty Fabric warehouse; staging is excluded at that delivery. Final delivery requires populated staging, DW and DQ tables after a successful full Fabric run. Local profiling is exploratory evidence only. Record actual run results, mapping coverage, rejected records, and recovery behavior in validation/.
