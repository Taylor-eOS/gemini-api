API_KEY = "your_api_key"
BASE_DIR = "input_folder"
OUTPUT_DIR = "rome_functions_analyzed"
MODEL_NAME = "gemini-3.5-flash" #gemini-3.1-flash-lite, gemini-3.5-flash, gemini-2.5-flash, gemma-4-31b-it
DELAY_SECONDS = 10
MAX_RETRIES = 10
MAX_DELAY_SECONDS = 640
CODING_INSTRUCTION = "Instruction: Describe this function's specific role in the internal logic by identifying the unique operation it performs, based strictly on the concrete behavior visible in the code. Do not invent details not directly supported by the code. State the functions distinct purpose in one plain sentence, unformatted, no headers. Briefly state which major subsystem it most likely belongs to (e.g. menu, memory housekeeping). Write without headers or repetitive descriptors. Finally suggest a flatcase name appendage for the function to distinguish it from others, that mainly highlights its belonging, not specific functionality."
