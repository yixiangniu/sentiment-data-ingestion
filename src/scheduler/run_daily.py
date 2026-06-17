import argparse
import time

import schedule

from src.main import run_pipeline


DEFAULT_APP_ID = "com.spotify.music"
DEFAULT_REVIEW_COUNT = 50
DEFAULT_RUN_TIME = "09:00"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Schedule the Google Play review ingestion pipeline to run daily."
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
        help="Number of recent reviews to fetch per run.",
    )

    parser.add_argument(
        "--time",
        default=DEFAULT_RUN_TIME,
        help="Daily run time in HH:MM format using the local machine timezone.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    schedule.every().day.at(args.time).do(
        run_pipeline,
        app_id=args.app_id,
        review_count=args.count,
    )

    print(
        f"Scheduled daily ingestion for app_id={args.app_id}, "
        f"count={args.count}, time={args.time}"
    )

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()