from database.connection import initialize_database


def run_pipeline():
    print("Initializing database...")
    initialize_database()
    print("Database initialized successfully.")


if __name__ == "__main__":
    run_pipeline()
