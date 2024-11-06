import json
import re
import os
import time
import logging
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open('scrapers/config.json', 'r') as config_file:
    config = json.load(config_file)

MAX_PAGES = config.get('ct_us_max_pages', 3)
USER_AGENT = config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36')
DOWNLOAD_ALL = config.get('download_all', False)
RETRIES = config.get('retries', 3)

def scrape_clinical_trials(timestamp, retries=RETRIES):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=USER_AGENT)

        url = "https://clinicaltrials.gov/search?limit=100&page=1"
        success = False

        while retries > 0 and not success:
            try:
                logging.debug(f"Attempting to navigate to {url}")
                page.goto(url, wait_until='networkidle', timeout=60000)  # Wait for the page to fully load
                success = True
                logging.info(f"Successfully connected to {url}")
            except Exception as e:
                retries -= 1
                logging.warning(f"Failed to connect to {url}. Retries left: {retries}. Error: {e}")
                if retries == 0:
                    logging.error(f"Failed to connect to {url} after multiple attempts.")
                    return

        # Check for checkboxes
        checkboxes = page.query_selector_all('//div[@class="headline"]//label[@class="usa-checkbox__label"]')
        num_checkboxes = len(checkboxes)

        if num_checkboxes > 100:
            logging.warning(f"More than 100 checkboxes found on page 1, skipping...")
            return

        # Click all checkboxes
        for checkbox in checkboxes:
            checkbox.click()

        # Verify the number of checked items
        clear_selection_button = page.query_selector('//div[@class="action-bar-items"]//span[@class="text-button"]')
        if clear_selection_button:
            clear_text = clear_selection_button.inner_text()
            checked_count = int(re.search(r'\d+', clear_text).group())
            if checked_count != num_checkboxes:
                logging.warning(f"Checkbox count mismatch on page 1, skipping...")
                return

        # Click the download CSV button
        download_button = page.query_selector('//button[@title="Download"]')
        if download_button:
            download_button.click()
            page.wait_for_selector('//div[@aria-controls="download"]')  # Wait for the modal to appear

            # Choose download option based on config
            if DOWNLOAD_ALL:
                download_all_option = page.query_selector('//div[@aria-controls="download"]//label[@for="download-results-all"]')
                download_all_option.click()
            else:
                download_top_option = page.query_selector('//div[@aria-controls="download"]//label[@for="download-results-top"]')
                download_top_option.click()
                # Set the number of top results to download
                top_results_input = page.query_selector('//div[@aria-controls="download"]//div[@class="option last-option"]/input[@type="number"]')
                top_results_input.fill(str(MAX_PAGES * 100))

            # First deselect all fields
            deselect_button_xpath = '//div[@aria-controls="download"]//button[@data-ga-label="De-select all"]'
            deselect_button = page.query_selector(deselect_button_xpath)
            if deselect_button:
                deselect_button.click()

            # Select the required data fields
            data_fields = [
                "Study Title", "NCT Number", "Conditions", "Sponsor",
                "Study URL", "Start Date", "Primary Completion Date",
                "Completion Date", "First Posted", "Results First Posted",
                "Last Update Posted"
            ]
            for field in data_fields:
                field_checkbox = page.query_selector(f'//div[@aria-controls="download"]//label[text()="{field}"]')
                if field_checkbox:
                    field_checkbox.click()

            # Download the CSV
            download_button = page.query_selector('//div[@aria-controls="download"]//button[normalize-space(text())="Download"]')
            if download_button:
                with page.expect_download() as download_info:
                    download_button.click()
                    download = download_info.value
                    directory = f'raw_csvs/{timestamp}'
                    os.makedirs(directory, exist_ok=True)
                    file_path = os.path.join(directory, 'ct_us_latest.csv')
                    download.save_as(file_path)
                    logging.info(f"Downloaded CSV to {file_path}")

        browser.close()

if __name__ == "__main__":
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    scrape_clinical_trials(timestamp)