# Ingestion Experiment Summary

## Purpose

This experiment evaluates whether the ingestion pipeline can support repeated and larger-volume ingestion runs while preserving duplicate handling, runtime tracking, error logging, and lightweight observability.

## Monitoring Layer

A lightweight monitoring layer was added around the existing ingestion pipeline. It writes run-level metrics to:

- `reports/ingestion_runs.csv`
- `reports/monitoring_report.md`

The monitoring layer tracks:

- Run ID
- Start and end time
- Runtime seconds
- App ID
- Requested batch size
- Records fetched
- Records inserted
- Duplicates skipped
- Duplicate rate
- Throughput records per second
- Status
- Error message

## Experiment Results

| Run ID | Batch Size | Records Fetched | Records Inserted | Duplicates Skipped | Duplicate Rate | Runtime Seconds | Throughput | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 20260623_185250 | 20 | 20 | 0 | 20 | 1.00 | 0.08 | 0.00 | failed |
| 20260623_190107 | 20 | 20 | 0 | 20 | 1.00 | 0.09 | 0.00 | success |
| 20260623_190232 | 20 | 20 | 0 | 20 | 1.00 | 0.07 | 0.00 | success |
| 20260623_190233 | 50 | 50 | 30 | 20 | 0.40 | 0.16 | 183.0463 | success |
| 20260623_190233 | 100 | 100 | 50 | 50 | 0.50 | 0.18 | 280.5033 | success |
| 20260623_190640_190833 | 20 | 20 | 0 | 20 | 1.00 | 0.09 | 0.00 | success |

## Observations

The monitoring layer successfully captured both failed and successful runs. The failed run was useful because it showed that pipeline errors are now recorded in both the CSV log and Markdown report instead of only appearing in the terminal.

After the cleaning function call was corrected, the pipeline successfully completed repeated runs with batch sizes of 20, 50, and 100 records.

Duplicate handling appears stable. Repeated runs against the same app produced high duplicate rates, and previously inserted reviews were not inserted again.

The larger local test runs completed without failure. Runtime remained low, and throughput increased when more new records were inserted.

## Engineering Notes

The monitoring code is separated into `src/monitoring/`, keeping observability separate from scraping, cleaning, and database loading.

The run ID format was updated to include microseconds so that rapid repeated runs do not create duplicate run IDs.

## Limitations

This was a lightweight local experiment, not a full production load test. The current test used one app ID only and a small number of runs.

Future tests should include multiple app IDs, longer intervals between scheduled runs, and additional data quality checks.

## Next Steps

1. Add a scheduled frequency test.
2. Test multiple app IDs.
3. Add README documentation for the monitoring outputs.
4. Add basic data quality checks.
5. Continue respecting rate limits and responsible scraping constraints.
