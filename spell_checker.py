from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
load_dotenv()

client = OpenAI(
    api_key=getenv('GORK_API'),
    base_url="https://api.groq.com/openai/v1",
)

def spell_checker(sentence):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"Correct the spelling. Return only corrected text. It could be a movie title, director, genre, or actor name: {sentence}"
            }
        ]
    )

    return response.choices[0].message.content.strip()