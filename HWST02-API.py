"""
HWST02-API.py
Weather lookup using the Open-Meteo API (free, no API key needed).

The user enters city names. For each city the program:
  1. Calls the geocoding API to get the city's location
  2. Calls the forecast API to get the current weather
  3. Stores the results in a 2D list
Then it prints a formatted report.
"""

import requests

# PART 1 - get input from the user
user_input = input("Enter city names separated by commas (e.g. Waco, Accra, London): ")
cities = user_input.split(",")

# 2D list to hold the data from each successful request
weather_list = []

# PART 2 - call the API for each city
for city in cities:
    city = city.strip()
    if city == "":
        continue

    try:
        # first API call - find the city's location
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(
                f"Error: request for {city} failed. Status code: {response.status_code}"
            )
            continue

        # convert payload to dictionary
        data = response.json()

        if "results" not in data:
            print(f"Error: {city} was not found. Check the spelling.")
            continue

        location = data["results"][0]
        name = location["name"]
        country = location["country"]
        latitude = location["latitude"]
        longitude = location["longitude"]

        # second API call - get the current weather for that location
        url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}"
            f"&longitude={longitude}"
            f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
            f"&temperature_unit=fahrenheit&wind_speed_unit=mph"
        )
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(
                f"Error: weather for {city} failed. Status code: {response.status_code}"
            )
            continue

        data = response.json()
        current = data["current"]
        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind = current["wind_speed_10m"]

        # add one row to the 2D list
        weather_list.append(
            [name, country, latitude, longitude, temperature, humidity, wind]
        )

    except requests.exceptions.RequestException:
        print(
            f"Error: could not connect to the API for {city}. Check your internet connection."
        )
    except KeyError:
        print(f"Error: the data returned for {city} was missing information.")

# PART 3 - print the report
print()
print("=" * 85)
print("CURRENT WEATHER REPORT".center(85))
print("=" * 85)

if len(weather_list) == 0:
    print("No data to display.")
else:
    print(
        f"{'City':<15}{'Country':<18}{'Latitude':>10}{'Longitude':>11}"
        f"{'Temp (F)':>10}{'Humidity':>10}{'Wind (mph)':>11}"
    )
    print("-" * 85)
    for row in weather_list:
        print(
            f"{row[0]:<15}{row[1]:<18}{row[2]:>10.2f}{row[3]:>11.2f}"
            f"{row[4]:>10}{row[5]:>9}%{row[6]:>11}"
        )

print("=" * 85)
