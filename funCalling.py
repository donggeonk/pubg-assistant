import requests
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

# create LLM client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Inventory -> LLM can use information from this function to answer user's questions
def get_temperature(city):
    if city == "Seoul":
        return 30
    if city == "London":
        return 28
    if city == "Tokyo":
        return 29
    if city == "San Diego":
        return 24
    
def get_humidity(city):
    if city == "Seoul":
        return 65
    if city == "London":
        return 76
    if city == "Tokyo":
        return 64
    if city == "San Diego":
        return 56
    
def get_wind_speed(city):
    if city == "Seoul":
        return 7
    if city == "London":
        return 8
    if city == "Tokyo":
        return 6
    if city == "San Diego":
        return 10

# Define the tool for the LLM to call - tell AI abotut the function
functions = [{
    "type": "function",
    "name": "get_temperature",
    "description": "Get the current, not yesterday or any time but current, right now, temperature for the provided city in celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "Name of the city"},
        },
        "required": ["city"],},
    },
    {
    "type": "function",
    "name": "get_humidity",
    "description": "Get the current, not yesterday or any time but current, right now, humidity for the provided city in percentage.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "Name of the city"},
        },
        "required": ["city"],},
    },
    {
    "type": "function",
    "name": "get_wind_speed",
    "description": "Get the current, not yesterday or any time but current, right now, wind speed for the provided city in kilometers per hour.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "Name of the city"},
        },
        "required": ["city"],},
    }
]

user_input = input("User: ")
# instructions tell the AI that it can call a function to get the weather
input_messages = [{"role": "user", "content": user_input},
                  {"role": "system", "content": "Out of many functions, you can call a function to get an information you need from the question of the user. If there is no such function that matches with what the user seeks, do not call a function."}]


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=input_messages,
    # give the AI access to the tool and information
    functions=functions, # custom skill LLM to have
    function_call="auto", # let the AI decide if it wants to call the function
)

# first AI decision - understanding the user's question and deciding whether to call a function or not
message = response.choices[0].message
print("First LLM response:", message)


if message.function_call:
    func_name = message.function_call.name
    args = json.loads(message.function_call.arguments)

    if func_name == "get_temperature":
        temp = get_temperature(**args)
        function_response = { "temperature": temp }
    if func_name == "get_humidity":
        humidity = get_humidity(**args)
        function_response = { "humidity": humidity}
    if func_name == "get_wind_speed":
        wind_speed = get_wind_speed(**args)
        function_response = { "wind_speed": wind_speed}
    else:
        print("Unknown function call:", func_name)


    followup_messages = [
        {"role": "system", "content": "Reply to user with what the user has asked for and information you got from other functions."},
        {"role": "user",   "content": user_input},
        message,
        {
            "role": "function",
            "name": func_name,
            "content": json.dumps(function_response)
        }
    ]

    followup = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=followup_messages,
    )
    print("Bot:", followup.choices[0].message.content)
else:
    print("Bot:", message.content)