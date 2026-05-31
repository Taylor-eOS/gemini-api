import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import errors

def generate_text():
    load_dotenv()
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not found.", file=sys.stderr)
        sys.exit(1)
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Respond with a brief cute sentence as if you were a embedded AI robot toy for which this API is used to generate responses.",
        )
        print(response.text)
    except errors.APIError as e:
        print(f"API Error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    generate_text()
