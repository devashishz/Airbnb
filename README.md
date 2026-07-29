# 🏘️ Airbnb Data Lakehouse & Analytics Pipeline

An end-to-end modern data engineering pipeline that processes, transforms, and visualizes Airbnb listing and review data. 

This project demonstrates a senior-level **Data Lakehouse** architecture, bypassing expensive cloud data warehouses by querying an S3 Data Lake directly using **DuckDB**, transforming the data with **dbt**, and serving the analytics via a modular **Streamlit** application.

## 🏗️ Architecture & Tech Stack

*   **Data Lake (Storage):** AWS S3 (Raw CSVs)
*   **Compute Engine:** DuckDB (In-memory/local analytical processing)
*   **Transformation:** dbt (Data Build Tool)
*   **Orchestration:** Dagster (Software-Defined Assets) *(In Progress)*
*   **BI & Visualization:** Streamlit (Python)

## 🚀 Key Engineering Features

*   **Lakehouse Paradigm:** Configured DuckDB with the `httpfs` extension to query raw data directly from S3, eliminating the need for complex ingestion scripts or heavy `COPY INTO` warehouse commands.
*   **Dimensional Modeling:** Refactored raw tables into a clean `Staging -> Intermediate -> Marts` structure, utilizing a denormalized `dim_listings_w_hosts` table to optimize BI query performance.
*   **Incremental Processing:** Implemented incremental materialization on the `fct_reviews` table using the `append_new_columns` strategy to efficiently process millions of reviews without full table scans.
*   **Defensive Data Testing:** Enforced data contracts using `dbt_expectations`. Includes advanced regression testing like `expect_table_row_count_to_equal_other_table` to guarantee no fan-out occurs during complex SQL joins.
*   **Bug Resolution & Data Quality:** Identified and resolved a critical Python logic bug and a SQL timestamp granularity mismatch that incorrectly flagged standard reviews as "Full Moon" anomalies.

## 📊 Pipeline Lineage (dbt DAG)

The data flows from raw S3 S3 sources, through our staging views, into our core dimensional models and fact tables.


## 📈 Streamlit Analytics Dashboard

A modular, production-ready Streamlit application featuring cached analytical queries, read-only database connections, and dynamic NLP (WordCloud) visualizations.


