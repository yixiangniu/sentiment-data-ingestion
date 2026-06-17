def clean_reviews(raw_reviews, app_id: str):
    """
    Normalize raw Google Play review records into the database schema format.
    """
    cleaned_reviews = []

    for review in raw_reviews:
        cleaned_reviews.append({
            "review_id": review.get("reviewId"),
            "app_id": app_id,
            "user_name": review.get("userName"),
            "rating": review.get("score"),
            "review_text": review.get("content"),
            "review_date": str(review.get("at")) if review.get("at") else None,
            "thumbs_up_count": review.get("thumbsUpCount"),
            "app_version": review.get("reviewCreatedVersion"),
            "source": "Google Play",
        })

    return cleaned_reviews
