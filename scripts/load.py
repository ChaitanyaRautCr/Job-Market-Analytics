import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Database connection
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Read cleaned data
df = pd.read_csv("data/processed/jobs_clean.csv")

print(f"Loading {len(df)} records...")

# Load data into PostgreSQL
df.to_sql(
    "jobs",
    engine,
    if_exists="append",
    index=False
)

print("Data loaded successfully!")