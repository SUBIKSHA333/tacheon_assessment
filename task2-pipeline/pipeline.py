import requests
import pandas as pd
import logging
import sys
from datetime import datetime, timedelta
from google.cloud import bigquery

# ── Logging setup ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger(__name__)

# ── Parameters (change these if needed) ────────────────────
CITY = "Chennai"
LATITUDE = 13.0827
LONGITUDE = 80.2707
DAYS_BACK = 7

BQ_PROJECT = "your-gcp-project-id"
BQ_DATASET = "marketing_weather"
BQ_TABLE   = "hourly_conditions"

# ── Step 1: Fetch data from Open-Meteo ─────────────────────
def fetch_weather(lat, lon, days_back):
    end_date   = datetime.today().date()
    start_date = end_date - timedelta(days=days_back)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,apparent_temperature,precipitation,windspeed_10m,cloudcover",
        "start_date": str(start_date),
        "end_date":   str(end_date),
        "timezone":   "Asia/Kolkata"
    }

    log.info(f"Fetching weather data for {CITY} from {start_date} to {end_date}")
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        log.info("API call successful")
        return response.json()
    except requests.exceptions.RequestException as e:
        log.error(f"API call failed: {e}")
        sys.exit(1)

# ── Step 2: Transform ───────────────────────────────────────
def transform(raw):
    log.info("Transforming raw API response")
    hourly = raw.get("hourly", {})

    df = pd.DataFrame({
        "timestamp":            hourly.get("time", []),
        "temperature_c":        hourly.get("temperature_2m", []),
        "apparent_temperature": hourly.get("apparent_temperature", []),
        "precipitation_mm":     hourly.get("precipitation", []),
        "windspeed_kmh":        hourly.get("windspeed_10m", []),
        "cloudcover_pct":       hourly.get("cloudcover", []),
    })

    # Handle nulls
    df.fillna({
        "temperature_c": 0,
        "apparent_temperature": 0,
        "precipitation_mm": 0,
        "windspeed_kmh": 0,
        "cloudcover_pct": 0
    }, inplace=True)

    # Cast types
    df["timestamp"]            = pd.to_datetime(df["timestamp"])
    df["temperature_c"]        = df["temperature_c"].astype(float)
    df["apparent_temperature"] = df["apparent_temperature"].astype(float)
    df["precipitation_mm"]     = df["precipitation_mm"].astype(float)
    df["windspeed_kmh"]        = df["windspeed_kmh"].astype(float)
    df["cloudcover_pct"]       = df["cloudcover_pct"].astype(float)

    # Derived fields
    df["feels_like_delta"] = (
        df["apparent_temperature"] - df["temperature_c"]
    ).round(2)

    df["weather_risk_score"] = (
        (df["precipitation_mm"] * 2) +
        (df["windspeed_kmh"] * 0.5) +
        (df["cloudcover_pct"] * 0.1)
    ).round(2)

    df["marketing_recommendation"] = df["weather_risk_score"].apply(
        lambda x: "Good day for outdoor campaigns"   if x < 10
             else "Consider indoor/digital campaigns" if x < 25
             else "Pause outdoor, boost digital spend"
    )

    df["city"]       = CITY
    df["ingested_at"] = datetime.utcnow().isoformat()

    log.info(f"Transformed {len(df)} rows successfully")
    return df

# ── Step 3: Load to BigQuery ────────────────────────────────
def load_to_bigquery(df):
    log.info(f"Loading data to BigQuery: {BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}")
    client = bigquery.Client(project=BQ_PROJECT)

    dataset_ref = client.dataset(BQ_DATASET)
    try:
        client.get_dataset(dataset_ref)
    except Exception:
        log.info(f"Dataset {BQ_DATASET} not found, creating it")
        client.create_dataset(bigquery.Dataset(dataset_ref))

    table_id = f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True,
    )

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    log.info(f"Loaded {len(df)} rows into {table_id}")

# ── Main ────────────────────────────────────────────────────
if __name__ == "__main__":
    raw  = fetch_weather(LATITUDE, LONGITUDE, DAYS_BACK)
    df   = transform(raw)
    load_to_bigquery(df)
    log.info("Pipeline completed successfully")