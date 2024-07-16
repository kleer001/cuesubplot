import re
import configparser

#The only setting we need on creation
config = configparser.ConfigParser()
config.read('settings.cfg')
maxvalue = config['DEFAULT']['max_items']
MAXITEMS = int(maxvalue)

import re


def generate_number_words():
    units = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
             "nineteen"]
    tens = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    scales = ["hundred", "thousand"]

    ordinal_units = ["", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth"]
    ordinal_teens = ["tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth",
                     "seventeenth", "eighteenth", "nineteenth"]
    ordinal_tens = ["twentieth", "thirtieth", "fortieth", "fiftieth", "sixtieth", "seventieth", "eightieth",
                    "ninetieth"]

    number_words = {}

    # Add cardinal numbers
    for i, word in enumerate(units[1:] + teens):
        number_words[word] = i + 1

    for i, ten in enumerate(tens):
        number_words[ten] = (i + 2) * 10

    # Add ordinal numbers
    for i, word in enumerate(ordinal_units[1:] + ordinal_teens):
        number_words[word] = i + 1

    for i, ten in enumerate(ordinal_tens):
        number_words[ten] = (i + 2) * 10

    # Add compounds (twenty-one to ninety-nine, and twenty-first to ninety-ninth)
    for i, ten in enumerate(tens):
        for j, unit in enumerate(units[1:]):
            cardinal = f"{ten}-{unit}"
            ordinal = f"{ten}-{ordinal_units[j + 1]}"
            number_words[cardinal] = (i + 2) * 10 + (j + 1)
            number_words[ordinal] = (i + 2) * 10 + (j + 1)

    # Add scales
    for i, scale in enumerate(scales):
        number_words[scale] = 10 ** ((i + 1) * 2)
        number_words[f"{scale}th"] = 10 ** ((i + 1) * 2)

    return number_words


NUMBER_WORDS = generate_number_words()

def parse_numbered_list(text, MAX_ITEMS=20):
    number_words = '|'.join(NUMBER_WORDS.keys())
    number_pattern = rf'\b(?:\d+\.?\s*|{number_words})\b'

    first_number_match = re.search(number_pattern, text, re.IGNORECASE)

    if first_number_match:
        start_index = first_number_match.start()
        numbered_text = text[start_index:]

        pattern = rf'(?:.*?\n\n)?{number_pattern}\s*(.*?)(?=\n{number_pattern}|\Z)'
        matches = re.findall(pattern, numbered_text, re.DOTALL | re.IGNORECASE)

        items = [match.strip() for match in matches if match.strip()]
        return items[:MAX_ITEMS]

    # Fallback methods
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    if len(lines) > 1:
        return lines[:MAX_ITEMS]

    return [text.strip()][:MAX_ITEMS] if text.strip() else []

