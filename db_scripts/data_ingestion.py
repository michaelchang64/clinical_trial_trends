import mysql.connector
import csv
import os
from datetime import datetime

# Database connection details
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'my_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'an*2hSDn5')
DB_NAME = os.getenv('DB_NAME', 'clinical_trials')

# Connect to MySQL
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = conn.cursor()

# Function to parse and validate date
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m').date().replace(day=1)
        except ValueError:
            return None

# Function to find the most recent directory
def get_latest_directory(base_path='raw_csvs'):
    directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    directories.sort(reverse=True)
    return os.path.join(base_path, directories[0]) if directories else None

# Function to insert data into the `us` table
def insert_us_data(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            start_date = parse_date(row['Start Date'])
            if start_date is None:
                continue
            cursor.execute('''
                INSERT INTO raw.us (study_identifier, study_name, conditions, sponsor, start_date)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                study_name=VALUES(study_name), conditions=VALUES(conditions), sponsor=VALUES(sponsor), start_date=VALUES(start_date)
            ''', (
                row['NCT Number'], row['Study Title'], row['Conditions'], row['Sponsor'], start_date
            ))
    conn.commit()

# Function to insert data into the `eu` table
def insert_eu_data(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            start_date = parse_date(row['Start Date'])
            if start_date is None:
                continue
            cursor.execute('''
                INSERT INTO raw.eu (study_identifier, study_name, conditions, sponsor, start_date)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                study_name=VALUES(study_name), conditions=VALUES(conditions), sponsor=VALUES(sponsor), start_date=VALUES(start_date)
            ''', (
                row['EudraCT Number'], row['Full Title'], row['Diseases'] if row['Diseases'] else row['Medical Condition'], row['Sponsor Name'], start_date
            ))
    conn.commit()

# Function to update the combined_trials and conditions tables
def update_combined_trials_and_conditions():
    # Clear the existing data in combined_trials and conditions
    cursor.execute('DELETE FROM transformed.conditions')
    cursor.execute('DELETE FROM transformed.combined_trials')

    # Insert data from raw.us into transformed.combined_trials
    cursor.execute('''
        INSERT INTO transformed.combined_trials (study_identifier, study_name, sponsor, start_date, created_at, source)
        SELECT study_identifier, study_name, sponsor, start_date, created_at, 'ClinicalTrials.gov' AS source
        FROM raw.us
    ''')

    # Insert data from raw.eu into transformed.combined_trials
    cursor.execute('''
        INSERT INTO transformed.combined_trials (study_identifier, study_name, sponsor, start_date, created_at, source)
        SELECT study_identifier, study_name, sponsor, start_date, created_at, 'EudraCT' AS source
        FROM raw.eu
    ''')

    # Fetch all trials from combined_trials
    cursor.execute('SELECT id, study_identifier FROM transformed.combined_trials')
    trials = cursor.fetchall()

    # Insert conditions into the transformed.conditions table
    for trial_id, study_identifier in trials:
        # Fetch conditions from raw.us
        cursor.execute('SELECT conditions FROM raw.us WHERE study_identifier = %s', (study_identifier,))
        us_conditions = cursor.fetchone()
        if us_conditions and us_conditions[0]:
            for condition in us_conditions[0].split('|'):
                cursor.execute('''
                    INSERT INTO transformed.conditions (trial_id, condition_name)
                    VALUES (%s, %s)
                ''', (trial_id, condition.strip()))

        # Fetch conditions from raw.eu
        cursor.execute('SELECT conditions FROM raw.eu WHERE study_identifier = %s', (study_identifier,))
        eu_conditions = cursor.fetchone()
        if eu_conditions and eu_conditions[0]:
            for condition in eu_conditions[0].split('|'):
                cursor.execute('''
                    INSERT INTO transformed.conditions (trial_id, condition_name)
                    VALUES (%s, %s)
                ''', (trial_id, condition.strip()))

    conn.commit()

# Main function to ingest data
def data_ingest():
    latest_directory = get_latest_directory()
    if not latest_directory:
        print("No data directories found.")
        return

    us_file_path = os.path.join(latest_directory, 'ct_us_latest.csv')
    eu_file_path = os.path.join(latest_directory, 'ct_eu_latest.csv')

    if os.path.exists(us_file_path):
        insert_us_data(us_file_path)
    else:
        print(f"File not found: {us_file_path}")

    if os.path.exists(eu_file_path):
        insert_eu_data(eu_file_path)
    else:
        print(f"File not found: {eu_file_path}")

    # Update the combined_trials and conditions tables after data ingestion
    update_combined_trials_and_conditions()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    data_ingest()