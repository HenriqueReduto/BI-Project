# Austin Animal Center project brief

## Selected source and scope
On 26 October 2026, the user selected the animal shelter datasets by requesting replacement of the Airbnb project documents. Working project: `D:\IMS\BI Project`.

- Organization: Austin Animal Center; proposed analytical audience: shelter operations managers.
- Business process: animal intake, shelter encounters, and outcomes.
- Proposed informational problem: understand arrival demand, outcome patterns, and time in care to support staffing, adoption activity, and resource planning.
- Group members / student identifiers: pending.
- Fabric workspace and access: pending.
- Report language: pending.
- Teacher eligibility/readiness assessment: pending.

## Original sources
| Local file in data/raw | Records | Unique animal IDs | Actual event coverage |
|---|---:|---:|---|
| Austin_Animal_Center_Intakes_(10_01_2013_to_05_05_2025)_20261026.csv | 173,812 | 156,287 | 2013-10-01 to 2025-05-04 |
| Austin_Animal_Center_Outcomes_(10_01_2013_to_05_05_2025)_20261026.csv | 173,775 | 156,237 | 2013-10-01 to 2025-05-05 |

Publisher: City of Austin. Official historical catalogues: [intakes](https://data.austintexas.gov/d/wter-evkm) and [outcomes](https://data.austintexas.gov/d/9t4d-g238), consulted 26 October 2026; both state Public Domain. The filename suffix is not verified evidence of the download date. Preserve original files. Use these historical sources rather than the newer ShelterBuddy datasets with different schemas.

## Proposed business questions
| ID | Question and explanation | Decision supported | Measures | Dimensions |
|---|---|---|---|---|
| BN-01 | When does arrival demand peak, and which animal groups contribute? | Staffing and resource planning | Intake count | Intake date, animal classification, intake reason |
| BN-02 | Which groups have longer observed shelter stays? | Prioritize care and adoption support | Total stay duration, completed encounter count; derived average | Date, age band, animal classification, intake condition |
| BN-03 | How do recorded outcomes vary across animal groups and time? | Adoption and transfer planning | Outcome count; derived outcome shares | Outcome date, outcome category, animal classification, age band |
| BN-04 | How are intake condition and reason associated with duration and outcomes? | Care planning | Encounter count, duration, outcome count | Intake condition, intake reason, outcome, animal classification |
| BN-05 | How often do animals have repeat recorded intakes? | Investigate recurring demand | Intake count, distinct animals; derived repeat-intake metrics | Animal, intake date, intake reason |

These questions are proposals for the selected source. Associations do not establish causation; rates require explicit denominators and observation windows.

## Readiness and decisions still needed
Preliminary assessment: medium readiness, not teacher feedback. Source volume, history, event records, and descriptive dimensions are strong. Resolve encounter matching, five defensible hierarchies averaging three levels, and teacher acceptance of two distinct primitive measures before finalizing the model.

Full files exceed the 30,000-row limit per project source dataset. A linked multi-year extract is required; 2022-2023 contains 23,123 intake records before duplicate review and is a candidate cohort, not an approved sample. Retain relevant later outcomes, verify each extract's size, and document observation boundaries. Independently sampling the files would break links. Cohort data cannot establish total shelter occupancy.

See raw-data-analysis.md for verified findings and model-and-etl.md for the proposed design. Fabric ingestion and execution remain unverified.
