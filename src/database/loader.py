from datetime import datetime

from src.database.connection import get_connection


def start_ingestion_run(source: str, app_id: str) -> int:
    """
    Create a new ingestion run record and return its run_id.
    """
    sql = """
    INSERT INTO ingestion_runs (
        source,
        app_id,
        status
    )
    VALUES (?, ?, ?)
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (source, app_id, "running"))
        conn.commit()
        return cursor.lastrowid


def finish_ingestion_run(
    run_id: int,
    status: str,
    records_fetched: int,
    records_inserted: int,
    error_message: str = None,
):
    """
    Update an ingestion run record after the pipeline finishes.
    """
    sql = """
    UPDATE ingestion_runs
    SET
        finished_at = ?,
        status = ?,
        records_fetched = ?,
        records_inserted = ?,
        error_message = ?
    WHERE run_id = ?
    """

    with get_connection() as conn:
        conn.execute(
            sql,
            (
                datetime.utcnow().isoformat(),
                status,
                records_fetched,
                records_inserted,
                error_message,
                run_id,
            ),
        )
        conn.commit()


def insert_reviews(cleaned_reviews, run_id: int = None):
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
        source,
        run_id
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                run_id,
            ))

            if cursor.rowcount == 1:
                inserted_count += 1

        conn.commit()

    return inserted_count