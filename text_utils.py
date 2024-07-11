import re


def parse_numbered_list(text, MAX_ITEMS=10):
    # Find the index of the first numbered item
    first_number_match = re.search(r'\n\d+\.?\s', text)

    if first_number_match:
        # If a numbered list is found, start from that index
        start_index = first_number_match.start()
        numbered_text = text[start_index:].strip()

        # Method 1: Match numbered items (1. Item, 2. Item, etc.)
        pattern = r'(\d+\.?\s*)(.*?)(?=\n\d+\.?\s*|\Z)'
        matches = re.findall(pattern, numbered_text, re.DOTALL)

        if matches:
            return [match[1].strip() for match in matches][:MAX_ITEMS]

    # If no numbered list is found or parsing fails, fall back to previous methods

    # Method 2: Try splitting by newlines
    lines = text.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]

    if len(non_empty_lines) > 1:
        return non_empty_lines[:MAX_ITEMS]

    # Method 3: If no newlines or only one line, return the whole text as a single item
    return [text.strip()][:MAX_ITEMS]
