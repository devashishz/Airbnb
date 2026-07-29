.PHONY: install build run setup clean

install:
	pip install --upgrade pip
	pip install -r requirements.txt

build:
	dbt deps
	dbt build

run:
	streamlit run Streamlit.py

setup: install build run

clean:
	dbt clean
