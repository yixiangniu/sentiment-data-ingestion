import argparse

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


def run_pipeline(app_id: str, review_count: int):
    print("Initializing database...")
    initialize_database()

    run_id = start_ingestion_run(source="Google Play", app_id=app_id)
    print(f"Started ingestion run: {run_id}")

    try:
        print(f"Fetching {review_count} reviews for app_id={app_id}...")
        raw_reviews = fetch_reviews(app_id, review_count)

        print("Cleaning reviews...")
        cleaned_reviews = clean_reviews(raw_reviews, app_id)

        print("Loading reviews into database...")
        inserted_count = insert_reviews(cleaned_reviews, run_id=run_id)

        finish_ingestion_run(
            run_id=run_id,
            status="success",
            records_fetched=len(raw_reviews),
            records_inserted=inserted_count,
        )

        print("Pipeline completed.")
        print(f"Run ID: {run_id}")
        print(f"Fetched: {len(raw_reviews)}")
        print(f"Cleaned: {len(cleaned_reviews)}")
        print(f"Inserted: {inserted_count}")

    except Exception as error:
        finish_ingestion_run(
            run_id=run_id,
            status="failed",
            records_fetched=0,
            records_inserted=0,
            error_message=str(error),
        )
        print("Pipeline failed.")
        print(f"Run ID: {run_id}")
        print(f"Error: {error}")
        raise


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(app_id=args.app_id, review_count=args.count)