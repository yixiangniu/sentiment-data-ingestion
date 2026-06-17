from src.database.connection import get_connection


def insert_reviews(cleaned_reviews):
    """
    Insert cleaned review records into the reviews table.

    Duplicate reviews are ignored based on review_id.
    """
    inserted_count = 0

    sql = """
    INSERT OR IGNORE INTO reviews (
        review_id,
        app_id,
        user_name,
        rating,
        review_text,
        review_date,
        thumbs_up_count,
        app_version,
        source
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        for review in cleaned_reviews:
            cursor.execute(sql, (
                review["review_id"],
                review["app_id"],
                review["user_name"],
                review["rating"],
                review["review_text"],
                review["review_date"],
                review["thumbs_up_count"],
                review["app_version"],
                review["source"],
            ))

            if cursor.rowcount == 1:
                inserted_count += 1

        conn.commit()

    return inserted_count
