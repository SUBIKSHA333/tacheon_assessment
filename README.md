\# Tacheon Assessment — Data \& AI Product Engineer

\*\*Candidate:\*\* Subiksha GD

\*\*Role:\*\* Data \& AI Product Engineer

\*\*Submitted:\*\* May 2026



\---



\## Repository Structure



tacheon\_assessment/

├── task1-product-scoping/

│   ├── product-brief.md

│   └── flow-diagram.md

├── task2-pipeline/

│   ├── pipeline.py

│   ├── requirements.txt

│   ├── sql/

│   │   └── summary\_query.sql

│   └── output/

└── README.md



\---



\## Task 1: Product Scoping



\*\*The question being solved:\*\* How is our marketing performing across

channels right now, and where should we be focusing?



\*\*My approach:\*\* I scoped a single-screen internal dashboard that gives

analysts a channel health summary, period-over-period deltas, and one

prioritised recommendation in under 2 minutes — without touching any

source tool manually.



\*\*Primary user:\*\* Internal analyst / account manager (not the client in v1)



\*\*What v1 does:\*\*

\- Shows key KPI per channel with delta vs prior period

\- Classifies each channel as On Track / Needs Attention / Critical

\- Surfaces one plain-English recommendation

\- Shows data freshness timestamp



\*\*What v1 deliberately excludes:\*\*

\- Client-facing interface (validate internally first)

\- Custom date range picker (7d/30d/MTD covers 80% of needs)

\- Drill-down by campaign (channel level is enough for the question)

\- Alerts and notifications (too early before trust is established)



See task1-product-scoping/product-brief.md for full reasoning.



\---



\## Task 2: Pipeline Building



\*\*API chosen:\*\* Open-Meteo (free, no API key, rich nested JSON)



\*\*Why Open-Meteo:\*\* No authentication barrier means the pipeline runs

anywhere without secrets management. Returns deeply nested hourly arrays

ideal for demonstrating real transformation work. Weather data has genuine

marketing relevance — outdoor campaign performance correlates with

conditions.



\*\*Pipeline steps:\*\*

1\. Fetch 7 days of hourly weather data for Chennai via Open-Meteo API

2\. Flatten nested JSON into tabular format

3\. Handle nulls and cast types

4\. Compute derived fields:

&#x20;  - feels\_like\_delta (apparent temp minus actual temp)

&#x20;  - weather\_risk\_score (weighted formula from precipitation, wind, cloud)

&#x20;  - marketing\_recommendation (rule-based, 3 categories)

5\. Load 192 rows into BigQuery



\*\*BigQuery details:\*\*

\- Project: fyndai-test-project

\- Dataset: marketing\_weather

\- Table: hourly\_conditions

\- Rows loaded: 192



\---



\## How to Run



1\. Install dependencies:

pip install -r task2-pipeline/requirements.txt



2\. Set up BigQuery credentials:

set GOOGLE\_APPLICATION\_CREDENTIALS=path\\to\\your\\key.json



3\. Run the pipeline:

python task2-pipeline/pipeline.py



\---



\## SQL Summary Query



See task2-pipeline/sql/summary\_query.sql



Sample output (8 rows, one per day):

date        | city    | avg\_temp\_c | avg\_risk\_score | good\_hours

2026-05-29  | Chennai | 33.5       | 12.88          | 4

2026-05-28  | Chennai | 33.4       | 11.44          | 10

2026-05-27  | Chennai | 32.8       | 12.54          | 7

2026-05-26  | Chennai | 34.0       | 10.01          | 11

2026-05-25  | Chennai | 34.1       | 9.83           | 15

2026-05-24  | Chennai | 34.0       | 10.46          | 11

2026-05-23  | Chennai | 32.9       | 15.64          | 1

2026-05-22  | Chennai | 33.5       | 10.4           | 12



\---



\## Production Thinking



\*\*Scheduling:\*\*

Use Google Cloud Scheduler to trigger a Cloud Function daily at 6am.

The pipeline is stateless and parameterised so it runs cleanly on

any schedule without manual intervention.



\*\*Failure detection:\*\*

Two layers:

1\. Python logging writes to Cloud Logging with a log-based alert

&#x20;  firing if no success log appears within the expected window

2\. BigQuery row count check after each load — if rows inserted is 0,

&#x20;  trigger an email alert



\*\*Scaling to 10x data volume:\*\*

\- Switch from direct BigQuery inserts to batch loads via Cloud Storage

\- Write parquet files to GCS first, then load into BigQuery

\- Add pagination handling in the fetch layer

\- Partition the BigQuery table by date for query efficiency



\---



\## What I Would Do Differently With More Time



\- Add unit tests for the transformation logic

\- Build GitHub Actions CI to run tests on every push

\- Parameterise BigQuery config via a config file

\- For Task 1: conduct actual user interviews before finalising the spec

\- Record a Loom walkthrough video

