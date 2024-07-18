import os
from datetime import datetime
from word_utils import extract_key_words
import gradio as gr
import configparser

#The only setting we need on creation
config = configparser.ConfigParser()
config.read('settings.cfg')
maxvalue = config['DEFAULT']['max_items']
MAX_ITEMS = int(maxvalue)


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
    if not os.path.exists(file_path):
        return "", "", "", []  # Return an empty list for items instead of a fixed-size list

    with open(file_path, 'r') as f:
        lines = f.readlines()

    if len(lines) < 3:
        return "", "", "", []

    zeroth_cue = lines[0].strip().split(': ', 1)[1] if lines[0].startswith("0th Cue: ") else ""
    first_cue = lines[1].strip().split(': ', 1)[1] if lines[1].startswith("1st Cue: ") else ""
    second_cue = lines[2].strip().split(': ', 1)[1] if lines[2].startswith("2nd Cue: ") else ""

    items_and_results = []
    current_item = ""
    current_result = ""
    reading_result = False

    for line in lines[4:]:
        if line.startswith("Item: "):
            if current_item:
                items_and_results.append((current_item, True, current_result.strip()))
                current_result = ""
            current_item = line.split(': ', 1)[1].strip()
            reading_result = False
        elif line.startswith("******"):
            reading_result = True
        elif reading_result:
            if line.startswith("Result:"):
                continue
            current_result += line

    if current_item:
        items_and_results.append((current_item, True, current_result.strip()))

    # Pad the items_and_results list to MAX_ITEMS
    items_and_results += [("", False, "") for _ in range(MAX_ITEMS - len(items_and_results))]

    # Flatten the list of tuples
    flattened_outputs = [item for tuple in items_and_results for item in tuple]

    return zeroth_cue, first_cue, second_cue, *flattened_outputs


def create_library_ui():
    with gr.Tab("Library"):
        gr.Markdown("# File Management")

        with gr.Row():
            with gr.Column():
                save_btn = gr.Button("Save Results")
                save_output = gr.File(label="Saved File")

            with gr.Column():
                open_input = gr.File(label="File to Open")
                open_btn = gr.Button("Open File", interactive=False)

        library_status_message = gr.Textbox(label="Library Status", interactive=False)

        # Enable the Open File button only when a file is selected
        open_input.change(
            lambda x: gr.update(interactive=x is not None),
            inputs=[open_input],
            outputs=[open_btn]
        )

    return save_btn, save_output, open_input, open_btn, library_status_message


def save_results_wrapper(zeroth_cue, first_cue, second_cue, *components):
    full_path = save_results(zeroth_cue, first_cue, second_cue, *components)
    return gr.update(value=full_path, visible=True), f"File saved as {os.path.basename(full_path)}"


# In file_utils.py

def open_file_wrapper(file_obj):
    total_outputs = 3 + MAX_ITEMS * 3 + 1  # 3 cues + (MAX_ITEMS * 3 components per item) + 1 status message

    if file_obj is None:
        return [gr.update()] * (total_outputs - 1) + [
            gr.update(value="Please select a file before clicking 'Open File'")]

    file_path = file_obj.name
    results = open_file(file_path)
    zeroth_cue, first_cue, second_cue = results[:3]
    item_results = results[3:]

    outputs = [
        gr.update(value=zeroth_cue),
        gr.update(value=first_cue),
        gr.update(value=second_cue)
    ]

    for i in range(MAX_ITEMS):
        if i * 3 + 2 < len(item_results):
            item_text = item_results[i * 3]
            result_text = item_results[i * 3 + 2]

            outputs.extend([
                gr.update(value=item_text, visible=True),
                gr.update(visible=True),
                gr.update(value=result_text, visible=bool(result_text))
            ])
        else:
            outputs.extend([
                gr.update(value="", visible=False),
                gr.update(visible=False),
                gr.update(value="", visible=False)
            ])

    outputs.append(gr.update(value=f"File opened: {os.path.basename(file_path)}"))

    assert len(outputs) == total_outputs, f"Expected {total_outputs} outputs, but got {len(outputs)}"

    return outputs

