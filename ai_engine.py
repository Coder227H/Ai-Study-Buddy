
from google import genai

client = genai.Client()

def generate_response(prompt):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    return response.text
