import requests
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

# create LLM client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Inventory -> LLM can use information from this function to answer user's questions
def get_weather(city):
    if city == "Seoul":
        return 30
    if city == "New York":
        return 25
    if city == "Tokyo":
        return 30
    else:
        return 0

# Define the tool for the LLM to call - tell AI abotut the function
functions = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get the current temperature for the provided city in celsius.",
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
                  {"role": "system", "content": "You can call a function to get the temperature."}]


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=input_messages,
    # give the AI access to the tool and information
    functions=functions,
    function_call="auto", # let the AI decide if it wants to call the function
)

# first AI decision - understanding the user's question and deciding whether to call a function or not
message = response.choices[0].message
print("First LLM response:", message)


# function_call=FunctionCall(arguments='{"city":"Seoul"}', name='get_weather')

# If it decided to call get_weather:
if message.function_call:
    func_name = message.function_call.name # get_weather
    args = json.loads(message.function_call.arguments) # Seoul

    if func_name == "get_weather":
        temp = get_weather(**args) # get_weather("Seoul")
        function_response = { "temperature": temp }
    else:
        print("Unknown function call:", func_name)


    # system message to tell the LLM that it can use the function call result to generate a followup response
    followup_messages = [
        {"role": "system", "content": "Reply to user with the current weather in the city."},
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