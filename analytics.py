import sqlite3
import pandas as pd
from pathlib import Path

# Locate the database
DB_FILE = Path(__file__).resolve().parent / "weather.db"


def run_analytics():
    connection = sqlite3.connect(DB_FILE)

    try:
        # Query 1: Complete weather report
        print("\n===== WEATHER REPORT =====")

        query = """
            SELECT
                city,
                temperature_c,
                humidity_percent,
                wind_speed_kmh,
                observed_at
            FROM weather
            ORDER BY temperature_c DESC;
        """

        df = pd.read_sql_query(query, connection)
        print(df.to_string(index=False))

        # Query 2: Temperature and humidity summary
        print("\n===== CITY-WISE SUMMARY =====")

        summary_query = """
            SELECT
                city,
                ROUND(AVG(temperature_c), 2) AS avg_temperature,
                ROUND(AVG(humidity_percent), 2) AS avg_humidity,
                ROUND(MAX(wind_speed_kmh), 2) AS max_wind_speed
            FROM weather
            GROUP BY city
            ORDER BY avg_temperature DESC;
        """

        summary = pd.read_sql_query(
            summary_query,
            connection
        )

        print(summary.to_string(index=False))

        # Query 3: Total records
        print("\n===== DATA QUALITY CHECK =====")

        count_query = """
            SELECT COUNT(*) AS total_records
            FROM weather;
        """

        result = pd.read_sql_query(
            count_query,
            connection
        )

        print(f"Total records in database: {result.iloc[0, 0]}")

    finally:
        connection.close()


if __name__ == "__main__":
    run_analytics()