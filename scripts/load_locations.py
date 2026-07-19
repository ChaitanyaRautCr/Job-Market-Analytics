import pandas as pd
from sqlalchemy import text
from database import get_engine

engine = get_engine()

df = pd.read_csv("data/processed/jobs_clean.csv")

locations = (
    df["location"]
    .dropna()
    .drop_duplicates()
    .sort_values()
)

with engine.begin() as conn:

    inserted = 0

    for location in locations:

        result = conn.execute(
            text("""
                SELECT location_id
                FROM locations
                WHERE location_name = :location
            """),
            {"location": location}
        ).fetchone()

        if result is None:

            conn.execute(
                text("""
                    INSERT INTO locations(location_name)
                    VALUES(:location)
                """),
                {"location": location}
            )

            inserted += 1

print(f"{inserted} locations inserted.")