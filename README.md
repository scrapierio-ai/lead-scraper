# Lead Scraper API

This is a FastAPI-based REST API designed to query and retrieve leads from a PostgreSQL database. It is fully compatible with Railway and bypasses common `libpq` system dependencies by utilizing `asyncpg`.

## Getting Started

When deployed to Railway, or run locally, the API listens for HTTP requests to fetch lead data.

### Environment Variables

If you want to configure your database connection without hardcoding credentials in `lead_scraper.py`, you can set the following environment variables (which you can also add in your Railway dashboard):

- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`

## How to use the Tool

Once the API is running (you will get a domain like `https://your-railway-app-url.up.railway.app`), you can interact with it via HTTP requests. 

FastAPI additionally hosts interactive API docs which you can view by visiting the `/docs` route (e.g. `https://your-railway-app-url.up.railway.app/docs`).

---

### Fetching Leads

**Endpoint:** `POST /leads`  
**Description:** Retrieves lead records based on optional filters and specific columns.

#### 1. Retrieve all columns matching a filter
You can pass filters in the JSON body. The keys are the column names, and the values are partial or full matches (it uses `ILIKE` for case-insensitive searching).

```bash
curl -X POST "https://your-railway-app-url.up.railway.app/leads" \
     -H "Content-Type: application/json" \
     -d '{
           "filters": {
               "person_name": "John"
           }
         }'
```

#### 2. Retrieve specific columns
If you only want certain columns (like their name and email) to save bandwidth, you can define them in the `columns` array.

```bash
curl -X POST "https://your-railway-app-url.up.railway.app/leads" \
     -H "Content-Type: application/json" \
     -d '{
           "columns": [
               "person_name", 
               "person_email"
           ],
           "filters": {
               "person_name": "John"
           }
         }'
```

#### 3. Retrieve all data (No filters)
If you just want to grab the default chunk of records without any specific filtering, send an empty JSON object:

```bash
curl -X POST "https://your-railway-app-url.up.railway.app/leads" \
     -H "Content-Type: application/json" \
     -d '{}'
```

### Health Check

**Endpoint:** `GET /health`  
Use this endpoint to verify that your service is running smoothly on Railway.

```bash
curl -X GET "https://your-railway-app-url.up.railway.app/health"
```
