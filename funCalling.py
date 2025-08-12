import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
# Initialize OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

user_input = input("User: ")


def get_temperature(city):
    if city == "Seoul":
        return 25
    elif city == "New York":
        return 15
    elif city == "Tokyo":
        return 20
    elif city == "London":
        return 10
    else:
        return None


functions = [{
    "type": "function",
    "name": "get_temperature",
    "description": "Get the current temperature for the provided city in celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "Name of the city"},
        },
        "required": ["city"],},
    }
]


# Chat Completion API
response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role":"system",  "content":"You are a helpful assistant to answer user's question concisely"}, # pointing to a LLM system prompt
    {"role":"user",    "content": user_input}, # user input  
    ],
  stream=False # parameter to control whether the response is chucnked or not
)

# presonses api print (when stream=False)
print(response.choices[0].message.content)



# response is a list now (stream=True)
# print("Bot:", end=" ", flush=True)
# for chunk in response:
#     delta = chunk.choices[0].delta.content
#     if delta:
#         print(delta, end="", flush=True)
# print()