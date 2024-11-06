# Clinical Trial Trends

This project contains scrapers for extracting data from clinical trial registries. The scrapers are designed to run on a schedule and are containerized using Docker.

## Installation and Setup

### Prerequisites

- Docker
- Python 3.10
- Playwright

### Project Structure

```
clinical_trial_trends/
│
├── raw_csvs/
├── scrapers/
│   ├── clinicaltrials_eu_scraper.py
│   └── clinicaltrials_gov_scraper.py
│   └── config.json
├── Dockerfile
├── requirements.txt
└── crontab
```

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/michaelchang64/clinical_trial_trends.git
   cd clinical_trial_trends
   ```

2. **Install Dependencies**

   Ensure you have the required Python packages listed in `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Playwright**

   Install Playwright and its dependencies:

   ```bash
   playwright install
   ```

4. **Build the Docker Image**

   Build the Docker image using the provided `Dockerfile`.

   ```bash
   docker build -t clinical-trial-trends .
   ```

5. **Run the Docker Container**

   Run the container to start the scrapers on a schedule.

   ```bash
   docker run --rm clinical-trial-trends
   ```

### Configuration

- **config.json**: Configure the number of pages to scrape and other settings.

### Scheduling

The scrapers are set to run every 12 hours using cron jobs within the Docker container. Logs are stored in `/var/log/cron.log`.