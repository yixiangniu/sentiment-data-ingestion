import csv
from pathlib import Path
from datetime import datetime


MONITORING_DIR = Path("reports")
MONITORING_CSV = MONITORING_DIR / "ingestion_runs.csv"
MONITORING_MD = MONITORING_DIR / "monitoring_report.md"


FIELDNAMES = [
    "run_id",
    "started_at",
    "ended_at",
    "runtime_seconds",
    "app_id",
    "batch_size_requested",
    "records_fetched",
    "records_inserted",
    "duplicates_skipped",
    "duplicate_rate",
    "throughput_records_per_second",
    "status",
    "error_message",
]


def safe_divide(numerator, denominator):
    if denominator == 0:
        return 0
    return numerator / denominator


def append_run_log(run_metrics):
    MONITORING_DIR.mkdir(parents=True, exist_ok=True)

    file_exists = MONITORING_CSV.exists()

    with MONITORING_CSV.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)

        if not file_exists:
            writer.writeheader()

        writer.writerow(run_metrics)


def read_run_logs():
    if not MONITORING_CSV.exists():
        return []

    with MONITORING_CSV.open("r", newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def generate_monitoring_report():
    runs = read_run_logs()

    if not runs:
        MONITORING_MD.write_text(
            "# Ingestion Monitoring Report\n\nNo ingestion runs have been logged yet.\n",
            encoding="utf-8",
        )
        return

    latest = runs[-1]

    total_runs = len(runs)
    successful_runs = sum(1 for run in runs if run["status"] == "success")
    failed_runs = sum(1 for run in runs if run["status"] == "failed")

    avg_runtime = safe_divide(
        sum(float(run["runtime_seconds"]) for run in runs),
        total_runs,
    )

    avg_duplicate_rate = safe_divide(
        sum(float(run["duplicate_rate"]) for run in runs),
        total_runs,
    )

    avg_throughput = safe_divide(
        sum(float(run["throughput_records_per_second"]) for run in runs),
        total_runs,
    )

    report = f"""# Ingestion Monitoring Report

## Latest Run Summary

- Run ID: {latest["run_id"]}
- Status: {latest["status"]}
- App ID: {latest["app_id"]}
- Started at: {latest["started_at"]}
- Ended at: {latest["ended_at"]}
- Runtime seconds: {latest["runtime_seconds"]}
- Batch size requested: {latest["batch_size_requested"]}
- Records fetched: {latest["records_fetched"]}
- Records inserted: {latest["records_inserted"]}
- Duplicates skipped: {latest["duplicates_skipped"]}
- Duplicate rate: {latest["duplicate_rate"]}
- Throughput records per second: {latest["throughput_records_per_second"]}
- Error message: {latest["error_message"]}

## Historical Summary

- Total runs: {total_runs}
- Successful runs: {successful_runs}
- Failed runs: {failed_runs}
- Average runtime seconds: {avg_runtime:.2f}
- Average duplicate rate: {avg_duplicate_rate:.2f}
- Average throughput records per second: {avg_throughput:.2f}

## Notes

This report is generated automatically from `reports/ingestion_runs.csv`.
It provides lightweight observability for repeated ingestion runs without requiring a full dashboard.
"""

    MONITORING_MD.write_text(report, encoding="utf-8")


def build_run_metrics(
    run_id,
    started_at,
    ended_at,
    app_id,
    batch_size_requested,
    records_fetched,
    records_inserted,
    status,
    error_message="",
):
    runtime_seconds = (ended_at - started_at).total_seconds()
    duplicates_skipped = max(records_fetched - records_inserted, 0)

    duplicate_rate = safe_divide(duplicates_skipped, records_fetched)
    throughput = safe_divide(records_inserted, runtime_seconds)

    return {
        "run_id": run_id,
        "started_at": started_at.isoformat(timespec="seconds"),
        "ended_at": ended_at.isoformat(timespec="seconds"),
        "runtime_seconds": round(runtime_seconds, 2),
        "app_id": app_id,
        "batch_size_requested": batch_size_requested,
        "records_fetched": records_fetched,
        "records_inserted": records_inserted,
        "duplicates_skipped": duplicates_skipped,
        "duplicate_rate": round(duplicate_rate, 4),
        "throughput_records_per_second": round(throughput, 4),
        "status": status,
        "error_message": error_message,
    }


def log_pipeline_run(
    run_id,
    started_at,
    ended_at,
    app_id,
    batch_size_requested,
    records_fetched,
    records_inserted,
    status,
    error_message="",
):
    run_metrics = build_run_metrics(
        run_id=run_id,
        started_at=started_at,
        ended_at=ended_at,
        app_id=app_id,
        batch_size_requested=batch_size_requested,
        records_fetched=records_fetched,
        records_inserted=records_inserted,
        status=status,
        error_message=error_message,
    )

    append_run_log(run_metrics)
    generate_monitoring_report()

    return run_metrics