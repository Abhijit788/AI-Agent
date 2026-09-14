from ollama import Client
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

weather_api_key = os.getenv("WEATHER_API_KEY")  # Get the weather API key from environment variables
client = Client(host="http://localhost:11434")

# response = client.chat(
#     model="phi4-mini:3.8b",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a helpful assistant."
#         },
#         {
#             "role": "user",
#             "content": "Can you write me a java program to calculate sum of n numbers?"
#         }
#     ],
#     format="json",
# )
def extract_forecast(tool_result, requested_date):

    forecast_days = tool_result["forecast"]["forecastday"]

    for day in forecast_days:

        if day["date"] == requested_date:
            return {
                "location": tool_result["location"]["name"],
                "country": tool_result["location"]["country"],
                "date": day["date"],
                "max_temperature_c": day["day"]["maxtemp_c"],
                "min_temperature_c": day["day"]["mintemp_c"],
                "average_temperature_c": day["day"]["avgtemp_c"],
                "condition": day["day"]["condition"]["text"],
                "chance_of_rain": day["day"]["daily_chance_of_rain"],
                "uv": day["day"]["uv"]
            }

    return None

def get_current_weather_info(location):
    url = f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}"
    response = requests.get(url)
    if response.status_code == 200:
        res_json = response.json()
        return {
            "location": res_json["location"]["name"],
            "country": res_json["location"]["country"],
            "date": res_json["current"]["last_updated"].split(" ")[0],
            "temperature_c": res_json["current"]["temp_c"],
            "condition": res_json["current"]["condition"]["text"],
            "humidity": res_json["current"]["humidity"],
            "wind_kph": res_json["current"]["wind_kph"]
        }
    return None

location = "New York"
date = "2026-08-31"
# url = f"https://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={location}&dt={date}"

# url2 = f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}"

# res= requests.get(url)
# json_res = json.loads(res.content)
# # print(json_res)

# print(extract_forecast(json_res, date))

url = f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}"
response = requests.get(url)
print(response.status_code)