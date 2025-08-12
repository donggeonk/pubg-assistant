import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
# Initialize OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_response(user_input, stream):
    # Chat Completion API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system",  "content":"You are a helpful assistant to answer user's question in one sentence"}, # pointing to a LLM system prompt
            {"role":"user",    "content": user_input}, # user input  
        ],
        stream=stream # parameter to control whether the response is chucnked or not
    )

    if stream:
        return response # a list of chunks
    else:
        return response.choices[0].message.content