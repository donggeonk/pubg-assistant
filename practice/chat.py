import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
# Initialize OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_response(user_input, stream):
    #Chatbot Completion API
    response = client.chat.completions.create(
    model = "gpt-4o",
    messages = [
        {"role": "system", "content": "You are a helpful assistant to answer user's question concicsely"}, #Instruction
        {"role": "user", "content": user_input}, #User input
        ],
    stream = stream #Parameter to control whether the response is chuncked or not
    )

    if stream:
        return response #a list of chunks
    else:
        return response.choices[0].message.content