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
