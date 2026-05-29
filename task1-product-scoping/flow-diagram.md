\# System Flow: Marketing Performance Tool



\## Data Flow



\[Google Ads] ──┐

\[Meta Ads]  ──┼──► \[Python Pipeline] ──► \[BigQuery] ──► \[Dashboard] ──► \[Analyst]

\[Email]     ──┘



\## Pipeline Steps



1\. FETCH   → Pull data from each channel API

2\. FLATTEN → Convert nested JSON to tabular rows

3\. ENRICH  → Compute deltas, status, recommendation

4\. LOAD    → Write to BigQuery marketing\_weather dataset

5\. DISPLAY → Dashboard reads from BigQuery and renders



\## Dashboard Interaction



Analyst opens tool

&#x20;   → Selects brand + time window (7d / 30d / MTD)

&#x20;   → Sees channel health summary

&#x20;   → Reads one recommendation

&#x20;   → Takes action in under 2 minutes



\## What is NOT in v1



\- No client access

\- No drill-down by campaign

\- No alerts or notifications

\- No multi-brand comparison

