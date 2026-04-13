from fastapi import FastAPI, Body, HTTPException
import uvicorn
import asyncpg
import os
from typing import List, Dict, Optional

# ------------------------ CONFIG ------------------------
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword")
DB_HOST = os.getenv("DB_HOST", "157.230.173.229")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "apollo")

CHUNK_SIZE = 100_000
# --------------------------------------------------------

app = FastAPI(title="Lead Scraper API", description="API to fetch leads from PostgreSQL database.")

async def get_db_connection():
    return await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT
    )

@app.post("/leads")
async def fetch_leads(
    filters: Optional[Dict[str, str]] = Body(None, description="Filters to apply containing column names and values for partial matching."),
    columns: Optional[List[str]] = Body(None, description="List of columns to retrieve. Leave empty to retrieve all columns.")
):
    """
    Retrieve leads from the database based on optional filters.
    """
    try:
        select_sql = "*" if not columns else ", ".join(columns)
        
        where_clauses = []
        values = []
        
        if filters:
            for idx, (col, val) in enumerate(filters.items(), start=1):
                where_clauses.append(f"{col} ILIKE ${idx}")
                values.append(f"%{val}%")

        where_sql = ""
        if where_clauses:
            where_sql = " WHERE " + " AND ".join(where_clauses)
            
        query = f"SELECT {select_sql} FROM leads{where_sql} LIMIT {CHUNK_SIZE}"
        
        conn = await get_db_connection()
        try:
            # Using asyncpg, which doesn't require libpq system library!
            if values:
                records = await conn.fetch(query, *values)
            else:
                records = await conn.fetch(query)
                
            # Convert asyncpg.Record to dict
            results = [dict(record) for record in records]
            return {"status": "success", "count": len(results), "data": results}
        finally:
            await conn.close()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("lead_scraper:app", host="0.0.0.0", port=port)
