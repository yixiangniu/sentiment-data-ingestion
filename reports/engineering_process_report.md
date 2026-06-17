# Engineering Process Report

## 1. Project Overview

This project implements the first phase of a sentiment analytics data pipeline: automated data ingestion and structured storage for user-generated review text.

## 2. Data Source Decision

Google Play reviews were selected as the initial data source because they provide public user-generated text, ratings, timestamps, and app metadata relevant to sentiment analysis.

## 3. Pipeline Architecture

Current pipeline flow:

```text
Google Play reviews
→ fetch recent reviews
→ clean and normalize fields
→ load into SQLite database
→ prevent duplicate inserts
→ record ingestion run metadata