from ollama import Client
import json
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from models.model import CurrentWeatherModel, FutureWeatherModel
load_dotenv()  # Load environment variables from .env file

weather_api_key = os.getenv("weather_api_key")

client = Client(host="http://localhost:11434")

SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.
You can also call a tool if required from the list of available tools.
For every tool call wait for the observe step which is the output from the called tool.

Rules:
- Strictly Follow the given JSON output format
- Only run one step at a time.
- The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and OUTPUT.

Output JSON Format:
{ "step": "START" | "PLAN" | "TOOL" | "OUTPUT",
    "content": "string",
    "tool": "string",
    "input": {} }

For TOOL:
- tool must contain the exact tool name.
- input must be a JSON object containing the arguments required by that tool.
- Do not put multiple arguments into a single string.

Available Tools:
1. get_current_weather_info(location): This tool takes a location as input and returns the current weather information for that location.
Arguments:
{
    "location": "string"
}


2. get_future_weather_info(location, date): This tool takes a location and a date as input and returns the weather forecast for that location from today till the specified date.
Arguments:
{
    "location": "string",
    "date": "YYYY-MM-DD"
}



Example 1:
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: { "step": "PLAN", "content": "Apply BODMAS/operator precedence to solve the expression." }
PLAN: { "step": "PLAN", "content": "Calculate 3 * 5 = 15, then 15 / 10 = 1.5." }
PLAN: { "step": "PLAN", "content": "Calculate 2 + 1.5 = 3.5." }
OUTPUT: { "step": "OUTPUT", "content": "3.5" }


Example 2:
START: Current Date: 2026-08-30. Hey, Can you tell me the current weather in New York?
PLAN: { "step": "PLAN", "content": "Use get_current_weather_info to retrieve the current weather for New York." }
TOOL: { "step": "TOOL", "tool": "get_current_weather_info", "input": {
"location": "New York"
} }
PLAN: { "step": "OBSERVE", "tool": "get_current_weather_info", "output": "{\\"temp_c\\": 22.0, \\"condition\\": {\\"text\\": \\"Partly cloudy\\"}, \\"humidity\\": 65, \\"wind_kph\\": 15.1}" }
PLAN: { "step": "PLAN", "content": "Use the returned weather data to provide the current conditions in New York." }
OUTPUT: { "step": "OUTPUT", "content": "The current weather in New York is 22°C with Partly cloudy conditions." }


Example 3:
START: Current Date: 2026-08-30. Hey, Can you tell me tomorrow's weather forecast for Mumbai?
PLAN: { "step": "PLAN", "content": "Tomorrow is 2026-08-31. Use get_future_weather_info to retrieve Mumbai's forecast for that date." }
TOOL: { "step": "TOOL", "tool": "get_future_weather_info", "input": {
"location": "Mumbai",
"date": "2026-08-31"
} }
PLAN: { "step": "OBSERVE", "tool": "get_future_weather_info", "output": "{\\"forecast\\": {\\"forecastday\\": [{\\"date\\": \\"2026-08-31\\", \\"day\\": {\\"maxtemp_c\\": 28.0, \\"mintemp_c\\": 18.0, \\"condition\\": {\\"text\\": \\"Sunny\\"}}}]}}" }
PLAN: { "step": "PLAN", "content": "Use the forecast data for 2026-08-31 to prepare the final answer." }
OUTPUT: { "step": "OUTPUT", "content": "The weather forecast for Mumbai on 2026-08-31 is a maximum temperature of 28°C, a minimum temperature of 18°C, and Sunny conditions." }
"""


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

def get_future_weather_info(location,date):
    url = f"https://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={location}&dt={date}"
    response = requests.get(url)
    if response.status_code == 200:
        res_json =  response.json()
        return extract_forecast(res_json, date)
    return None

available_tools = {
    "get_current_weather_info": get_current_weather_info,
    "get_future_weather_info": get_future_weather_info,
}

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

user_query = input("👉 ")

user_context =  f"""
Current date: {datetime.now().strftime("%Y-%m-%d")}.

User query:
{user_query}
"""


messages.append({
    "role": "user",
    "content": user_context
})


while True:
    if user_query.lower() in ["exit", "quit"]:
        print("Exiting the assistant. Goodbye!")
        break
    
    response = client.chat(
        model="phi4-mini:3.8b",
        messages=messages,
        format="json"
    )


    raw_result = response["message"]["content"]

    try:
        result = json.loads(raw_result)

    except json.JSONDecodeError:
        print("Invalid JSON returned by model:")
        print(raw_result)
        break

    step = result.get("step")
    content = result.get("content")

    # Store model response
    messages.append({
        "role": "assistant",
        "content": raw_result
    })



    if step == "START":
    
            print("🧠", content)
    
            # Tell the model to continue
            messages.append({
                "role": "user",
                "content": "Continue with the next step."
            })
            continue
    
    elif step == "PLAN":

        print("🧠", content)

        # Tell the model to continue
        messages.append({
            "role": "user",
            "content": "Continue with the next step."
        })

        continue


    elif step == "TOOL":
        tool_name = result.get("tool")
        tool_input = result.get("input")
        if tool_name not in available_tools:
            print("❌ Unknown tool:", tool_name)
            break
        print("🔧 Calling tool:", tool_name)

        tool_function = available_tools[tool_name]

        if tool_name == "get_current_weather_info":
            validated_input = CurrentWeatherModel(**tool_input)
        elif tool_name == "get_future_weather_info":
            validated_input = FutureWeatherModel(**tool_input)

        try:
            tool_result = tool_function(**validated_input.model_dump())
        except Exception as e:
            print("❌ Error parsing input for get_future_weather_info:", e)
            break
        
        messages.append({
        "role": "user",
        "content": json.dumps({
            "step": "OBSERVE",
            "tool": tool_name,
            "output": tool_result
            })
        })
        continue
        
    elif step == "OBSERVE":
        
        print("🔍 Observed tool output:", content)
        # Tell the model to continue
        messages.append({
            "role": "user",
            "content": "Continue with the next step."
        })
        continue

    elif step == "OUTPUT":

        print("✅", content)
        break

    else:

        print("❌ Invalid step:", step)
        break