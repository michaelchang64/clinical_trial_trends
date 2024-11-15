# Clinical Trial Trends Dashboard

This project consists of a backend service that scrapes clinical trials data and stores it in a MySQL database, and a frontend application built with Next.js and TypeScript to visualize the data.

## Prerequisites

- **Docker**: Ensure Docker is installed and running on your machine.
- **Node.js**: Ensure Node.js (and npm) is installed for running the frontend locally.

## Backend Setup

The backend is dockerized and consists of a Python application and a MySQL database.

### Step 1: Build and Run the Docker Containers

1. **Build and start the containers**:

   ```bash
   docker-compose up --build -d
   ```

   - This command will build the Docker images and start the containers for both the Python application and the MySQL database.
   - The MySQL database will be initialized with the `init.sql` script.

2. **Verify the containers are running**:

   - Use the following command to check the status of the containers:

     ```bash
     docker-compose ps
     ```

   - You should see both the `python_app` and `mysql_db` containers running.

### Step 2: Run initial scrape run

1. Use the general scraper run command now that the container is built and loaded:

   ```bash
   docker exec -it python_app python /app/run_scrapers.py
   ```

   This script will run the scrapers and then run data ingests to update data in the MySQL database.

### Step 2: Access the Backend

- The backend API should be accessible at `http://localhost:8000` (or the port specified in your Docker setup).

Endpoints:
- **GET `/api/trials/top10`**: Retrieves the top 10 clinical trials from the database.

- **GET `/api/trials/total`**: Returns the total number of trials from ClinicalTrials.gov and EudraCT.

- **GET `/api/trials/sponsors`**: Provides a breakdown of trials by sponsor, ordered by the number of trials.

- **GET `/api/trials/conditions`**: Offers a breakdown of trials by condition, ordered by the number of occurrences.

## Frontend Setup

The frontend is built with Next.js and can be run locally.

### Step 1: Install Dependencies

1. **Navigate to the frontend directory**:

   ```bash
   cd react-frontend
   ```

2. **Install the required packages**:

   ```bash
   npm install
   ```

### Step 2: Run the Frontend Locally

1. **Start the development server**:

   ```bash
   npm start
   ```

   - This will start the Next.js development server on `http://localhost:3000`.

2. **Access the Frontend**:

   - Open your browser and navigate to `http://localhost:3000` to view the Clinical Trials Dashboard.

## Troubleshooting

- **Docker Issues**: If you encounter issues with Docker, ensure Docker is running and that you have sufficient permissions.
- **Network Errors**: If the frontend cannot connect to the backend, check CORS settings and ensure the backend is running.
- **Database Connection**: Ensure the MySQL container is running and the credentials in your application match those in `docker-compose.yml`.

## Additional Notes

- **Data Scraping**: The backend uses cron jobs to periodically scrape data and update the database. Ensure the cron jobs are correctly configured in the Dockerfile.
- **Environment Variables**: Consider using environment variables for sensitive information like database credentials.

## Future Improvements

- **Dockerize Frontend**: Will try my hand at dockerizing the frontend for a consistent deployment environment, but it for now it seems to work well enough without being dockerized.
- **More parameters to scrape**: plan is to scrape the full data more thoroughly, meaning more data visualizations
- **Filters by params**: filter by clinical trial type (completed, phase x, us, eu, university, topic, condition)
- **Topic modelling**: essentially this step would require running an embedding model across summaries of all clinical trials, chunking/storing in vectorstore db, then allowing capabilities of seeing a bunch of trials clustered by topic. also gives rise to RAG with vectorstore db
- **async scraping in eu trials site**: right now my scrapers are all synchronous, which arguably is better to prevent overloading servers (though they are probably big enough to handle this scraping given it's not a whole lot). us scraper doesn't need async because it's just downloading a csv and doing the thin
- **tracking clinical trial detail change over time**: given that I'm already scraping a whole bunch of clinical trials data, i wonder what kind of insights can be uncovered from taking diffs of clinical trials over time
  - for example, maybe i first encounter Trial A by University X 11/2/2024. Maybe over the course of 3 months, I can 
    - check for any diffs
    - run through an LLM to check if the diff is qualitatively/content-wise a significant change
    - be able to visualize the changes in a sort of timeline graphic