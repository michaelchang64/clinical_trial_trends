import mysql.connector
from fastapi import APIRouter, HTTPException
from app.database import get_db_connection

router = APIRouter(
   prefix="/api/trials",
   tags=["trials"]
)

@router.get("/top10")
async def get_top_10_trials():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM transformed.combined_trials LIMIT 10"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"trials": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   
@router.get("/total")
async def get_total_trials():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                SUM(CASE WHEN source = 'ClinicalTrials.gov' THEN 1 ELSE 0 END) AS clinicalTrialsGov,
                SUM(CASE WHEN source = 'EudraCT' THEN 1 ELSE 0 END) AS eudraCT
            FROM transformed.combined_trials
        """
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sponsors")
async def get_sponsors_breakdown():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT sponsor AS name, COUNT(*) AS value
            FROM transformed.combined_trials
            GROUP BY sponsor
            ORDER BY value DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"sponsors": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conditions")
async def get_conditions_breakdown():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT conditions AS name, COUNT(*) AS value
            FROM transformed.combined_trials
            GROUP BY conditions
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"conditions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
