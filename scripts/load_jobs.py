import pandas as pd
from sqlalchemy import text
from database import get_engine

engine = get_engine()

# Read cleaned CSV
df = pd.read_csv("data/processed/jobs_clean.csv")

inserted = 0
skipped = 0

with engine.begin() as conn:

    for _, row in df.iterrows():

        # Get company_id
        company = conn.execute(
            text("""
                SELECT company_id
                FROM companies
                WHERE company_name = :company
            """),
            {"company": row["company"]}
        ).fetchone()

        company_id = company[0] if company else None

        # Get location_id
        location = conn.execute(
            text("""
                SELECT location_id
                FROM locations
                WHERE location_name = :location
            """),
            {"location": row["location"]}
        ).fetchone()

        location_id = location[0] if location else None

        # Check if job already exists
        existing_job = conn.execute(
            text("""
                SELECT job_id
                FROM jobs
                WHERE redirect_url = :redirect_url
            """),
            {"redirect_url": row["redirect_url"]}
        ).fetchone()

        if existing_job:
            skipped += 1
            continue

        # Insert new job
        conn.execute(
            text("""
                INSERT INTO jobs(
                    title,
                    company_id,
                    location_id,
                    salary_min,
                    salary_max,
                    average_salary,
                    category,
                    contract_type,
                    created,
                    redirect_url,
                    description
                )
                VALUES(
                    :title,
                    :company_id,
                    :location_id,
                    :salary_min,
                    :salary_max,
                    :average_salary,
                    :category,
                    :contract_type,
                    :created,
                    :redirect_url,
                    :description
                )
            """),
            {
                "title": row["title"],
                "company_id": company_id,
                "location_id": location_id,
                "salary_min": row["salary_min"],
                "salary_max": row["salary_max"],
                "average_salary": row["average_salary"],
                "category": row["category"],
                "contract_type": row["contract_type"],
                "created": row["created"],
                "redirect_url": row["redirect_url"],
                "description": row["description"],
            }
        )

        inserted += 1

print("=" * 40)
print(f"Jobs Inserted : {inserted}")
print(f"Jobs Skipped  : {skipped}")
print("=" * 40)