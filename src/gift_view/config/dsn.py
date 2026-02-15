import os


def build_postgres_dsn() -> str:
    return (
        f"postgresql+asyncpg://"
        f"{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}"
        f"@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}"
    )