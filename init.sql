
-- Switch to the clinical_trials database
USE clinical_trials;

-- Create the raw schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS raw;

-- Create the us table within the raw schema
CREATE TABLE IF NOT EXISTS raw.us (
  id INT AUTO_INCREMENT PRIMARY KEY,
  study_identifier VARCHAR(255) UNIQUE,
  study_name VARCHAR(900),
  conditions TEXT,
  sponsor VARCHAR(500),
  start_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the eu table within the raw schema
CREATE TABLE IF NOT EXISTS raw.eu (
  id INT AUTO_INCREMENT PRIMARY KEY,
  study_identifier VARCHAR(255) UNIQUE,
  study_name VARCHAR(900),
  conditions TEXT,
  sponsor VARCHAR(500),
  start_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the transformed schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS transformed;

-- Create the combined_trials table within the transformed schema
CREATE TABLE IF NOT EXISTS transformed.combined_trials (
  id INT AUTO_INCREMENT PRIMARY KEY,
  study_identifier VARCHAR(255),
  study_name VARCHAR(900),
  conditions TEXT,
  sponsor VARCHAR(500),
  start_date DATE,
  created_at TIMESTAMP,
  source VARCHAR(50)
);

-- Grant INSERT and UPDATE privileges on the `us` table
GRANT SELECT, INSERT, UPDATE, DELETE ON raw.us TO 'my_user'@'%';

-- Grant INSERT and UPDATE privileges on the `eu` table
GRANT SELECT, INSERT, UPDATE, DELETE ON raw.eu TO 'my_user'@'%';

-- Grant INSERT and UPDATE privileges on the `combined_trials` table
GRANT SELECT, INSERT, UPDATE, DELETE ON transformed.combined_trials TO 'my_user'@'%';

-- Apply the changes
FLUSH PRIVILEGES;