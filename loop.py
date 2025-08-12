import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from chat import get_response

# Load environment variables from .env file

load_dotenv()
# Initialize OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

while True:
    user_input = input("User: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        print ("Exiting the chatbot. Goodbye!")
        break

    #stream = false
    print("Bot: ", get_response(user_input, stream = False))

    #stream = true
    response = get_response(user_input, stream = True)
    print("Bot:", end = " ", flush = True)
    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end = "", flush = True)
    print()