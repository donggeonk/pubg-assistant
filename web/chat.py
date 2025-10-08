import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def bot_response(prompt):
    """
    Function to get a response from the OpenAI API.
    """
    # Chat Completion
    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that replies in one sentence."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

