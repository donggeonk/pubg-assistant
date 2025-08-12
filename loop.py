import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
# Initialize OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

while True:
    user_input = input("User: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Exiting the chatbot. Goodbye!")
        break

    # Chat Completion API
    # Chat Completion API
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role":"system",  "content":"You are a helpful assistant to answer user's question concisely"}, # pointing to a LLM system prompt
        {"role":"user",    "content": user_input}, # user input  
        ],
    stream=True # parameter to control whether the response is chucnked or not
    )

    # response is a list now (stream=True)
    print("Bot:", end=" ", flush=True)
    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
    print()