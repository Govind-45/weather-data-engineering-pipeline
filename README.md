# Weather Data Engineering Pipeline

A Python-based ETL pipeline that extracts weather data
from a public API, transforms and cleans the data using
Pandas, and stores it in a SQLite database for analysis.

## Architecture

Weather API
    ↓
Python Data Extraction
    ↓
Pandas Data Transformation
    ↓
SQLite Database
    ↓
SQL Analytics

## Tech Stack

- Python
- REST APIs
- Pandas
- SQLite
- SQL
- Git and GitHub

## Features

- Extract weather data for multiple cities.
- Clean and transform data using Pandas.
- Store structured weather records in SQLite.
- Analyze temperature, humidity, and wind speed using SQL.
- Export extracted data to CSV.
- Handle API request failures.

## Project Structure

weather-data-pipeline/
├── main.py
├── load_data.py
├── analytics.py
├── weather_data.csv
└── README.md

The SQLite database file is generated when the
data loading script runs.

## Installation

1. Clone this repository.
2. Create a virtual environment.
3. Install dependencies.
4. Run the extraction script.
5. Load the data into SQLite.
6. Run the analytics script.

## Commands

Install dependencies:

    pip install pandas requests

Extract weather data:

    python main.py

Load data into SQLite:

    python load_data.py

Run SQL analytics:

    python analytics.py

## Data Source

Open-Meteo public weather API:
https://open-meteo.com/

## Future Improvements

- Automate pipeline execution.
- Add robust logging and monitoring.
- Implement automated data quality tests.
- Add Apache Airflow orchestration.
- Extend analytics using PySpark.