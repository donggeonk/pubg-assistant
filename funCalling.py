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
    


#Chat Completion API
response = client.chat.completions.create(
    model = "gpt-4o",
    messages = [
        {"role": "system", "content": "You are a helpful assistant to answer user's question concicsely"}, #Instruction
        {"role": "user", "content": user_input}, #User input
    ],
    stream = False #Parameter to control whether the response is chuncked or not
)

#Responses API print (when stream = False)
print(response.choices[0].message.content)
