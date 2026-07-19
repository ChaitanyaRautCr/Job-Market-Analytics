import pandas as pd
from sqlalchemy import text
from database import get_engine

engine = get_engine()

df = pd.read_csv("data/processed/jobs_clean.csv")

companies = (
    df["company"]
    .dropna()
    .drop_duplicates()
    .sort_values()
)

with engine.begin() as conn:

    inserted = 0

    for company in companies:

        result = conn.execute(
            text("""
                SELECT company_id
                FROM companies
                WHERE company_name = :company
            """),
            {"company": company}
        ).fetchone()

        if result is None:

            conn.execute(
                text("""
                    INSERT INTO companies(company_name)
                    VALUES(:company)
                """),
                {"company": company}
            )

            inserted += 1

print(f"{inserted} companies inserted.")