import re
from constants import MAX_ITEMS

def parse_numbered_list(text):
    pattern = r'\d+\.\s*(.*)'
    matches = re.findall(pattern, text)
    return matches[:MAX_ITEMS]
