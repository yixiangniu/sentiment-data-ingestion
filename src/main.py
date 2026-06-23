import argparse
from datetime import datetime
from src.monitoring.run_logger import log_pipeline_run

from src.database.connection import initialize_database
from src.scraper.google_play_reviews import fetch_reviews
from src.cleaning.review_cleaner import clean_reviews
from src.database.loader import (
    finish_ingestion_run,
    insert_reviews,
    start_ingestion_run,
)


DEFAULT_APP_ID = "com.spotify.music"
DEFAULT_REVIEW_COUNT = 50


def parse_args():
    """
    Parse command-line arguments for the ingestion pipeline.
    """
    parser = argparse.ArgumentParser(
        description="Run the Google Play review ingestion pipeline."
    )

    parser.add_argument(
        "--app-id",
        default=DEFAULT_APP_ID,
        help="Google Play app ID to collect reviews for.",
    )

    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_REVIEW_COUNT,
        help="Number of recent reviews to fetch.",
    )

    return parser.parse_args()


def run_pipeline(app_id, review_count):
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    started_at = datetime.now()

    records_fetched = 0
    records_inserted = 0

    try:
        initialize_database()

        raw_reviews = fetch_reviews(app_id=app_id, count=review_count)
        records_fetched = len(raw_reviews)

        cleaned_reviews = clean_reviews(raw_reviews, app_id=app_id)
        records_cleaned = len(cleaned_reviews)

        records_inserted = insert_reviews(cleaned_reviews, run_id=run_id)

        ended_at = datetime.now()

        log_pipeline_run(
            run_id=run_id,
            started_at=started_at,
            ended_at=ended_at,
            app_id=app_id,
            batch_size_requested=review_count,
            records_fetched=records_fetched,
            records_inserted=records_inserted,
            status="success",
            error_message="",
        )

        print("Pipeline completed.")
        print(f"Run ID: {run_id}")
        print(f"Fetched: {records_fetched}")
        print(f"Cleaned: {records_cleaned}")
        print(f"Inserted: {records_inserted}")

    except Exception as error:
        ended_at = datetime.now()

        log_pipeline_run(
            run_id=run_id,
            started_at=started_at,
            ended_at=ended_at,
            app_id=app_id,
            batch_size_requested=review_count,
            records_fetched=records_fetched,
            records_inserted=records_inserted,
            status="failed",
            error_message=str(error),
        )

        print("Pipeline failed.")
        print(f"Run ID: {run_id}")
        print(f"Error: {error}")
        raise


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(app_id=args.app_id, review_count=args.count)
