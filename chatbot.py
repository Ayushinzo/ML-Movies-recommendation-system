from dotenv import load_dotenv
from os import getenv
from openai import OpenAI
load_dotenv()

client = OpenAI(
    api_key=getenv('GORK_API'),
    base_url="https://api.groq.com/openai/v1",
)

def chatbot(messages):
    system_message = {
        "role": "system",
        "content": """
        You are a movie chatbot. Give helpful, concise answers about movies,
        actors, directors, genres, story themes, and recommendations.
        Avoid major spoilers unless the user asks.
        """
    }
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[system_message] + messages
    )
    reply = response.choices[0].message.content.strip()
    return reply