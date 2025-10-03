import requests
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from search_database import search
from pubg_stats import get_pubg_data

# create LLM client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the tool for the LLM to call - tell AI about the function
functions = [{
    "type": "function",
    "name": "search",
    "description": "Search top 3 most related PUBG rules that matches the user's query from the Pinecone vector database.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "User's query about PUBG rules in a noun format"},
        },
        "required": ["query"],
    },
}, {
    "type": "function",
    "name": "get_pubg_data",
    "description": "Return the player's PUBG stats in squad-fpp mode",
    "parameters": {
        "type": "object",
        "properties": {
            "player_name": {"type": "string", "description": "Player's PUBG in-game name to search for"},
        },
        "required": ["player_name"],
    },
}]



user_input = input("User: ")
# instructions tell the AI that it can call a function to search PUBG rules and PUBG stats
input_messages = [{"role": "user", "content": user_input},
                  {"role": "system", "content": "You can call a function to search PUBG rules by passing in a query in a noun format to a Pinecone database or you can search for a player's lifetime PUBG stats in squad-fpp mode."}]


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=input_messages,
    # give the AI access to the tool
    functions=functions,
    function_call="auto",
)

message = response.choices[0].message
# print("First LLM response:", message)

# If it decided to call get_weather:
if message.function_call:
    func_name = message.function_call.name
    args = json.loads(message.function_call.arguments)

    print("Arguments of search:", args)

    if func_name == "search":
        rules = search(**args)
        function_response = { "pubg_rules": rules }
    elif func_name == "get_pubg_data":
        pubg_stats = get_pubg_data(**args)
        function_response = { "pubg_stats": pubg_stats }
    else:
        print("Unknown function call:", func_name)

    # system message to tell the LLM that it can use the function call result to generate a followup response
    # RAG (Retrieval Augmented Generation)
    response_instruction = """
    If the user is asking about the PUBG rules, reply to user with the correct PUBG rule. You have 3 rules from the database to help you answer the user's question, but only some of them might apply as these are from vector database search with some uncertainty. If none of the rules apply, say 'Sorry, I don't know how to help with that.'
    If the user is asking about the player's PUBG stats, reply to user with the player's PUBG stats in squad-fpp mode. You have the player's PUBG stats data from official PUBG API, you can use all or some of the data depending on the user's question. If you don't have the stats, say 'Sorry, I don't know how to help with that.'
    """


    followup_messages = [
        {"role": "system", "content": response_instruction},
        {"role": "user",   "content": user_input},
        message,
        {
            "role": "function",
            "name": message.function_call.name,
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