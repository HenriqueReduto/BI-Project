# Model and ETL specification — template

## Dimensional model
Business process and fact grain: pending. Declare exactly what one fact row represents before choosing keys or measures.

| Table | Role | Grain/key | Source | Attributes or primitive measures | Business needs |
|---|---|---|---|---|---|
| Pending | Pending | Pending | Pending | Pending | Pending |

## Hierarchies
| Dimension | Ordered levels | Depth | Business purpose |
|---|---|---|---|
| Pending | Pending | Pending | Pending |
Verify ≥5 hierarchies and average depth ≥3 levels. Explain ordering and distinguish genuine analytical hierarchies from arbitrary attributes.

## ETL mapping
| Source/field | Staging target | Cleansing/transformation | DW target | Key/lookup behavior | Validation | Fabric artifact |
|---|---|---|---|---|---|---|
| Pending | Pending | Pending | Pending | Pending | Pending | Pending |

## Quality checks
Insert the exact four lab-required checks and staging LOG schema after lab materials are supplied. Additional proposed checks may cover row reconciliation, uniqueness at declared grain, referential integrity, required values, valid dates, and measure semantics; these are suggestions, not confirmed lab requirements.

## Execution and recovery
Document pipeline order, preparatory steps, rerun behavior, failure handling, logging, and successful full-run evidence. Submitted transformations must run within Fabric without external services. Delivery 2 warehouse remains empty; final delivery requires populated STG/DW/DQ tables.
