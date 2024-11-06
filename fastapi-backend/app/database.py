import mysql.connector
import os
from fastapi import HTTPException

# Load environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'my_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'an*2hSDn5')
DB_NAME = os.getenv('DB_NAME', 'clinical_trials')

def get_db_connection():
   try:
       conn = mysql.connector.connect(
           host=DB_HOST,
           user=DB_USER,
           password=DB_PASSWORD,
           database=DB_NAME
       )
       return conn
   except mysql.connector.Error as err:
       raise HTTPException(status_code=500, detail=f"Database connection error: {err}")
