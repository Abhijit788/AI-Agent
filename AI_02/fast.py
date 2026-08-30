from ollama import Client
import json
import requests
import re

# Initialize Ollama client
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
{ "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string" }

Available Tools:
1. get_weather_info(location): This tool takes a location as input and returns the current weather information for that location.

Example 1:
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN: { "step": "PLAN", "content": "Seems like user is interested in math problem" }
PLAN: { "step": "PLAN", "content": "looking at the problem, we should solve this using BODMAS method" }
PLAN: { "step": "PLAN", "content": "Yes, The BODMAS is correct thing to be done here" }
PLAN: { "step": "PLAN", "content": "first we must multiply 3 * 5 which is 15" }
PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 15 / 10" }
PLAN: { "step": "PLAN", "content": "We must perform divide that is 15 / 10 = 1.5" }
PLAN: { "step": "PLAN", "content": "Now the new equation is 2 + 1.5" }
PLAN: { "step": "PLAN", "content": "Now finally lets perform the add 3.5" }
PLAN: { "step": "PLAN", "content": "Great, we have solved and finally left with 3.5 as ans" }
OUTPUT: { "step": "OUTPUT", "content": "3.5" }

Example 2:
START: Hey, Can you tell me the current weather in New York?
PLAN: { "step": "PLAN", "content": "Seems like user is interested in weather of New York" }
PLAN: { "step": "PLAN", "content": "lets see if we have any available tools from the list of available tools" }
PLAN: { "step": "PLAN", "content": "Great, we have get_weather_info tool available for this query" }
PLAN: { "step": "PLAN", "content": "I need to call get_weather_info tool for New York as input for location" }
TOOL: { "step": "TOOL", "tool": "get_weather_info", "input": "New York" }
PLAN: { "step": "OBSERVE", "tool": "get_weather_info", "output": "{\\"temp_c\\": 22.0, \\"condition\\": {\\"text\\": \\"Partly cloudy\\"}, \\"humidity\\": 65, \\"wind_kph\\": 15.1}" }
PLAN: { "step": "PLAN", "content": "The tool returned that the current temperature in New York is 22°C with Partly Cloudy conditions." }
PLAN: { "step": "PLAN", "content": "Now that I have observed the actual weather response, I can synthesize the final result." }
OUTPUT: { "step": "OUTPUT", "content": "The current weather in New York is 22°C with Partly cloudy conditions." }
"""

def get_weather_info(location):
    url = f"https://api.weatherapi.com/v1/current.json?key=a9da4328cf48463387c120619262308&q={location}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

available_tools = {
    "get_weather_info": get_weather_info
}

message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

print("🤖 Chatbot initialized! Type 'exit' to quit.\n")

# Outer loop keeps the session active across multiple questions
while True:
    user_query = input("👉 ")
    
    if user_query.strip().lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    if not user_query.strip():
        continue

    message_history.append({"role": "user", "content": user_query})

    # Inner loop processes the step-by-step reasoning cycle
    while True:
        response = client.chat(
            model="gemma:2b",
            messages=message_history,
            format="json"
        )

        raw_result = response.message.content.strip()
        message_history.append({"role": "assistant", "content": raw_result})

        # Extract only the first valid JSON object to avoid "Extra data" errors
        match = re.search(r"\{.*?\}", raw_result, re.DOTALL)

        if match:
            json_str = match.group(0)
            try:
                parsed_result = json.loads(json_str)
            except json.JSONDecodeError:
                print("⚠️ Failed to parse JSON, extracted string was:", json_str)
                continue
        else:
            print("⚠️ No valid JSON object found in output:", raw_result)
            continue

        step_type = parsed_result.get("step")

        if step_type == "START":
            print("🔥", parsed_result.get("content"))
            continue

        if step_type == "PLAN":
            print("🧠", parsed_result.get("content"))
            continue

        if step_type == "TOOL":
            tool_name = parsed_result.get("tool")
            input_data = parsed_result.get("input")
            print(f"🛠️ Tool call: {tool_name} ({input_data})")
            
            if tool_name in available_tools:
                tool_response = available_tools[tool_name](input_data)
            else:
                tool_response = f"Error: Tool '{tool_name}' not found."

            observe_payload = json.dumps({
                "step": "OBSERVE",
                "tool": tool_name,
                "output": tool_response
            })
            
            message_history.append({"role": "user", "content": observe_payload})
            continue

        if step_type == "OUTPUT":
            print("🤖", parsed_result.get("content"))
            