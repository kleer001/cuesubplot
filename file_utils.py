import os
from datetime import datetime
from constants import MAX_ITEMS
import gradio as gr

def generate_filename(first_cue):
    words = first_cue.split()[:4]
    base_filename = ''.join(word.capitalize() for word in words)
    date_str = datetime.now().strftime("%Y%m%d")
    return f"{base_filename}{date_str}.txt"


def save_results(zeroth_cue, first_cue, second_cue, *components):
    words = first_cue.split()[:4]
    base_filename = ''.join(word.capitalize() for word in words)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_filename}{date_str}.txt"

    counter = 1
    while os.path.exists(filename):
        filename = f"{base_filename}{date_str}_{counter}.txt"
        counter += 1

    full_path = os.path.abspath(filename)

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
                    f.write(f"Result: {result}\n")
                f.write("\n")

    return full_path

def open_file(file_path):
    if not os.path.exists(file_path):
        return "File not found", "", "", [gr.update(visible=False, value="")] * (MAX_ITEMS * 3)

    with open(file_path, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    zeroth_cue = lines[0].split(': ', 1)[1] if lines[0].startswith('0th Cue:') else ""
    first_cue = lines[1].split(': ', 1)[1] if lines[1].startswith('1st Cue:') else ""
    second_cue = lines[2].split(': ', 1)[1] if lines[2].startswith('2nd Cue:') else ""

    items_and_results = []
    current_item = ""
    current_result = ""
    for line in lines[4:]:
        if line.startswith("Item: "):
            if current_item:
                items_and_results.append((current_item, current_result))
                current_result = ""
            current_item = line.split(': ', 1)[1]
        elif line.startswith("Result: "):
            current_result = line.split(': ', 1)[1]

    if current_item:
        items_and_results.append((current_item, current_result))

    outputs = []
    for i in range(MAX_ITEMS):
        if i < len(items_and_results):
            item, result = items_and_results[i]
            outputs.extend([
                gr.update(visible=True, value=item),
                gr.update(visible=True),
                gr.update(visible=True, value=result)
            ])
        else:
            outputs.extend([
                gr.update(visible=False, value=""),
                gr.update(visible=False),
                gr.update(visible=False, value="")
            ])

    return zeroth_cue, first_cue, second_cue, *outputs

