from src.database.connection import initialize_database
from src.scraper.google_play_reviews import fetch_reviews
from src.cleaning.review_cleaner import clean_reviews
from src.database.loader import insert_reviews


APP_ID = "com.spotify.music"
REVIEW_COUNT = 50


def run_pipeline():
    print("Initializing database...")
    initialize_database()

    print(f"Fetching {REVIEW_COUNT} reviews for app_id={APP_ID}...")
    raw_reviews = fetch_reviews(APP_ID, REVIEW_COUNT)

    print("Cleaning reviews...")
    cleaned_reviews = clean_reviews(raw_reviews, APP_ID)

    print("Loading reviews into database...")
    inserted_count = insert_reviews(cleaned_reviews)

    print("Pipeline completed.")
    print(f"Fetched: {len(raw_reviews)}")
    print(f"Cleaned: {len(cleaned_reviews)}")
    print(f"Inserted: {inserted_count}")


if __name__ == "__main__":
    run_pipeline()