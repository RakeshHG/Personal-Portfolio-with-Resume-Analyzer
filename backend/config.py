# config.py
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
JOB_PORTAL_URLS = [
    "https://www.linkedin.com/jobs/search/?keywords=&location=Bengaluru&geoId=102350846&trk=public_jobs_jobs-search-bar_search-submit&f_TPR=r86400", # Example LinkedIn URL for Bengaluru
    "https://www.indeed.com/jobs?q=&l=Bengaluru%2C+Karnataka", # Example Indeed URL for Bengaluru
    # Add more job portal URLs as needed
]