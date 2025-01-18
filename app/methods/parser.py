import re
from datetime import datetime


def parse_value(text: str, keyword: str):
    pattern = rf"{re.escape(keyword)}:\s*([\d.,]+)"
    match = re.search(pattern, text)

    if match:
        return match.group(1)
    else:
        return None


def is_valid_date(date_string: str) -> bool:
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_only_digits(data):
    try:
        pattern = r'^\d+$'
        return bool(re.fullmatch(pattern, data))
    except ValueError:
        return False
