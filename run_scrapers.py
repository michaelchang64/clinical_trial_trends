from datetime import datetime
from scrapers.clinicaltrials_eu_scraper import scrape_eu_clinical_trials
from scrapers.clinicaltrials_us_scraper import scrape_clinical_trials
from db_scripts.data_ingestion import data_ingest

def main():
    # Generate a common timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Run both scrapers with the same timestamp
    scrape_eu_clinical_trials(timestamp)
    scrape_clinical_trials(timestamp)
    data_ingest()

if __name__ == "__main__":
    main()