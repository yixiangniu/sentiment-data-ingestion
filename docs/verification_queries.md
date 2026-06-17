# Verification Queries

This document records SQL queries used to verify the health and completeness of the Google Play review ingestion pipeline.

## 1. Total Review Count

```sql
SELECT COUNT(*) AS total_reviews
FROM reviews;