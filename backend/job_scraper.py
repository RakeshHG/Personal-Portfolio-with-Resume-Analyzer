# backend/job_scraper.py
import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_linkedin_jobs(url):
    """Scrapes job listings from a LinkedIn Jobs search URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        job_listings = []
        jobs = soup.find_all('li', class_='job-card-list__item')
        for job in jobs:
            title_element = job.find('h3', class_='base-search-card__title')
            company_element = job.find('h4', class_='base-search-card__subtitle')
            location_element = job.find('span', class_='job-search-card__location')
            link_element = job.find('a', class_='base-card__full-link')

            if title_element and company_element and location_element and link_element:
                job_listings.append({
                    'title': title_element.text.strip(),
                    'company': company_element.text.strip(),
                    'location': location_element.text.strip(),
                    'url': link_element['href']
                })
        return job_listings
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return []

# Add similar scraping functions for Indeed, Naukri, etc. as needed.
# You'll need to inspect the HTML structure of each website to extract the relevant information.

def scrape_jobs(urls):
    """Scrapes jobs from a list of URLs with a delay to be polite."""
    all_jobs = []
    for url in urls:
        print(f"Scraping jobs from: {url}")
        if "linkedin.com" in url:
            jobs = scrape_linkedin_jobs(url)
        # elif "indeed.com" in url:
        #     jobs = scrape_indeed_jobs(url)
        # elif "naukri.com" in url:
        #     jobs = scrape_naukri_jobs(url)
        else:
            print(f"No specific scraper implemented for: {url}")
            jobs = []
        all_jobs.extend(jobs)
        time.sleep(random.randint(3, 7)) # Be respectful to the websites
    return all_jobs

if __name__ == '__main__':
    from backend.config import JOB_PORTAL_URLS
    scraped_jobs = scrape_jobs(JOB_PORTAL_URLS)
    print(f"Found {len(scraped_jobs)} job listings.")
    # You can save these jobs to a file or database here
    # For now, let's just print a few
    for job in scraped_jobs[:5]:
        print(job)