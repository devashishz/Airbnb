🚀 AIRBNB E2E Pipeline
📌 Overview

This project is an end-to-end modern data pipeline that builds a scalable, maintainable, and production-ready data engineering workflows.

It integrates:

Snowflake as the cloud data warehouse

dbt (Data Build Tool) for transformation, modeling, and testing

Dagster for orchestration and observability of data pipelines

Streamlit for interactive dashboards and insights

Best practices in modularity, version control, and CI/CD

The goal of this project is to show how raw data can be ingested, transformed, orchestrated, and visualized in a seamless way using DBT on Snowflake.

🛠️ Tech Stack

Snowflake – Data warehouse

dbt – SQL-based transformations, tests, and documentation

Dagster – Orchestration, observability, and lineage tracking

Streamlit – Lightweight data app framework for building dashboards

Git & GitHub – Version control and collaboration

🔄 Architecture

Ingestion Layer

Raw data loaded into Snowflake staging tables.

Transformation Layer

dbt models structure the data into staging → intermediate → mart layers.

Data quality checks with dbt tests (uniqueness, null checks, referential integrity).

Orchestration & Monitoring

Dagster schedules and orchestrates dbt runs.

Built-in lineage and observability ensure reliable pipelines.

Visualization

Streamlit dashboard built on top of Snowflake queries & dbt models.

Business-friendly UI for KPIs and trend monitoring.
