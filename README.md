# Gift View
An analytics tool for Telegram NFT gifts trading. Each marketplace shows only its trades – Gift View collects them all into one place, enriches them with USD prices at the time of the sale, and presents the data as price charts across multiple timeframes.

## How it works
Sales are collected continuously from marketplace APIs and normalized into a unified schema. Token prices are fetched from Binance and used to compute USD value of each sale at the moment it happened. Aggregations are built directly in the database and served via a REST API to a Chart.js frontend.

The pipeline is orchestrated with Apache Airflow – marketplace ingestion runs every minute, price sync and aggregations run hourly.

## Stack
- Python – pipeline logic
- PostgreSQL – data store
- SQLAlchemy (async) + asyncpg – database access
- Apache Airflow – orchestration
- FastAPI – REST API
- Chart.js – chart building
- Docker / docker-compose – containerized deployment

## Running locally
1. Clone the repo and create a `.env` file:
```dotenv
DB_USER=gifts
DB_PASSWORD=gifts
DB_HOST=postgres
DB_PORT=5432
DB_NAME=gift_view
TONNEL_AUTH_DATA=<your_auth_data_from_tonnel>
```

2. Start everything:
```bash
docker-compose up -d --build 
```

3. Open:
- Frontend + API: http://localhost:8000
- Airflow UI: http://localhost:8080

## Notes
- Tonnel's API is protected by Cloudflare. Requests use `curl_cffi` with browser impersonation to handle TLS fingerprinting.
- Tonnel uses offset-based pagination which slows down significantly at high page numbers. This is a limitation on their end.