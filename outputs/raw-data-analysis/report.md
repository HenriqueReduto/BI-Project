# Raw data exploration and BI I readiness

Generated from all rows, without sampling. Inputs and source references are recorded in profile.json. Raw file hashes were unchanged after analysis. This is local exploratory evidence, not Fabric implementation or teacher approval.

## Verdict
**Conditionally useful, but not compliant as supplied.** Listings are within the 30k source limit; the calendar and reviews are far larger and need a documented, linked sampling/aggregation plan. Reviews provide historical events, but not booking/payment transactions or per-review prices/ratings. Calendar is a prospective availability snapshot, not actual booking history. At least two distinct primitive measures and five genuine three-level hierarchies are not yet established for one defensible fact grain. Confirm this analytical scope with the lab teacher before committing to the model.

## File inventory
| File | Rows/features | Fields | Duplicate grain extra rows |
|---|---:|---:|---:|
| calendar.extracted.csv | 9,132,343 | 5 | 0 |
| listings.csv | 25,020 | 19 | 0 |
| listings.extracted.csv | 25,020 | 90 | 0 |
| neighbourhoods.csv | 134 | 2 | 0 |
| reviews.csv | 1,950,076 | 2 | N/A |
| reviews.extracted.csv | 1,950,076 | 6 | 1,147 |
| neighbourhoods.geojson | 173 | 4 | N/A |

Gzip originals exactly match their extracted CSV payloads. Do not count them as extra sources. Summary and detailed listings/reviews represent overlapping entities/events; do not append them into a single fact table without reconciliation. Uniqueness of summary review events cannot be established from listing/date alone.

## Time and relationships
- Review dates: 2010-07-24 to 2026-09-21 (5,903 days): historical coverage exceeds one year.
- Calendar dates: 2026-09-19 to 2027-09-21 (367 days): forward-looking calendar coverage, not multi-year observed transactions. Crossing calendar years does not prove more than one year of history.
- Listing scrape dates: 2026-09-19 to 2026-09-22; geography labels indicate the Lisbon region, not just the municipality.
- Distinct listing IDs without a detailed listing: {"calendar.extracted.csv": 0, "listings.csv": 0, "reviews.csv": 0, "reviews.extracted.csv": 0}. These counts describe missing keys, not orphan row counts.
- Listing geography pairs absent from neighbourhoods.csv: 0.
- Neighbourhood labels used in multiple groups: 1. Use a compound geography key where needed.

## Numeric snapshot
| Detailed listings feature | Missing % | Mean | Median | Min | Max | IQR flags |
|---|---:|---:|---:|---:|---:|---:|

| price | 11.899 | 194.581 | 140.000 | 14.000 | 13,610.670 | 1,608 |
| accommodates | 0.000 | 3.808 | 4.000 | 1.000 | 16.000 | 1,806 |
| bedrooms | 0.192 | 1.665 | 1.000 | 0.000 | 43.000 | 1,617 |
| beds | 1.527 | 2.435 | 2.000 | 1.000 | 45.000 | 866 |
| minimum_nights | 0.216 | 3.872 | 2.000 | 1.000 | 730.000 | 1,751 |
| maximum_nights | 0.216 | 592.419 | 365.000 | 1.000 | 10,000.000 | 1 |
| number_of_reviews | 0.000 | 77.941 | 25.000 | 0.000 | 1,933.000 | 2,445 |
| reviews_per_month | 11.279 | 1.577 | 1.090 | 0.010 | 41.570 | 521 |
| availability_365 | 0.000 | 227.335 | 275.000 | 0.000 | 365.000 | 0 |
| review_scores_rating | 11.279 | 4.658 | 4.770 | 1.000 | 5.000 | 1,520 |

## Missingness and potential outliers

All-empty fields: listings.extracted.csv: neighborhood_overview, listings.extracted.csv: host_since, listings.extracted.csv: host_response_time, listings.extracted.csv: host_response_rate, listings.extracted.csv: host_acceptance_rate, listings.extracted.csv: host_thumbnail_url, listings.extracted.csv: host_neighbourhood, listings.extracted.csv: host_total_listings_count, listings.extracted.csv: neighbourhood, listings.extracted.csv: bathrooms, listings.extracted.csv: calendar_updated, listings.extracted.csv: instant_bookable.

Largest missing shares:
- listings.extracted.csv / neighborhood_overview: 100.00%.
- listings.extracted.csv / host_since: 100.00%.
- listings.extracted.csv / host_response_time: 100.00%.
- listings.extracted.csv / host_response_rate: 100.00%.
- listings.extracted.csv / host_acceptance_rate: 100.00%.
- listings.extracted.csv / host_thumbnail_url: 100.00%.
- listings.extracted.csv / host_neighbourhood: 100.00%.
- listings.extracted.csv / host_total_listings_count: 100.00%.
- listings.extracted.csv / neighbourhood: 100.00%.
- listings.extracted.csv / bathrooms: 100.00%.
- listings.extracted.csv / calendar_updated: 100.00%.
- listings.extracted.csv / instant_bookable: 100.00%.
- listings.extracted.csv / source: 88.43%.
- listings.extracted.csv / host_about: 44.47%.
- listings.extracted.csv / host_location: 30.59%.

Do not fill every blank with zero. Missing prices prevent price-based analysis; blank ratings/review dates can reflect no reviews, whereas host rates and legacy export fields need source-specific interpretation. No blank is asserted structurally inapplicable without supporting evidence. IQR flags identify unusual observations, not proven errors: expensive homes, high-volume hosts, and long-stay rules may be legitimate. Zero-IQR distributions can flag all non-modal observations. Review semantic checks, units, and business purpose before capping or dropping anything. Detailed per-field parse failures, domain flags, quartiles, distinct counts, and values appear in the HTML/CSV/JSON profiles.

## Assignment fit
| Criterion | Assessment |
|---|---|
| Source provenance / eligibility | Real public-data source, not one of the prohibited teaching databases. Preserve attribution and confirm teacher acceptance of the business scenario. Download date and exact historical URL of local files have not been supplied. |
| Source row limits | Detailed listings 25,020 meet the ≤30k cap. See inventory for all other files: calendar and review datasets exceed it. Keep originals intact and prepare derived, linked samples outside raw. |
| Minimum fact rows | Large event volumes are available, but final fact grain and valid sampled rows must still demonstrate ≥10k source facts (p.2) and ≥5k DW facts (p.4). |
| More than one year history | Reviews meet date coverage; listings are a current snapshot; calendar is prospective, not historical transactions. |
| ≥5 dimensions including Date | Candidate Date, Listing, Host, Geography, Accommodation Type can be designed. Host/type separation and keys require design; reviewer attributes are sparse. Dimensions are not yet implemented. |
| ≥5 hierarchies, average depth 3 | Not demonstrated. Date year→quarter→month→day and Geography country→municipality→neighbourhood are plausible. Additional attributes/groupings must be justified, not invented to inflate the count. |
| ≥2 distinct primitive measures | Not demonstrated at a historical transaction grain. Review count=1 is one event measure; date or IDs are not measures. Text length is derived, not a second primitive business measure. Price/capacity/stay rules exist at listing/calendar grains, not review-event prices. Estimated revenue/occupancy are modelled, not primitive transactions. |
| Varied sources and transformations | CSV plus GeoJSON enable joins, JSON/list parsing, currency/percent parsing, missing-value policy, and geography reconciliation. Summary/detailed exports are not independent business systems. |
| Fabric STG/DW, ETL and lab quality logging | Not verified by local EDA. Required Fabric pipelines, Copy Data/Dataflows, separate staging, four lab DQ checks, successful execution, and delivery access remain separate work. |

## Observed conditional missingness and rule conflicts

- review_scores_rating: 2,822 blanks; 2,822 have zero reviews and 0 have positive reviews.
- first_review: 2,822 blanks; 2,822 have zero reviews and 0 have positive reviews.
- last_review: 2,822 blanks; 2,822 have zero reviews and 0 have positive reviews.
- reviews_per_month: 2,822 blanks; 2,822 have zero reviews and 0 have positive reviews.
These observed associations support treating review-related missing values separately from general data loss; they do not justify inventing a zero score.
- Detailed reviews: 1,147 extra rows repeat review IDs, involving 443 repeated IDs. Of these, 0 are exact duplicate rows across all fields; 443 IDs have conflicting row variants. These remain in raw inputs and raw statistics; define and document a deduplication policy before fact loading.
- GeoJSON: 173 geometry features, 134 distinct geography keys; 0 listing geography pairs lack a GeoJSON key. Multiple shapes with the same key do not automatically represent additional neighbourhoods.
- calendar.extracted.csv: minimum_exceeds_maximum = 508 rows. Investigate flagged source records before choosing a correction.
- listings.extracted.csv: minimum_exceeds_maximum = 1 rows. Investigate flagged source records before choosing a correction.

Independent direct pandas calculations matched listing rows, duplicate IDs, price missing count, mean, median, and IQR outlier count.

## Recommended next step
Choose the business questions and fact grain before sampling. If using reviews, stratify across years and relevant geographic/listing groups, retain ≥10k valid events, and keep every selected event's listing/host/geography lookup. Do not randomly sample related files independently. For availability analysis, consider a separate listing-day snapshot fact, clearly labelled as prospective. Obtain teacher agreement on primitive measures and hierarchies; supplement eligible source data if needed. Do not claim real occupancy or revenue from unavailable nights.

## Methods and reproducibility
Run `python scripts/profile_raw_data.py` from the project. Tested with Python, pandas 3.0.1 and numpy 2.3.5; versions are captured in profile.json. The script reads full files in 100,000-row chunks, builds temporary on-disk exact frequency tables, and removes scratch tables after use. Exact distinct counts exclude empty fields; whitespace-only counts are separate, and NA-like text is not silently converted. Mean/median use finite parsed numeric values only; numeric IDs remain strings. Percentages are 0–100; currency symbols do not establish currency. Quantiles use linear interpolation over the full weighted frequency distribution. All statistical results are unsampled. Existing generated analysis files in the output folder are replaced on rerun.

Outputs: report.md, report.html, column_profile.csv, profile.json, room_type_summary.csv, geography_summary.csv, reviews_by_year.csv. Each field's meaning is source-informed or explicitly labelled as an unverified inference; the linked public dictionary is version 4.3 (2022) and does not document every newer field in these local exports. No external service is required to rerun this local profiler. It is not the submitted Fabric ETL.

## Sources
- Assignment: docs/source/BI I Project Guide 2026-2027 v1.1.pdf, pp.2–6 and 9.
- [Inside Airbnb data catalogue](https://insideairbnb.com/get-the-data/): file roles and licence; consulted 20 October 2026. Attribute Inside Airbnb under the listed CC BY 4.0 licence.
- [Inside Airbnb data dictionary](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit): field context, legacy version; consulted 20 October 2026. Explanations here are analytical interpretations, not a copied dictionary.
- [Inside Airbnb assumptions](https://insideairbnb.com/data-assumptions/): collection/snapshot and availability caveats; consulted 20 October 2026. Unavailable nights cannot distinguish bookings from blocks; locations are approximate; modelled estimates are not actual transaction records.
