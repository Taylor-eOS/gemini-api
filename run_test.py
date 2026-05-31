import os
import sys
from google import genai
from google.genai import errors

def run_chat():
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not found.", file=sys.stderr)
        sys.exit(1)
    try:
        client = genai.Client()
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction": "You are an embedded educational AI robot toy. Respond with a brief answer."}
        )
        response1 = chat.send_message("How large are sharks?")
        print(response1.text)
        response2 = chat.send_message("What animal did we just talk about?")
        print(response2.text)
    except errors.APIError as e:
        print(f"API Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    run_chat()
