import os
from google.genai import Client

# Initialize the client
gen_ai = Client()

def generate_text(prompt: str, model: str = "models/text-bison-001") -> str:
    """
    Generate text using Google GenAI
    """
    response = gen_ai.generate_text(
        model=model,
        prompt=prompt,
    )
    return response.text
