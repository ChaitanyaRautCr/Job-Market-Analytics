import os
import pandas as pd

# File paths
RAW_FILE = "data/raw/jobs.csv"
PROCESSED_DIR = "data/processed"
PROCESSED_FILE = os.path.join(PROCESSED_DIR, "jobs_clean.csv")

# Create processed directory
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Load raw data
df = pd.read_csv(RAW_FILE)

print(f"Raw Records: {len(df)}")

# Remove duplicates
df.drop_duplicates(inplace=True)

# Fill text columns only
text_columns = [
    "title",
    "company",
    "location",
    "category",
    "contract_type",
    "description",
    "redirect_url",
    "created"
]

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].fillna("Not Available")

# Convert salary columns to numeric
salary_columns = ["salary_min", "salary_max"]

for col in salary_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(0)

# Create average salary
df["average_salary"] = (df["salary_min"] + df["salary_max"]) / 2

# Remove rows without job title
df = df[df["title"] != "Not Available"]

# Save cleaned data
df.to_csv(PROCESSED_FILE, index=False)

print(f"Clean Records: {len(df)}")
print(f"Saved to: {PROCESSED_FILE}")