# Olist E-Commerce Data Platform: Medallion Architecture

An enterprise-grade, local Lakehouse pipeline transforming raw Brazilian e-commerce data into actionable logistics and sales intelligence. 

This project demonstrates scalable data modeling practices by processing 100k+ multi-grain records into a cohesive Medallion architecture (Bronze -> Silver -> Gold) using DuckDB as a fast, localized compute engine prior to cloud deployment.

## 🏗️ Architecture & Tech Stack
* **Compute Engine / Warehouse:** DuckDB (Local, In-Memory Lakehouse)
* **Data Transformation:** dbt (Data Build Tool)
* **Visualization Layer:** Streamlit, Altair
* **Language:** Python, SQL

## 🚀 Engineering Highlights
This project was built to solve common enterprise data engineering challenges, specifically focusing on resolving one-to-many relationships before they hit the visualization layer.

* **Grain Resolution (Avoiding Fan-Outs):** Implemented an intermediate `silver` layer to pre-aggregate line items and split payment methods (credit card, boleto, vouchers) to a strict `one-row-per-order` grain before joining to the master fact table.
* **Medallion Architecture:** 
  * `Staging (Silver):` Cleaned Portuguese column names, casted data types, and managed NULL timestamps.
  * `Intermediate (Silver):` Handled complex group-by logic and metric rollups.
  * `Mart (Gold):` Produced `fct_orders`, enriched with calculated SLAs (Days to Delivery) and GMV metrics.
* **Automated Data Quality:** Integrated `schema.yml` testing to assert primary key uniqueness and enforce strict `accepted_values` on shifting order statuses.
* **Read-Only Analytics:** The Streamlit BI layer connects to the DuckDB instance exclusively in read-only mode, mimicking production-grade concurrent access limits.

## 🛠️ How to Run Locally

Because this project uses DuckDB, you do not need any Snowflake or Azure cloud credentials to run this pipeline. Everything executes instantly on your local machine.

### 1. Environment Setup
```bash
# Install dependencies (dbt-core, dbt-duckdb, streamlit, etc.)
make install