import os
from datetime import datetime
from constants import MAX_ITEMS
from ollama_utils import extract_key_words
import gradio as gr
from word_utils import extract_key_words

def generate_filename(zeroth_cue, first_cue):
    key_words = extract_key_words(zeroth_cue)

    # If we don't have enough key words, fall back to using words from the first cue
    if len(key_words) < 4:
        first_cue_words = extract_key_words(first_cue, num_words=4 - len(key_words))
        key_words.extend(first_cue_words)

    base_filename = ''.join(word.capitalize() for word in key_words[:4])
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_filename}{date_str}.txt"


def save_results(zeroth_cue, first_cue, second_cue, *components):
    # Create the 'saved_cues' directory if it doesn't exist
    save_dir = os.path.join(os.getcwd(), 'saved_cues')
    os.makedirs(save_dir, exist_ok=True)

    filename = generate_filename(zeroth_cue, first_cue)

    counter = 1
    while os.path.exists(os.path.join(save_dir, filename)):
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{counter}{ext}"
        counter += 1

    full_path = os.path.join(save_dir, filename)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(f"0th Cue: {zeroth_cue}\n")
        f.write(f"1st Cue: {first_cue}\n")
        f.write(f"2nd Cue: {second_cue}\n\n")

        for i in range(0, len(components), 2):
            item = components[i]
            result = components[i + 1] if i + 1 < len(components) else None

            if item:  # If item has a value, save it
                f.write(f"Item: {item}\n")
                if result:  # If result has a value, save it
                    f.write("******\n")
                    f.write(f"Result:\n{result}\n")  # Write 'Result:' on its own line
                f.write("\n")  # Extra newline for separation

    return full_path



def open_file(file_path):
    # Check if the file_path is just a filename or a full path
    if not os.path.dirname(file_path):
        # If it's just a filename, assume it's in the 'saved_cues' directory
        file_path = os.path.join(os.getcwd(), 'saved_cues', file_path)

    if not os.path.exists(file_path):
        return "File not found", "", "", *[("", False, "") for _ in range(MAX_ITEMS)]

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    zeroth_cue = lines[0].split(': ', 1)[1] if lines[0].startswith('0th Cue:') else ""
    first_cue = lines[1].split(': ', 1)[1] if lines[1].startswith('1st Cue:') else ""
    second_cue = lines[2].split(': ', 1)[1] if lines[2].startswith('2nd Cue:') else ""

    items_and_results = []
    current_item = ""
    current_result = ""
    reading_result = False

    for line in lines[4:]:
        if line.startswith("Item: "):
            if current_item:
                items_and_results.append((current_item, True, current_result.strip()))
                current_result = ""
            current_item = line.split(': ', 1)[1]
            reading_result = False
        elif line.startswith("******"):
            reading_result = True
        elif reading_result:
            if line.startswith("Result:"):
                continue  # Skip the "Result:" line
            current_result += line + "\n"

    if current_item:
        items_and_results.append((current_item, True, current_result.strip()))

    # Pad the items_and_results list to MAX_ITEMS
    items_and_results += [("", False, "") for _ in range(MAX_ITEMS - len(items_and_results))]

    # Flatten the list of tuples
    flattened_outputs = [item for tuple in items_and_results for item in tuple]

    return zeroth_cue, first_cue, second_cue, *flattened_outputs


