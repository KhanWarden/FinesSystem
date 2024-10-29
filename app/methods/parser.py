import re


def parse_value(text: str, keyword: str):
    pattern = rf"{re.escape(keyword)}:\s*([\d.,]+)"
    match = re.search(pattern, text)

    if match:
        return match.group(1)
    else:
        return None
