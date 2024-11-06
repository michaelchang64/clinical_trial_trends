import mysql.connector
import os

# Database connection details
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'my_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'an*2hSDn5')
DB_NAME = os.getenv('DB_NAME', 'clinical_trials')

try:
    # Connect to MySQL
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()

    # Query to select the top 10 rows from transformed.combined_trials
    query = "SELECT * FROM transformed.combined_trials LIMIT 10"
    cursor.execute(query)

    # Fetch and print the results
    results = cursor.fetchall()
    for row in results:
        print(row)

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()