import requests
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from tools import get_weather

# create LLM client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def get_weather(city):
#     if city == "Seoul":
#         return 25
#     if city == "New York":
#         return 15
#     if city == "Tokyo":
#         return 20
#     else:
#         return 0

# Define the tool for the LLM to call - tell AI abotut the function
functions = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get current weather, including temperature in celsius, wind speed in km/h, humidity percentage, and weather description.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "Name of the city"},
        },
        "required": ["city"],
    },
}]

user_input = input("User: ")
# instructions tell the AI that it can call a function to get the weather
input_messages = [{"role": "user", "content": user_input},
                  {"role": "system", "content": "You can call a function to get the weather."}]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=input_messages,
    # give the AI access to the tool
    functions=functions,
    function_call="auto",
)

message = response.choices[0].message
print("First LLM response:", message)

# If it decided to call get_weather:
if message.function_call:
    args = json.loads(message.function_call.arguments)
    print("Arguments of get_weather:", args)
    temp = get_weather(**args)
    print("Temperature from get_weather:", temp)

    # system message to tell the LLM that it can use the function call result to generate a followup response
    followup_messages = [
        {"role": "system", "content": "Reply to user with the current weather in the city."},
        {"role": "user",   "content": user_input},
        message,
        {
            "role": "function",
            "name": message.function_call.name,
            "content": json.dumps({ "temperature": temp })
        }
    ]

    # send the function call result back to the LLM so it can generate a followup response
    followup = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=followup_messages,
    )
    print("Bot:", followup.choices[0].message.content)
else:
    # otherwise it answered directly or didn't call a function
    print("Bot:", message.content)