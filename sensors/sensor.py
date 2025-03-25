import os
import sys
import time
import random
import requests
from datetime import datetime
from dotenv import load_dotenv

def get_env_var(name, cast_func=str, default=None):
    value = os.environ.get(name, default)
    if value is None:
        raise ValueError(f"Environment variable '{name}' is not set")
    try:
        return cast_func(value)
    except Exception as e:
        raise ValueError(f"Error casting env var '{name}': {e}")

def main():
    # Check that a config file was provided as a command-line argument.
    if len(sys.argv) < 2:
        print("Usage: python3 sensor.py config.env")
        sys.exit(1)

    config_file = sys.argv[1]
    load_dotenv(dotenv_path=config_file)

    # Load configuration from environment variables.
    sensor_id = get_env_var("SENSOR_ID", int)
    sensor_latitude = get_env_var("SENSOR_LATITUDE", float)
    sensor_longitude = get_env_var("SENSOR_LONGITUDE", float)
    sensor_type = get_env_var("SENSOR_TYPE", str)
    period = get_env_var("PERIOD", float)  # in seconds
    api_url = get_env_var("API_URL", str)  # e.g., http://flask_app:5000/submit
    min_value = get_env_var("MIN_VALUE", float)
    max_value = get_env_var("MAX_VALUE", float)

    # Mapping sensor type to its unit.
    unit_mapping = {
        "TemperatureSensor": "°C",
        "PressureSensor": "hPa",
        "AirQualitySensor": "PM10",
        "CO2Sensor": "ppm"
    }
    unit = unit_mapping[sensor_type]

    print("Starting virtual sensor with the following configuration:")
    print(f"Sensor ID: {sensor_id}, Location: ({sensor_latitude}, {sensor_longitude})")
    print(f"Type: {sensor_type}, Unit: {unit}")
    print(f"Sending data every {period} seconds to {api_url}")
    print(f"Data range: {min_value} to {max_value}\n")

    while True:
        harakiri(sensor_id)

        # Generate timestamp in UTC format: "YYYY-MM-DD HH:MM UTC"
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M") + " UTC"
        # Generate a random value between min_value and max_value.
        value = round(random.uniform(min_value, max_value), 2)
        payload = {
            "sensor_id": sensor_id,
            "sensor_location": {"latitude": sensor_latitude, "longitude": sensor_longitude},
            "sensor_type": sensor_type,
            "unit": unit,
            "timestamp": timestamp,
            "value": value
        }
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code != 201:
                print(f"Error sending data: {response.text}")
            else:
                print(f"Data sent successfully: {payload}")
        except Exception as e:
            print(f"Exception occurred while sending data: {e}")

        time.sleep(period)

def harakiri(sensor_id):
    # Check if this sensor's id is in the death_note list.
    try:
        death_response = requests.get("http://flask_app:5000/death_note")
        if death_response.status_code == 200:
            death_ids = death_response.json()  # expecting a list of sensor ids
            if sensor_id in death_ids:
                sys.exit(0)
    except Exception as e:
        # Ignore errors in checking the death_note list.
        pass

if __name__ == "__main__":
    main()

