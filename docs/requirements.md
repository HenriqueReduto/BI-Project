# Assignment requirements and acceptance evidence

Source: `docs/source/BI I Project Guide 2026-2027 v1.1.pdf`, version 1.1 dated 13 October 2026. Page references below use PDF page numbers. Status of all implementation requirements: NOT YET VERIFIED.

| Requirement | Source | Evidence to collect |
|---|---|---|
| Group size 1–4; cross-class groups allowed | p.1 | Group identification |
| Source transactions: hard minimum 10k fact rows; ideal 20k–30k; history >1 year | p.2 | Source profile and date range |
| ≥5 dimensions including Date; ≥5 hierarchies averaging 3 levels; ≥1 fact table with ≥2 distinct primitive measures | FR1–2, p.4 | Star schema, hierarchy levels, grain and measure definitions |
| ≥1 warehouse fact table with ≥5k rows; real-life exceptions require teacher approval | FR2d, p.4 | Loaded row counts and any approval |
| No individual source dimension/fact dataset >30k rows; ideally 20k–30k | FR3, p.4 | Per-dataset counts and sampling rationale |
| Varied usable sources convertible to delimited files/Excel for Fabric ingestion | FR3, p.4 | Source manifest and ingestion evidence |
| Staging database separate from DW | FR4, p.4 | Fabric object identities and design |
| Fabric Data Engineering ETL; independent staging and DW processes | FR5, p.4 | Pipeline diagram and successful runs |
| Submitted ETL self-contained in Fabric; no external webservices or GenAI/LLM API calls | FR5d, p.4 | Dependency inventory and rerun evidence |
| Teaching/demo datasets such as AdventureWorks, Northwind, WorldWideImporters, Chinook, Sakila excluded | p.4 | Dataset provenance and eligibility review |
| Both Copy Data and Dataflows required, at least one of each | GC3.2, p.5 | Artifact inventory |
| Separate pipelines for distinct ETL objectives; lab naming practices | GC3.2, p.6 | Pipeline inventory and lab checklist |
| ≥4 lab-taught DQ checks; results in LOG table in staging | GC3.3, p.6 | Confirmed lab definitions and stored results |
| Useful, varied, non-trivial transformations; correct SKs/lookups and STG→DW transfer | GC3.4–5, p.6 | Mapping, execution evidence, reconciliations |
| Up to four extra original ETL developments; expectations depend on readiness feedback | GC4, p.6 | Dedicated report chapter and evidence |
| Report chapters cover all eight discussion areas | pp.7–8 | Report and chapter checklist |
| Every delivery: report PDF to Moodle plus Fabric workspace shared with all lab teachers | p.9 | User-verified submission/access records |

## Grading and delivery notes
Report 3/20; DW 8/20; ETL 8/20; original ETL 1/20 (pp.5–6). Intermediate criteria are graded once; improvements are encouraged but not regraded. Late delivery costs 0.5 points per late day cumulatively; delivery-instruction failures can cost 0.5 per affected delivery (p.9).
Use p.9's explicit 23:59 deadline wording rather than p.1's ambiguous “midnight”. Confirm course timezone; do not infer it from the computer.

## Clarifications required
- Source minimum is 10k on p.2, whereas warehouse fact minimum is 5k on p.4. These describe different stages but need teacher confirmation if sampling/filtering changes the count; conservatively target ≥10k loaded fact rows where feasible, subject to documented grain and valid data.
- Obtain the four exact lab DQ checks, LOG schema, naming conventions, and delivery identification/access rules. Do not substitute guessed checks and claim compliance.
- Confirm first-call exam date and final deadline, plus course timezone.
- Obtain teacher readiness assessment after Delivery 1; distinguish it from our provisional profiling assessment.
