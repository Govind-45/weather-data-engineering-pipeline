import sqlite3
import pandas as pd
from pathlib import Path

# File paths
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "weather_data.csv"
DB_FILE = BASE_DIR / "weather.db"


def transform_data(df):
    """Clean and transform the extracted weather data."""

    # Remove duplicate records
    df = df.drop_duplicates(
        subset=["city", "observed_at"],
        keep="last"
    )

    # Convert numeric columns to appropriate types
    numeric_columns = [
        "temperature_c",
        "humidity_percent",
        "wind_speed_kmh"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove rows with missing essential values
    df = df.dropna(
        subset=[
            "city",
            "temperature_c",
            "humidity_percent",
            "wind_speed_kmh",
            "observed_at"
        ]
    )

    # Standardize city names
    df["city"] = df["city"].str.strip().str.title()

    return df


def load_data(df):
    """Load transformed records into SQLite."""

    with sqlite3.connect(DB_FILE) as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                temperature_c REAL NOT NULL,
                humidity_percent REAL NOT NULL,
                wind_speed_kmh REAL NOT NULL,
                observed_at TEXT NOT NULL,
                extracted_at TEXT NOT NULL,
                UNIQUE(city, observed_at)
            )
        """)

        df.to_sql(
            "weather",
            connection,
            if_exists="append",
            index=False,
            method=None
        )

        print("Data loaded into SQLite successfully!")


if __name__ == "__main__":

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            "weather_data.csv not found. Run main.py first."
        )

    # Extract the CSV data
    df = pd.read_csv(CSV_FILE)

    print(f"Records extracted: {len(df)}")

    # Transform
    df = transform_data(df)

    print(f"Records after cleaning: {len(df)}")

    # Load
    load_data(df)

    print(f"Database location: {DB_FILE}")