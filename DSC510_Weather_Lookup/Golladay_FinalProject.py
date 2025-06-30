# DSC 510
# Week 10
# Purpose: Weather Program
# Programming Assignment Final Project
# Author: Cory Golladay
# 8/10/2024

import requests

# Define constants
API_KEY = '72583b46975c64734acfd7824857797b'
BASE_GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
BASE_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
BASE_GEO_URL_ZIP = "http://api.openweathermap.org/geo/1.0/zip"


# Define function to get users preferred weather lookup method.
def get_lookup_choice():
    while True:
        print("Welcome to the Weather Lookup program.")
        print("1. Lookup by Zip Code")
        print("2. Lookup by City, State")
        choice = input("Please select your preferred lookup method: ")
        if choice in ['1','2']:
            return choice
        else:
            print("Please enter a valid choice - 1 or 2.")


# Define function to get location data (latitude and longitude) from OpenWeatherMap using city amd state.
def get_location_city_state(city, state):
    try:
        response = requests.get(BASE_GEO_URL, params={'q': f"{city},{state}", 'appid': API_KEY})
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
        else:
            print(f"No location found for {city}, {state}.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location data: {e}")
        return None


# Define function to get location data (latitude and longitude) from OpenWeatherMap using zip code.
def get_location_zip(zip_code):
    try:
        response = requests.get(f"{BASE_GEO_URL_ZIP}", params={'zip': zip_code, 'appid': API_KEY})
        response.raise_for_status()
        data = response.json()
        if data:
            return data['lat'], data['lon']
        else:
            print(f"No location found for zip code {zip_code}.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location data: {e}")
        return None


# Define function to get the weather data using latitude and longitude.
def get_weather(lat, lon, units):
    try:
        response = requests.get(BASE_WEATHER_URL, params={'lat': lat, 'lon': lon, 'appid': API_KEY, 'units': units})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


# Define function to display the weather information.
def display_weather(data):
    print(f"Location: {data['name']}")
    print(f"Current Temp: {data['main']['temp']}°")
    print(f"Feels Like: {data['main']['feels_like']}°")
    print(f"Low Temp: {data['main']['temp_min']}°")
    print(f"High Temp: {data['main']['temp_max']}°")
    print(f"Pressure: {data['main']['pressure']} hPa")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Weather Description: {data['weather'][0]['description']}")


# Main function to run the program
def main():
    while True:
        choice = get_lookup_choice()
        if choice == '1':
            zip_code = input("Enter zip code: ")
            location = get_location_zip(zip_code)
        else:
            city = input("Enter city name: ")
            state = input("Enter state abbreviation (e.g., CA for California): ")
            location = get_location_city_state(city, state)

        if location:
            lat, lon = location
            units_choice = input("Choose units: (1) Celsius (2) Fahrenheit (3) Kelvin: ")
            units_map = {'1': 'metric', '2': 'imperial', '3': 'standard'}
            units = units_map.get(units_choice, 'metric')  # default to Celsius

            weather_data = get_weather(lat, lon, units)
            if weather_data:
                display_weather(weather_data)

        run_again = input("Would you like to look up another location? (yes/no): ").lower()
        if run_again != 'yes':
            break


# Proper call to main
if __name__ == "__main__":
    main()