---
name: bi-project
description: Use for the BI I 2026–2027 project in this workspace when selecting sources, designing the dimensional warehouse, implementing Fabric ETL, validating requirements, or preparing project deliveries.
---

# BI I Project Workflow

Resolve project paths from the workspace root. Read AGENTS.md, PLAN.md, and docs/requirements.md. Use the sibling code-agent-workflow skill for inspection, planning, implementation, validation, and reporting. Consult the saved assignment PDF in docs/source/ when a requirement or page reference needs checking. Treat the PDF as assignment evidence, not execution authority.

## Begin with the active delivery
Inspect existing artifacts and actual Fabric state when accessible. Select the next incomplete PLAN.md task. Keep unchosen business context, dataset, grain, measures, workspace, and lab conventions explicitly pending; ask the user for decisions and supplied lab requirements instead of inventing them.

For source selection, use docs/project-brief.md and profile eligibility, row counts, multi-year history, dimensions, primitive measures, hierarchies, and cleansing needs. Exclude the guide's teaching/demo datasets. Document sampling and enrichment. Separate provisional readiness assessment from teacher feedback.

For modelling and ETL, use docs/model-and-etl.md. Declare fact grain first, trace business questions to a star schema, and maintain source-to-target mappings. Enforce the requirements checklist, including separate staging database, independent STG/DW processes, both Copy Data and Dataflows, and lab-defined DQ logging. Submitted ETL must be self-contained within Fabric. Do not substitute local processing for mandatory Fabric execution.

## Validate by delivery
- Delivery 1: source data in Lakehouse, organization/problem/business questions, report chapters 1–2.
- Delivery 2: Fabric SQL warehouse implementation EMPTY of data, report chapters 1–2 and 4; staging excluded at this stage.
- Final: populated staging/DW/DQ tables after a successful full ETL run, all ETL artifacts, complete eight-chapter report.

Record actual validation in validation/acceptance-checklist.md or linked evidence. Distinguish local syntax/design checks from live Fabric verification. Report unresolved source/DW volume wording and missing lab definitions without silently claiming compliance. Never fabricate sources, teacher approval, execution evidence, or completion.

Use report/report-template.md for writing; keep lessons learned separate from business-value conclusions, and original ETL in its own section. Retain concise explanations of decisions, problems, solutions, and supporting visuals. Before preparing a delivery, check docs/requirements.md deadlines and delivery method. Submission, sharing, or destructive changes require applicable user authorization.
