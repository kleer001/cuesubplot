import re
import configparser

#The only setting we need on creation
config = configparser.ConfigParser()
config.read('settings.cfg')
maxvalue = config['DEFAULT']['max_items']
MAXITEMS = int(maxvalue)


NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
    "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
    "eleventh": 11, "twelfth": 12, "thirteenth": 13, "fourteenth": 14, "fifteenth": 15,
    "sixteenth": 16, "seventeenth": 17, "eighteenth": 18, "nineteenth": 19, "twentieth": 20
}

def parse_numbered_list(text, MAX_ITEMS=MAXITEMS):
    # Find the index of the first numbered item anywhere in the text
    first_number_match = re.search(r'\b(?:\d+\.?\s*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth)\b', text, re.IGNORECASE)

    if first_number_match:
        # If a numbered list is found, start from that index
        start_index = first_number_match.start()
        numbered_text = text[start_index:].strip()

        # Method 1: Match numbered items (1. Item, 2. Item, etc. or one. Item, two. Item, etc. or first. Item, second. Item, etc.)
        pattern = r'(?:.*?\n\n)?\b(?:\d+\.?\s*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth)\b\s*(.*?)(?=\n\b(?:\d+\.?\s*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth)\b\s*|\Z)'
        matches = re.findall(pattern, numbered_text, re.DOTALL | re.IGNORECASE)

        if matches:
            items = []
            for match in matches:
                item_text = match.strip()
                if item_text:
                    items.append(item_text)
            return items[:MAX_ITEMS]

    # If no numbered list is found or parsing fails, fall back to previous methods

    # Method 2: Try splitting by newlines
    lines = text.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]

    if len(non_empty_lines) > 1:
        return non_empty_lines[:MAX_ITEMS]

    # Method 3: If no newlines or only one line, return the whole text as a single item
    return [text.strip()][:MAX_ITEMS] if text.strip() else []
