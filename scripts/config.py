import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")
COUNTRY = os.getenv("COUNTRY", "in")

BASE_URL = (
    f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1"
)