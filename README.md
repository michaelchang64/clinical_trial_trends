# Clinical Trials Dashboard

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

### Step 2: Access the Backend

- The backend API should be accessible at `http://localhost:8000` (or the port specified in your Docker setup).

## Frontend Setup

The frontend is built with Next.js and can be run locally.

### Step 1: Install Dependencies

1. **Navigate to the frontend directory**:

   ```bash
   cd frontend
   ```

2. **Install the required packages**:

   ```bash
   npm install
   ```

### Step 2: Run the Frontend Locally

1. **Start the development server**:

   ```bash
   npm run dev
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

- **Dockerize Frontend**: Consider dockerizing the frontend for a consistent deployment environment.
- **Security**: Implement security best practices, such as using a secrets management tool for sensitive data.