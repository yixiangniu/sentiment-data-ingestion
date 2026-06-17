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