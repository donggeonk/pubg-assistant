import os
import requests
from dotenv import load_dotenv

# 1. Load the API key from .env
load_dotenv()  
API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city: str) -> float:
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    resp = requests.get(endpoint, params=params)
    resp.raise_for_status() # Raise an error for bad responses (4xx, 5xx)

    data = resp.json()
    print(data)
    weather = {
        "temp_c": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity_pct": data["main"]["humidity"],
        "wind_kph": data["wind"]["speed"] * 3.6  # m/s → km/h
    }
    # temperature = weather["temp_c"]
    return weather

city = input("Enter city name: ")
try:
    weather = get_weather(city)
    print(f"Current weather in {city}:")
    print(f"Temperature: {weather['temp_c']}°C")
    print(f"Conditions: {weather['description']}")
    print(f"Humidity: {weather['humidity_pct']}%")
    print(f"Wind Speed: {weather['wind_kph']:.1f} km/h")
except requests.HTTPError as e:
    print("Failed to fetch weather:", e)
except KeyError:
    print("Unexpected response format")



# def weather(city):
#     return [get_weather(city), is_raining(city), get_humidity(city)]

# # Inventory -> LLM can use information from this function to answer user's questions
# def get_weather(city):
#     if city == "Seoul":
#         return 25
#     if city == "New York":
#         return 15
#     if city == "Tokyo":
#         return 20
#     else:
#         return 0

# def is_raining(city):
#     if city == "Seoul":
#         return True
#     if city == "New York":
#         return False
#     if city == "Tokyo":
#         return True
#     else:
#         return False
    
# def get_functions():
#     return functions