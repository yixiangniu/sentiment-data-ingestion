# sentiment-data-ingestion
Sciencia AI Internship Project - Data Ingestion &amp; Infrastructure

## Project Overview

Phase I Data Ingestion & Infrastructure project for Sciencia AI.

## Objectives

- Data acquisition
- Data structuring
- Data storage
- Automated cleaning and loading

## Repository Structure

docs/
notebooks/
src/
reports/

## Current Pipeline Status

The current implementation provides an initial repeatable ingestion pipeline for Google Play reviews.

Pipeline flow:

```text
Google Play reviews
→ fetch recent reviews
→ clean and normalize fields
→ load into SQLite database
→ prevent duplicate review inserts
→ record ingestion run metadata
```
## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the pipeline with default settings:

```bash
python -m src.main
```

Run with custom configuration:

```bash
python -m src.main --app-id com.spotify.music --count 100
```

Run the lightweight daily scheduler:

```bash
python -m src.scheduler.run_daily --app-id com.spotify.music --count 50 --time 09:00
```

Note: The scheduler is a lightweight local prototype for recurring execution. In a production setting, this could be replaced with cron, Airflow, Prefect, or a cloud scheduler.

Generated local data is stored under:

```text
data/reviews.db
```

The `data/` directory is ignored by Git because it contains generated local database files.