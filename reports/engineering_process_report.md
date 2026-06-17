# Engineering Process Report

## 1. Project Overview

This project implements Phase I of a sentiment analytics data pipeline: automated data ingestion and structured storage for user-generated review text.

The current implementation focuses on building a repeatable ingestion layer that can collect Google Play review data, normalize the raw fields, store the results in a relational database, and preserve execution traces for future review and debugging.

## 2. Data Source Decision

Google Play reviews were selected as the initial data source because they provide public user-generated text, star ratings, timestamps, app version information, and lightweight user metadata relevant to sentiment analysis.

This source is also suitable for a first ingestion prototype because the review records have a consistent structure and can be mapped cleanly into a relational schema.

## 3. Pipeline Architecture

Current pipeline flow:

```text
Google Play reviews
→ fetch recent reviews
→ clean and normalize fields
→ load into SQLite database
→ prevent duplicate review inserts
→ record ingestion run metadata
```

The code is organized into modular components:

```text
src/
  scraper/
    google_play_reviews.py
  cleaning/
    review_cleaner.py
  database/
    connection.py
    loader.py
    schema.sql
  scheduler/
    run_daily.py
  main.py
```

## 4. Database Design

The current SQLite schema includes three main tables:

- `apps`
- `reviews`
- `ingestion_runs`

The `reviews` table stores normalized review records. The `review_id` field is used as the primary key, which prevents duplicate inserts when the pipeline is run repeatedly.

The `ingestion_runs` table records each pipeline execution, including the source, app ID, status, number of records fetched, number of records inserted, and any error message. This makes the ingestion process easier to audit and debug.

## 5. Cleaning and Loading Rules

Raw Google Play review fields are normalized into a consistent database-ready structure.

Current field mapping includes:

- `reviewId` → `review_id`
- `userName` → `user_name`
- `score` → `rating`
- `content` → `review_text`
- `at` → `review_date`
- `thumbsUpCount` → `thumbs_up_count`
- `reviewCreatedVersion` → `app_version`

The loading step uses `INSERT OR IGNORE` so duplicate review IDs are skipped rather than inserted again.

## 6. Verification and Data Quality Checks

Verification queries are documented in:

```text
docs/verification_queries.md
```

The current verification checks include:

- total review count
- reviews by rating
- duplicate review detection
- latest ingestion runs
- latest review timestamp

A key validation result was that running the same ingestion command twice caused the second run to insert zero duplicate records, confirming that the `review_id` primary key and duplicate prevention logic are working.

## 7. Automation Strategy

The pipeline can be run manually with:

```bash
python -m src.main
```

It also supports command-line configuration:

```bash
python -m src.main --app-id com.spotify.music --count 100
```

A lightweight local scheduler has been added:

```bash
python -m src.scheduler.run_daily --app-id com.spotify.music --count 50 --time 09:00
```

This scheduler is a local prototype for recurring ingestion. In a production environment, it could be replaced by cron, Airflow, Prefect, or a cloud scheduler.

## 8. Challenges Encountered

Several engineering issues came up during implementation:

- A module naming conflict occurred when the local file name matched the `google_play_scraper` package name.
- Python import paths required using `python -m src.main` instead of `python src/main.py`.
- Generated local database files needed to be excluded with `.gitignore`.
- Notebook exploration logic had to be separated into reusable source modules.
- The pipeline needed duplicate prevention so repeated ingestion runs would not corrupt the database.

## 9. Key Design Decisions

Key design decisions include:

- SQLite was selected for local prototyping because it is lightweight and easy to run in a remote development environment.
- The codebase was split into scraper, cleaning, database, and scheduler modules to improve maintainability.
- `review_id` was used as the primary key to support repeatable ingestion.
- `ingestion_runs` was added to preserve an execution trace for each run.
- `requirements.txt` was added to improve reproducibility.
- `.gitignore` was updated to avoid committing generated data and environment files.

## 10. Current Limitations

Current limitations include:

- The pipeline currently targets one app per run.
- The scheduler is a lightweight local prototype and is not yet production orchestration.
- Logging is currently based on print statements rather than a structured logging framework.
- Verification queries are documented but not yet automated as a script.
- The database is SQLite, which is appropriate for prototyping but may need PostgreSQL or another production database later.

## 11. Future Work

Recommended next steps:

- Add support for multiple app IDs in one run.
- Add structured logging.
- Add automated verification scripts.
- Add configuration files for app IDs, country, language, and review count.
- Add stronger error handling and retry logic.
- Evaluate whether PostgreSQL is needed for larger-scale ingestion.
- Expand the report with screenshots, sample outputs, and final observations.