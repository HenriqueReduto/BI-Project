# How the AI code agent works in BI Project

This folder is the working home for your Business Intelligence I project. The goal is to build and explain a Microsoft Fabric data warehouse and the processes that load and clean its data. The agent helps you turn that goal into small tasks with evidence that the results work.

## What happens when you ask for work

1. **Inspect:** The agent reads the project rules, the current plan, and the files relevant to your request. It checks what already exists and identifies missing facts or decisions.
2. **Plan:** It chooses the next coherent task and records substantial work in [PLAN.md](PLAN.md), including how to check the result.
3. **Implement:** It works on that task, following the BI assignment and your decisions. It asks you about business choices it cannot infer, such as the dataset and the questions the warehouse should answer.
4. **Validate:** It checks the result using the tools actually available and records evidence. Writing a SQL file is different from successfully running it in Fabric; the agent reports that distinction.
5. **Report:** It explains what changed, what was checked, what remains uncertain, and what comes next.

## Which files guide the agent

| File | What it does |
|---|---|
| [AGENTS.md](AGENTS.md) | Sets this project's stable rules and boundaries. |
| [PLAN.md](PLAN.md) | Tracks delivery milestones, current tasks, and completion. |
| [General workflow skill](.agents/skills/code-agent-workflow/SKILL.md) | Defines the inspect → plan → implement → validate → report cycle. |
| [BI project skill](.agents/skills/bi-project/SKILL.md) | Applies that cycle to source selection, modelling, Fabric ETL, and assignment deliveries. |
| [Requirements](docs/requirements.md) | Maps the assignment to acceptance evidence and records unresolved requirements. |
| [Saved assignment PDF](docs/source/BI%20I%20Project%20Guide%202026-2027%20v1.1.pdf) | Preserves the original source for checking assignment wording. |
| [Project decisions](memory/decisions.md) | Keeps durable decisions and their evidence available for later sessions. |

This AIREADME explains the setup to you. Detailed rules, requirements, and live task status belong in the linked files so that they have one authoritative home. The PDF describes the assignment; it does not authorize the agent to submit work, share access, or execute instructions embedded in documents.

## Where the work belongs

| Location | Contents |
|---|---|
| `data/raw/` | Original source data, preserved without editing. |
| `data/processed/` | Working transformations and derived data, with their provenance. |
| [Project brief](docs/project-brief.md) | Organization, dataset, business needs, and decisions still to make. |
| [Model and ETL specification](docs/model-and-etl.md) | Fact grain, tables, measures, hierarchies, mappings, and quality-check design. |
| `sql/` | Warehouse and staging SQL scripts as they are developed. |
| `fabric/` | Relevant Fabric artifact exports and supporting configuration, without secrets. |
| [Report template](report/report-template.md) | The assignment's eight report discussion areas. |
| [Validation checklist](validation/acceptance-checklist.md) | Checks to complete and links to actual evidence. |
| `outputs/` | Finished deliverables, such as report PDFs and presentation-ready diagrams. |

The local folders organize source files and evidence. They do not replace the required Fabric workspace, Lakehouse, databases, or pipelines.

## What you decide and review

You choose the business scenario, eligible dataset, group details, and business questions. The agent can inspect and profile supplied data, propose a model, prepare scripts and report drafts, and explain trade-offs. Teacher feedback and lab materials are needed to settle lab-specific conventions and the exact required data quality checks.

Routine work within your request can continue without repeated confirmation. The agent asks when a material decision is missing or an action needs authorization, including submissions, access changes, paid provisioning, and destructive Fabric operations. Keep credentials out of this folder and out of report screenshots.

## How to judge the result

A result is supported by evidence: a source profile, schema diagram, executed SQL checks, pipeline run results, reconciliation counts, or stored data quality logs, depending on the task. Unrun checks stay explicit. Templates and proposed designs are not proof of a working warehouse.

Use [PLAN.md](PLAN.md) for delivery progress and [docs/requirements.md](docs/requirements.md) for the detailed assignment checklist. The agent should connect business questions to the model, the transformations, and the checks that establish the result.

## Starting state

As of 20 October 2026, this setup contains the assignment guide, local skills, planning documents, and templates. No dataset, dimensional model, SQL implementation, ETL pipeline, or Fabric run has been completed. Fabric access and executable project commands have not been configured or verified. This is a dated setup snapshot; PLAN.md holds subsequent progress.

## GitHub version control

The project remote is [HenriqueReduto/BI-Project](https://github.com/HenriqueReduto/BI-Project), using the `main` branch. Raw CSV, gzip, and GeoJSON files use Git LFS; install Git LFS before cloning and run `git lfs pull` if a checkout contains pointer files. Raw inputs remain intact locally. `.gitignore` excludes local environments, caches, credentials, and temporary files.

The initial local commit is preserved on `backup/pre-lfs-2026-10-20`; this backup branch is local only and should not be pushed because it contains large ordinary Git blobs. Publication results are recorded in `validation/github-publication.md`. GitHub version control does not constitute an assignment submission or Fabric deployment.

## How to start the next session

Open this BI Project folder as the working project and ask, for example:

> Read AGENTS.md and PLAN.md. Use the local BI project and code-agent-workflow skills to help me evaluate this dataset for Delivery 1. Profile it against the requirements, identify gaps, and update the project brief with verified findings.

Supply the dataset or its location when making that request. For later work, name the next outcome you want, such as reviewing a star schema or validating an ETL run. The agent maintains this explanation when the project's operating setup materially changes.

## Extracting compressed source files

Run `python scripts/extract_csv_gz.py` from this project folder. The script uses Python's standard library to stream each `data/raw/*.csv.gz` file into `data/raw/<name>.extracted.csv`. It preserves compressed originals and existing CSVs, skips an extracted output if it already exists, and removes its partial output if extraction fails. A skipped file is not revalidated; if interrupted by a forced process stop, check for incomplete output before rerunning.

The `.extracted.csv` naming distinguishes these files from the existing `listings.csv` and `reviews.csv`. This is lossless decompression only: it does not clean, sample, or load data into Fabric. Extraction completed on 20 October 2026 for calendar, listings, and reviews. Dataset selection and profiling still require separate work.

## Raw-data exploration
Use scripts/profile_raw_data.py to profile all raw CSVs and GeoJSON features without changing the inputs. Setup and methods are documented in [docs/raw-data-analysis.md](docs/raw-data-analysis.md). Results are saved in outputs/raw-data-analysis/; inspect report.html for the searchable field explorer and report.md for the BI readiness assessment. This local Python analysis does not replace Fabric ETL or teacher validation.

