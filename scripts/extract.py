import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")
COUNTRY = os.getenv("COUNTRY", "in")

url = (
    f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1"
    f"?app_id={APP_ID}"
    f"&app_key={APP_KEY}"
    f"&results_per_page=50"
    f"&what=software"
)

print("Fetching job data...")

response = requests.get(url)

if response.status_code != 200:
    print("API Error:", response.status_code)
    print(response.text)
    exit()

data = response.json()

jobs = data.get("results", [])

job_list = []

for job in jobs:
    job_list.append({
        "title": job.get("title"),
        "company": job.get("company", {}).get("display_name"),
        "location": job.get("location", {}).get("display_name"),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "category": job.get("category", {}).get("label"),
        "contract_type": job.get("contract_type"),
        "created": job.get("created"),
        "redirect_url": job.get("redirect_url"),
        "description": job.get("description")
    })

df = pd.DataFrame(job_list)

os.makedirs("data/raw", exist_ok=True)

output_path = "data/raw/jobs.csv"

df.to_csv(output_path, index=False)

print(f"Successfully saved {len(df)} jobs to {output_path}")