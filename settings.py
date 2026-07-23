import os

STARTING_STRING = "input"
matching_dirs = [d for d in os.listdir(".") if os.path.isdir(d) and d.startswith(STARTING_STRING)]
if len(matching_dirs) == 0:
    raise FileNotFoundError(f"No folder starting with {STARTING_STRING} found")
if len(matching_dirs) > 1:
    raise FileNotFoundError(f"Multiple folders starting with {STARTING_STRING} found")
BASE_DIR = matching_dirs[0]
IDENTIFIER = BASE_DIR.split("_", 1)[1] if "_" in BASE_DIR else BASE_DIR
OUTPUT_DIR = "analyzed_" + IDENTIFIER

MODEL_NAMES = ["gemini-3.5-flash", "gemini-3.1-flash-lite"]
DELAY_SECONDS = 8
MAX_RETRIES = 10
MAX_DELAY_SECONDS = 600
CODING_INSTRUCTION = "This is a decompilers C-style reconstruction of a function from the executable of the video game Rome Total War. Describe this functions apparent purpose and role within the games systems. State only what is directly supported by code and data structures, but include high confidence inferences where appropriate. The description should attempt to be on the level of broader holistic purposerather than particular implementation detail. Return the response as a JSON object with exactly these fields: \"name\": a suggestion for a descriptive flatcase name to append to the generated function name. \"purpose\": a documentation annotation describing the functions apparent conceptual responsibility, the game concepts it operates on, what role it most likely serves within the games logic, and any high confidence inferences that would help distinguish it from other functions in the game. Prefer including useful context over brevity. Do not describe implementation details unless they are necessary to explain the conceptual role. Focus on what matters to the player, not the algorithmic details. \"domain\": the primary game system or engine domain this function belongs to. This should be a categorization into subsystems by which functions can later be sorted. \"keywords\": a comprehensive list of search terms that someone reverse engineering the game might later search for, including game concepts, mechanics, entities, systems, and closely related concepts. Include plausible synonyms where supported by the code. Do not overly focus on implementation terminology. \"modding_relevant\": a boolean that is true only if this function appears to define, compute, or directly apply a game mechanic that a reverse engineer would likely modify to intentionally change gameplay. Return false for wrappers, accessors, dispatchers, lookups, validation, state management, scripting infrastructure, rendering, UI, or other supporting functions, even if they participate in gameplay. Modders care about application of in-game effects or healing casualties calculations, not assert plumbing. \"modding_explanation\": Explanation of the choice of the `modding` value. \"arguments\": As far as possible to infer from this stripped code, provide a segment on what data the function handles and what arguments it passes on to the functions it calls or what data they contain. This information is meant to later be included in the context when generating these functions annotations, so it can be known what data they received. This is difficult to say with stripped code, so state what is known at this time. Provide this in one combined element.\n Output a JSON object with no surrounding text, code fence, backticks, or headers."
