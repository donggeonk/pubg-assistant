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
    if city == "New York":
        return 25
    if city == "Tokyo":
        return 28
    else:
        return None
    
def get_wind_speed(city):
    if city == "Seoul":
        return 5
    if city == "New York":
        return 10
    if city == "Tokyo":
        return 7
    else:
        return None

# Define the tool for the LLM to call - tell AI abotut the function
functions = [{
    "type": "function",
    "name": "get_temperature",
    "description": "Get today's temperature for the provided city in celsius.",
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
    "description": "Get today's wind speed for the provided city in mph.",
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
                  {"role": "system", "content": "You can call a function to get the temperature or wind speed. If there is no function dedicated to the question, do not call the function."}]


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

# function_call=FunctionCall(arguments='{"city":"Seoul"}', name='get_weather')

# If it decided to call get_weather:
if message.function_call:
    func_name = message.function_call.name # get_temperature & get_wind_speed 
    args = json.loads(message.function_call.arguments) # Seoul

    if func_name == "get_temperature":
        temp = get_temperature(**args) # get_weather("Seoul")
        function_response = { "temperature": temp }
    elif func_name == "get_wind_speed":
        wind_speed = get_wind_speed(**args)
        function_response = { "wind_speed": wind_speed }
    else:
        print("Unknown function call:", func_name)


    # system message to tell the LLM that it can use the function call result to generate a followup response
    followup_messages = [
        {"role": "system", "content": "Reply to user with the current temperature or wind speed in the city."},
        {"role": "user",   "content": user_input},
        message,  # the function_call event
        {
            "role": "function",
            "name": func_name,
            "content": json.dumps(function_response)
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