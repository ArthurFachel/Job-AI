import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
from datetime import datetime
from urllib.parse import urljoin

BASE_URL = "https://www.coolstartupjobs.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
MAX_PAGES = 50
DELAY = (1, 3)

def get_page(url):
    """Fetch a page with error handling"""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_job_cards(soup):
    """Extract job cards using the specific div structure"""
    return soup.find_all('div', class_='border dark:bg-gray-800 text-lg rounded-xl flex p-4 mt-2 mb-4 max-w-lg w-full items-center justify-between')

def scrape_job_card(card, company_name, card_number, total_cards):
    """Scrape job information from a single job card"""
    job = {
        'company': company_name,
        'title': '',
        'location': '',
        'job_url': '',
        'posted_date': '',
        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    try:
        print(f"\rProcessing card {card_number}/{total_cards}", end="", flush=True)
        
        title_elem = card.find('div')
        job['title'] = title_elem.get_text(strip=True) if title_elem else ''
        
        link_elem = card.find('a', href=True)
        if link_elem:
            job['job_url'] = link_elem['href']
        
        location_elem = card.select_one('.text-gray-400, .text-gray-500, .location')
        job['location'] = location_elem.get_text(strip=True) if location_elem else ''
        
    except Exception as e:
        print(f"\nError extracting job data: {e}")
    
    return job

def scrape_company_page(url):
    """Scrape all jobs from a company page"""
    soup = get_page(url)
    if not soup:
        return []
    
    company_name = url.split('/')[-1].replace('-', ' ').title()
    
    # Find all job cards on the page
    job_cards = extract_job_cards(soup)
    total_cards = len(job_cards)
    jobs = []
    
    if total_cards > 0:
        print(f"\nFound {total_cards} job cards at {company_name}")
    
    for i, card in enumerate(job_cards, 1):
        job_data = scrape_job_card(card, company_name, i, total_cards)
        if job_data['title']:  
            jobs.append(job_data)
    
    if total_cards > 0:
        print(f"\nCompleted {total_cards} cards at {company_name}")
    
    return jobs

def scrape_all_jobs():
    """Main scraping function with proper pagination"""
    all_jobs = []
    total_companies = 0
    total_jobs = 0
    
    for page in range(1, MAX_PAGES + 1):
        url = f"{BASE_URL}/startups?p={page}"
        print(f"\nScraping page {page}: {url}")
        
        soup = get_page(url)
        if not soup:
            continue
        
        company_links = []
        for card in soup.select('div.flex.flex-col'):
            link = card.find('a', href=True)
            if link and link['href'].startswith('/startups/'):
                company_links.append(urljoin(BASE_URL, link['href']))
        
        if not company_links:
            print("No company links found - ending pagination")
            break
        
        print(f"Found {len(company_links)} companies on page {page}")
        total_companies += len(company_links)
        
        for company_url in company_links:
            print(f"\nProcessing company: {company_url}")
            jobs = scrape_company_page(company_url)
            all_jobs.extend(jobs)
            total_jobs += len(jobs)
            time.sleep(random.uniform(*DELAY))
    
    print(f"\nScraping complete. Processed {total_companies} companies and {total_jobs} jobs total.")
    return all_jobs

def save_to_csv(jobs, filename=None):
    """Save jobs data to CSV"""
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'coolstartupjobs_{timestamp}.csv'
    
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)
    print(f"Saved {len(jobs)} jobs to {filename}")
    return filename

def main():
    print("Starting CoolStartupJobs.com scraper...")
    start_time = time.time()
    jobs = scrape_all_jobs()
    
    if jobs:
        saved_file = save_to_csv(jobs)
        print(f"Scraping complete. Data saved to {saved_file}")
    else:
        print("No jobs were scraped.")
    
    elapsed = time.time() - start_time
    print(f"Total scraping time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()