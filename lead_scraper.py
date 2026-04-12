import psycopg2
from psycopg2.extras import RealDictCursor

# ------------------------ CONFIG ------------------------
DB_USER = "myuser"
DB_PASSWORD = "mypassword"
DB_HOST = "157.230.173.229"
DB_PORT = 5432
DB_NAME = "apollo"

# Filters you want to apply (column_name: value)
FILTERS = {
    "person_name": "John"
}

# Columns to retrieve (empty list = all columns)
COLUMNS = []  # e.g., ["person_name", "person_email", "person_location_city"]

# Chunk size (rows per fetch)
CHUNK_SIZE = 100_000
# --------------------------------------------------------

def fetch_leads(filters: dict = None, columns: list = None, chunksize: int = CHUNK_SIZE):
    # Columns to select
    select_sql = "*" if not columns else ", ".join(columns)

    # Build WHERE clause
    where_clauses = []
    values = []
    if filters:
        for col, val in filters.items():
            where_clauses.append(f"{col} ILIKE %s")
            values.append(f"%{val}%")  # case-insensitive partial match

    where_sql = ""
    if where_clauses:
        where_sql = " WHERE " + " AND ".join(where_clauses)

    query = f"SELECT {select_sql} FROM leads{where_sql}"

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    results = []

    try:
        with conn.cursor(name="leads_cursor", cursor_factory=RealDictCursor) as cursor:
            # server-side cursor for memory efficiency
            cursor.itersize = chunksize
            cursor.execute(query, tuple(values) if values else None)

            for row in cursor:
                results.append(dict(row))  # convert each row to dict
    finally:
        conn.close()

    return results

# ------------------------ RUN ------------------------
if __name__ == "__main__":
    data = fetch_leads(filters=FILTERS, columns=COLUMNS)
    print(f"Retrieved {len(data)} rows")
    if data:
        # Print first 5 rows
        for row in data[:5]:
            print(row)
