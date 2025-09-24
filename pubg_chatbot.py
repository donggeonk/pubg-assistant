import requests
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from search_database import search
# from tools import get_weather

# create LLM client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the tool for the LLM to call - tell AI about the function
functions = [{
    "type": "function",
    "name": "search",
    "description": "Search top 3 PUBG rules that matches the user's query from the Pinecone database.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "User's query about PUBG rules in a noun format"},
        },
        "required": ["query"],
    },
}]

user_input = input("User: ")
# instructions tell the AI that it can call a function to search PUBG rules
input_messages = [{"role": "user", "content": user_input},
                  {"role": "system", "content": "You can call a function to search PUBG rules by passing in a query in a noun format to a Pinecone database."}]


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
    print("Arguments of search:", args)
    rules = search(**args)
    print("Top 3 pubg rules from search:", rules)

    # system message to tell the LLM that it can use the function call result to generate a followup response
    followup_messages = [
        {"role": "system", "content": "Reply to user with the correct PUBG rule."},
        {"role": "user",   "content": user_input},
        message,
        {
            "role": "function",
            "name": message.function_call.name,
            "content": json.dumps({ "rules": rules })
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