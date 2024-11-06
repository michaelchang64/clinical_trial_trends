# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Install cron and other necessary packages
RUN apt-get update && apt-get install -y \
    cron \
    libglib2.0-0 \
    libnss3 \
    libglib2.0-dev \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libdrm2 \
    libxkbcommon0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    wget \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its dependencies
RUN playwright install

# Copy the rest of your application code into the container
COPY . .
COPY db_scripts /app/db_scripts

# Add the crontab file
COPY crontab /etc/cron.d/scraper-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/scraper-cron

# Apply the cron job
RUN crontab /etc/cron.d/scraper-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log