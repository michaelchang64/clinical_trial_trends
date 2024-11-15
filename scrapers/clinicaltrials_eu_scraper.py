import json
import os
import logging
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open('scrapers/config.json', 'r') as config_file:
    config = json.load(config_file)

MAX_PAGES = config.get('ct_eu_max_pages', 3)
USER_AGENT = config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36')
RETRIES = config.get('retries', 3)

def scrape_eu_clinical_trials(timestamp, retries=RETRIES):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=USER_AGENT)

        data = []

        for page_number in range(1, MAX_PAGES + 1):
            url = f"https://www.clinicaltrialsregister.eu/ctr-search/search?query=&page={page_number}"
            retries = 3
            success = False

            while retries > 0 and not success:
                try:
                    logging.debug(f"Attempting to navigate to {url}")
                    page.goto(url, wait_until='networkidle', timeout=60000)
                    success = True
                    logging.info(f"Successfully connected to {url}")
                except Exception as e:
                    retries -= 1
                    logging.warning(f"Failed to connect to {url}. Retries left: {retries}. Error: {e}")
                    if retries == 0:
                        logging.error(f"Failed to connect to {url} after multiple attempts.")
                        return

            results = page.query_selector_all('//table[@class="result"]')
            for result in results[:20]:
                row_data = {}
                for key, label in {
                    'EudraCT Number': 'EudraCT Number:',
                    'Sponsor Name': 'Sponsor Name:',
                    'Full Title': 'Full Title:',
                    'Medical Condition': 'Medical condition:',
                    'Start Date': 'Start Date'
                }.items():
                    element = result.query_selector(f'td:has(span.label:has-text("{label}"))')
                    if element:
                        text = element.inner_text().split(':', 1)[-1].strip()
                        row_data[key] = text
                    else:
                        row_data[key] = None

                # Extract diseases from the meddra table
                meddra_table = result.query_selector('//table[@class="meddra"]')
                if meddra_table:
                    disease_terms = meddra_table.query_selector_all('tr td:nth-child(4)')
                    diseases = [term.inner_text().strip() for term in disease_terms][1:]
                    if diseases:
                        row_data['Diseases'] = '|'.join(diseases)
                    else:
                        row_data['Diseases'] = None
                else:
                    row_data['Diseases'] = None

                data.append(row_data)
            logging.debug(f"Extracted data for page {page_number}")

        browser.close()

        # Create DataFrame and save to CSV with timestamped directory
        df = pd.DataFrame(data)
        directory = f'raw_csvs/{timestamp}'
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, 'ct_eu_latest.csv')
        df.to_csv(file_path, index=False)
        logging.info(f"Data saved to {file_path}")

if __name__ == "__main__":
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    scrape_eu_clinical_trials(timestamp)
