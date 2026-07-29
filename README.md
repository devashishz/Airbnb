# Airbnb Data Pipeline: DuckDB + dbt + Streamlit

An end-to-end local data engineering pipeline that transforms raw Airbnb data into analytical dashboards using a modern Lakehouse architecture.

## 🏗️ Architecture & Tech Stack
* **Data Warehouse:** DuckDB (Local, In-Memory Lakehouse)
* **Data Transformation:** dbt (Data Build Tool)
* **Visualization:** Streamlit
* **Language:** Python, SQL

## 🚀 Project Overview
This project simulates a real-world data engineering workflow. It ingestes raw Airbnb host, listing, and review data, standardizes it through a staging layer, and builds dimensional models (marts). 

**Key Features:**
* Migrated from a cloud-based Snowflake warehouse to a lightweight, local DuckDB architecture for instant reproducibility.
* Implemented incremental materialization for fact tables (e.g., `fct_reviews`) to optimize processing times.
* Integrated custom dbt data tests (`dbt_expectations`) to enforce strict data quality rules (e.g., handling nulls, verifying minimum night stays, ensuring consistent created dates).
* Investigated and resolved a data anomaly where reviews spiked during Full Moon events using a custom Streamlit dashboard.

## 🛠️ How to Run Locally

Because this project uses DuckDB, you do not need any cloud credentials to run this pipeline. Everything executes instantly on your local machine!
