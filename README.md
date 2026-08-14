# 📦 Olist E-Commerce Lakehouse 

An end-to-end, local data engineering and analytics platform built on the Brazilian E-Commerce public dataset. This project processes raw transactional records through a Medallion Architecture using **DuckDB** and **dbt**, serving interactive logistics and revenue insights via **Streamlit** and **Altair**.

---

### Key Engineering Highlights
* **Medallion Architecture:**
  * `Staging (Silver)`: Materialized as views; cleans Portuguese naming conventions, casts timestamp datatypes, and normalizes schema structures.
  * `Intermediate (Silver)`: Materialized as ephemeral CTEs; resolves complex multi-grain relationships (e.g., aggregating line items and payment methods to a strict 1-row-per-order grain) to avoid join fan-outs.
  * `Mart (Gold)`: Materialized as persistent analytical tables (`fct_orders`) containing SLA metrics (days to delivery) and financial metrics (GMV, basket sizes).
* **Data Quality & Testing:** Enforces schema integrity, primary key uniqueness, and accepted values using `dbt_utils`, `dbt_expectations`, and `dbt_date`.
* **Pushdown Query Engine:** Streamlit queries DuckDB directly with read-only locks, offloading KPI aggregations and time-series rollups to DuckDB's vectorized engine rather than loading large DataFrames into memory.

---

## 🛠️ Tech Stack

* **Compute & Storage:** [DuckDB](https://duckdb.org/)
* **Transformation & Testing:** [dbt (data build tool)](https://www.getdbt.com/) (`dbt-core`, `dbt-duckdb`)
* **Dashboard & Visualizations:** [Streamlit](https://streamlit.io/), [Altair](https://altair-viz.github.io/)
* **Language & Orchestration:** Python, SQL, Make

---

## 📁 Repository Structure

```plaintext
├── models/                     # dbt transformation models
│   ├── staging/                # Bronze -> Silver views
│   ├── intermediate/           # Silver ephemeral grain rollups
│   └── mart/                   # Gold analytical tables (fct_orders)
├── dbt_project.yml             # dbt configuration & materialization rules
├── packages.yml                # dbt packages (dbt_utils, dbt_expectations, dbt_date)
├── profiles.yml                # DuckDB local target connection
├── Streamlit.py                # BI application with query pushdown
├── Makefile                    # Project build automation
├── requirements.txt            # Python dependencies
└── README.md
