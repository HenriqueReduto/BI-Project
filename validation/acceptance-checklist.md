# Validation evidence checklist

All unchecked items remain unverified. For each actual check, record date, Fabric artifact or local command, expected result, observed result, and evidence path. Never mark a template as a successful run.

- [ ] Source eligibility/provenance, per-dataset row counts, date history >1 year.
- [ ] Business questions trace to the model.
- [ ] Star schema, ≥5 dimensions including Date, ≥5 hierarchies averaging ≥3 levels.
- [ ] Declared fact grain and ≥2 distinct primitive measures.
- [ ] Fact row-count requirements checked against source and DW separately.
- [ ] Delivery 2 schema exists in Fabric and warehouse tables are empty.
- [ ] Staging is a separate database from DW.
- [ ] Independent STG/DW ETL; Copy Data and Dataflow both used.
- [ ] Exact four lab DQ checks implemented and logged in staging.
- [ ] Grain/key integrity, relationships, lookups, dates, measures, and reconciliations checked.
- [ ] Final full ETL executed successfully with STG/DW/DQ data loaded.
- [ ] ETL reruns self-contained in Fabric with no external service dependency.
- [ ] Original ETL work documented separately, up to four developments.
- [ ] Required report chapters and PDF prepared for current delivery.
- [ ] Naming, student identification, workspace teacher access, and Moodle submission checked by user.
