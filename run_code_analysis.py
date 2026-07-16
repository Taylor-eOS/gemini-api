import os
import sys
import time
from google import genai
from google.genai import errors
from utils import natural_sort_key, collect_files
import settings

def analyze_file(client, input_path, output_path, filename):
    try:
        with open(input_path, "r") as f:
            code_content = f.read()
    except Exception as e:
        print(f"Error reading {filename}: {e}", file=sys.stderr, flush=True)
        return
    attempt = 0
    while True:
        try:
            chat = client.chats.create(model=settings.MODEL_NAME, config={"system_instruction": settings.CODING_INSTRUCTION, "tools": []})
            response = chat.send_message(code_content)
            cleaned_text = "\n".join([line for line in response.text.splitlines() if line.strip()])
            with open(output_path, "w") as f:
                f.write(cleaned_text)
            print(f"Saved analysis to {output_path}", flush=True)
            time.sleep(settings.DELAY_SECONDS)
            return
        except Exception as e:
            check_error(e)
            attempt += 1
            if attempt > settings.MAX_RETRIES:
                print(f"Giving up on {filename} after {attempt - 1} retries: {e}", file=sys.stderr, flush=True)
                return
            backoff = min(settings.DELAY_SECONDS * (2 ** (attempt - 1)), settings.MAX_DELAY_SECONDS)
            print(f"Error processing {filename} (attempt {attempt}/{settings.MAX_RETRIES}): {e}.\nRetrying in {backoff}s...", file=sys.stderr, flush=True)
            time.sleep(backoff)

def check_error(e):
    if isinstance(e, errors.APIError):
        if e.code == 429 or "RESOURCE_EXHAUSTED" in str(e):
            print("Quota exhausted. Quitting script.", file=sys.stderr, flush=True)
            sys.exit(1)
        if e.code == 404 or "NOT_FOUND" in str(e):
            print("Resource not found. Quitting script.", file=sys.stderr, flush=True)
            sys.exit(1)

def run_chat():
    if not os.path.exists(settings.BASE_DIR):
        print(f"Error: Base directory {settings.BASE_DIR} not found.")
        return
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Failed to initialize client: {e}")
        return
    files = collect_files()
    if not files:
        print("No files found to process.")
        return
    for input_path in files:
        filename = os.path.basename(input_path)
        output_path = os.path.join(settings.OUTPUT_DIR, f"{os.path.splitext(filename)[0]}.txt")
        if os.path.exists(output_path):
            print(f"Skipping {filename}, file already exists.")
            continue
        print(f"Processing {filename}", flush=True)
        analyze_file(client, input_path, output_path, filename)
    print("Analysis script execution finished.")

if __name__ == "__main__":
    print(f"Using {settings.MODEL_NAME}")
    run_chat()
