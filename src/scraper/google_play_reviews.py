from google_play_scraper import Sort, reviews


def fetch_reviews(app_id: str, count: int = 500):
    """
    Fetch recent reviews from Google Play for a given app_id.
    """
    result, _ = reviews(
        app_id,
        lang="en",
        country="us",
        sort=Sort.NEWEST,
        count=count,
    )

    return result