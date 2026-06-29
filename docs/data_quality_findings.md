# Data Quality Findings

## Purpose

This document summarizes lightweight data quality checks performed during the Phase I ingestion prototype.

The goal was to verify that Google Play review data can be collected, normalized, stored, and re-ingested without corrupting the database or creating duplicate records.

## Data Quality Areas Checked

### 1. Field Availability

Google Play review records provide several fields that are useful for sentiment analytics and downstream modeling:

- review text
- star rating
- review timestamp
- app version
- thumbs-up count
- lightweight user metadata

These fields support both text-based sentiment analysis and structured analysis by rating, time, and app version.

### 2. Field Normalization

Raw review fields were mapped into a consistent database-ready schema.

| Raw Field | Normalized Field |
|---|---|
| reviewId | review_id |
| userName | user_name |
| score | rating |
| content | review_text |
| at | review_date |
| thumbsUpCount | thumbs_up_count |
| reviewCreatedVersion | app_version |

This mapping makes the data easier to query and reuse across downstream analysis steps.

### 3. Duplicate Handling

The `review_id` field is used as the primary key in the `reviews` table.

The database loading step uses `INSERT OR IGNORE`, so records with review IDs that already exist in the database are skipped.

Repeated ingestion tests confirmed that duplicate records were not inserted again.

### 4. Ingestion Completeness

The monitoring layer compares:

- records fetched
- records inserted
- duplicates skipped
- duplicate rate

This helps explain whether a run inserted new records or mainly re-encountered previously stored reviews.

### 5. Run-Level Reliability

The monitoring layer records both successful and failed ingestion runs.

This makes pipeline behavior easier to audit because failures are preserved in `reports/ingestion_runs.csv` and summarized in `reports/monitoring_report.md`.

### 6. Current Findings

Current findings from the ingestion experiment:

- Repeated runs against the same app produced high duplicate rates.
- Previously inserted reviews were skipped rather than inserted again.
- Larger local test runs with batch sizes of 20, 50, and 100 completed successfully after the cleaning function issue was fixed.
- The run ID format was updated to include microseconds so rapid repeated runs do not create duplicate run IDs.

## Limitations

Current data quality checks are lightweight and mostly focused on ingestion correctness.

The project does not yet include a fully automated data quality validation script.

Additional future checks could include:

- missing review text count
- invalid rating values
- malformed timestamp detection
- review text length distribution
- app version completeness
- rating distribution monitoring
- automated validation report generation

## Summary

The current pipeline provides a reliable foundation for structured review ingestion.

The strongest validated data quality behavior is duplicate prevention across repeated runs. Future work should expand this into a more complete automated data quality validation layer.
