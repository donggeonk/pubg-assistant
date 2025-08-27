import requests
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from tools import get_weather

# create LLM client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the tool for the LLM to call - tell AI abotut the function
functions = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get the current, not yesterday or any time but current, right now, weather (which includes temperature, humidity, etc.) for the provided city in an appropriate unit. .",
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
#print("First LLM response:", message)


if message.function_call:
    func_name = message.function_call.name
    args = json.loads(message.function_call.arguments)

    weather_data = get_weather(**args)
    
    temp = {"temperature": weather_data["temp_c"]}
    description = {"description": weather_data["description"]}
    humidity = {"humidity": weather_data["humidity_pct"]}
    wind_speed = {"wind_speed": weather_data["wind_kph"]}
    function_response = {**temp, **description, **humidity, **wind_speed}


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