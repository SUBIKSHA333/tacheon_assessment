\# Tacheon Assessment — Data \& AI Product Engineer

\*\*Candidate:\*\* Subiksha GD

\*\*Role:\*\* Data \& AI Product Engineer

\*\*Submitted:\*\* May 2026



\## Repository Structure



tacheon\_assessment/

├── task1-product-scoping/

│   └── product-brief.md

├── task2-pipeline/

│   ├── pipeline.py

│   ├── requirements.txt

│   ├── sql/

│   │   └── summary\_query.sql

│   └── output/

└── README.md



\## Task 1: Product Scoping



I scoped a single-screen internal dashboard that gives analysts a channel health summary, period-over-period deltas, and one prioritised recommendation in under 2 minutes without touching any source tool.



See task1-product-scoping/product-brief.md for the full brief.



\## Task 2: Pipeline Building



API chosen: Open-Meteo (free, no API key required)



The pipeline fetches hourly weather data, flattens nested JSON, computes derived fields, and loads into BigQuery.



\## How to Run



pip install -r task2-pipeline/requirements.txt

python task2-pipeline/pipeline.py



\## Production Thinking



Scheduling: Google Cloud Scheduler triggers the pipeline daily.

Failure detection: Log-based alerts in Cloud Logging.

Scaling: Switch to GCS batch loads and partition BigQuery table by date.

