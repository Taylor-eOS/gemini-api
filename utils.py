import os
from settings import BASE_DIR

def collect_files():
    files = []
    for item in os.listdir(BASE_DIR):
        full_path = os.path.join(BASE_DIR, item)
        if os.path.isfile(full_path):
            files.append(full_path)
    files.sort(key=natural_sort_key)
    return files

def natural_sort_key(s):
    key = []
    part = ""
    is_numeric = False
    for char in s:
        char_is_digit = char.isdigit()
        if char_is_digit != is_numeric:
            if part:
                key.append(int(part) if is_numeric else part.lower())
            part = char
            is_numeric = char_is_digit
        else:
            part += char
    if part:
        key.append(int(part) if is_numeric else part.lower())
    return key

def strip_code_fence(text):
    lines = [line for line in text.splitlines() if line.strip()]
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)
