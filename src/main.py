from src.database.connection import initialize_database
from src.scraper.google_play_reviews import fetch_reviews
from src.cleaning.review_cleaner import clean_reviews
from src.database.loader import (
    finish_ingestion_run,
    insert_reviews,
    start_ingestion_run,
)


APP_ID = "com.spotify.music"
REVIEW_COUNT = 50


def run_pipeline():
    print("Initializing database...")
    initialize_database()

    run_id = start_ingestion_run(source="Google Play", app_id=APP_ID)
    print(f"Started ingestion run: {run_id}")

    try:
        print(f"Fetching {REVIEW_COUNT} reviews for app_id={APP_ID}...")
        raw_reviews = fetch_reviews(APP_ID, REVIEW_COUNT)

        print("Cleaning reviews...")
        cleaned_reviews = clean_reviews(raw_reviews, APP_ID)

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
    run_pipeline()