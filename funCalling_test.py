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
    "description": "Get today's weather information for the provided city, including temperature in Celcius, weather description, humidity in pct, and wind speed in kph.",
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
                  {"role": "system", "content": "You can call a function get_weather to get the temperature, weather description, humiditym and wind speed. If there is no function dedicated to the question, do not call the function."}]


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
    func_name = message.function_call.name
    args = json.loads(message.function_call.arguments)

    weather_data = get_weather(**args)

    temp = {"temperature" : weather_data["temp_c"]}
    description = {"description" : weather_data["description"]}
    humidity = {"humidity" : weather_data["humidity_pct"]}
    wind_speed = {"wind_speed" : weather_data["wind_kph"]}
    function_response = {**temp, **description, **humidity, **wind_speed}

    # if func_name == "get_temperature":
    #     temp = get_temperature(**args) # get_weather("Seoul")
    #     function_response = { "temperature": temp }
    # elif func_name == "get_wind_speed":
    #     wind_speed = get_wind_speed(**args)
    #     function_response = { "wind_speed": wind_speed }
    # else:
    #     print("Unknown function call:", func_name)


    # system message to tell the LLM that it can use the function call result to generate a followup response
    followup_messages = [
        {"role": "system", "content": "Reply to user with the current temperature, weather description, humidity, and wind speed in the city, or all together. Be friendly without putting any special characters in your response"},
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