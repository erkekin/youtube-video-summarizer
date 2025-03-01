import base64
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def generate(input_text):
    # Load environment variables from .env file
    load_dotenv()
    
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-pro-exp-02-05"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=input_text,
                ),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=64,
        max_output_tokens=8192,
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_CIVIC_INTEGRITY",
                threshold="BLOCK_LOW_AND_ABOVE", # Block most
            ),
        ],
        response_mime_type="text/plain",
    )

    # Collect the entire response instead of printing
    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text
        
    return response_text

# Only run standalone if called directly
if __name__ == "__main__":
    print(generate("PUT RESPONSE TEXT HERE"))