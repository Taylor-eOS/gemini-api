import os
import sys
import time
from google import genai
from google.genai import errors
import settings

def collect_files():
    files = []
    for root, _, filenames in os.walk(settings.BASE_DIR):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    files.sort()
    return files

def analyze_file(client, input_path, output_path, relative_path):
    try:
        with open(input_path, "r") as f:
            code_content = f.read()
    except Exception as e:
        print(f"Error reading {relative_path}: {e}", file=sys.stderr, flush=True)
        return
    attempt = 0
    while True:
        try:
            chat = client.chats.create(model=settings.MODEL_NAME, config={"system_instruction": settings.CODING_INSTRUCTION})
            response = chat.send_message(code_content)
            with open(output_path, "w") as f:
                f.write(response.text)
            print(f"Saved analysis to {output_path}", flush=True)
            time.sleep(settings.DELAY_SECONDS)
            return
        except Exception as e:
            attempt += 1
            if attempt > settings.MAX_RETRIES:
                print(f"Giving up on {relative_path} after {attempt - 1} retries: {e}", file=sys.stderr, flush=True)
                return
            backoff = min(settings.DELAY_SECONDS * (2 ** (attempt - 1)), settings.MAX_DELAY_SECONDS)
            print(f"Error processing {relative_path} (attempt {attempt}/{settings.MAX_RETRIES}): {e}. Retrying in {backoff}s...", file=sys.stderr, flush=True)
            time.sleep(backoff)

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
        relative_path = os.path.relpath(input_path, settings.BASE_DIR)
        flat_name = relative_path.replace(os.sep, "_")
        output_path = os.path.join(settings.OUTPUT_DIR, f"{os.path.splitext(flat_name)[0]}.txt")
        if os.path.exists(output_path):
            print(f"Skipping {relative_path}, file already exists.")
            continue
        print(f"Processing {relative_path}.", flush=True)
        analyze_file(client, input_path, output_path, relative_path)
    print("Analysis script execution finished.")

if __name__ == "__main__":
    run_chat()
