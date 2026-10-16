import requests
import pandas as pd
from datetime import datetime

# Cities we want to collect weather data for
CITIES = ["Lucknow", "Delhi", "Mumbai", "Bengaluru", "Prayagraj"]

def extract_weather_data():
    """Extract weather data from the Open-Meteo API."""

    records = []

    for city in CITIES:
        try:
            # Get city coordinates
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"

            geo_response = requests.get(
                geo_url,
                params={"name": city, "count": 1, "language": "en"},
                timeout=15
            )
            geo_response.raise_for_status()

            locations = geo_response.json().get("results", [])

            if not locations:
                print(f"Location not found: {city}")
                continue

            location = locations[0]
            latitude = location["latitude"]
            longitude = location["longitude"]

            # Fetch current weather
            weather_url = "https://api.open-meteo.com/v1/forecast"

            weather_response = requests.get(
                weather_url,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": (
                        "temperature_2m,relative_humidity_2m,"
                        "wind_speed_10m"
                    )
                },
                timeout=15
            )
            weather_response.raise_for_status()

            weather = weather_response.json()["current"]

            records.append({
                "city": city,
                "temperature_c": weather["temperature_2m"],
                "humidity_percent": weather["relative_humidity_2m"],
                "wind_speed_kmh": weather["wind_speed_10m"],
                "observed_at": weather["time"],
                "extracted_at": datetime.now().isoformat()
            })

            print(f"Successfully extracted data for {city}")

        except (requests.RequestException, KeyError, ValueError) as error:
            print(f"Failed to extract data for {city}: {error}")

    return records


if __name__ == "__main__":
    weather_records = extract_weather_data()

    if weather_records:
        df = pd.DataFrame(weather_records)
        print("\nWeather Data Preview:")
        print(df.to_string(index=False))

        df.to_csv("weather_data.csv", index=False)
        print(f"\nSaved {len(df)} records to weather_data.csv")
    else:
        print("No weather data collected. Please check your connection.")