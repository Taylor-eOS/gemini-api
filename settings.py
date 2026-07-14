API_KEY = "your_api_key"
BASE_DIR = "input"
OUTPUT_DIR = BASE_DIR + "_analyzed"
MODEL_NAME = "gemini-3.1-flash-lite" #gemini-3.5-flash, gemini-3.1-flash-lite, gemini-2.5-flash, gemma-4-31b-it
DELAY_SECONDS = 10
MAX_RETRIES = 10
MAX_DELAY_SECONDS = 600
CODING_INSTRUCTION = "This is a functin of decompiled C code from a video game. Describe this functions specific role in the games internal logic based strictly on the behavior visible in the code. Support each claim with specific evidence from the code such as function calls, string literals, or data operations. Do not infer details that are not supported by the code. If the functions purpose cannot be determined with confidence, say so. State the functions purpose in a few plain, unformatted sentences. State which subsystem the function most likely belongs to."
