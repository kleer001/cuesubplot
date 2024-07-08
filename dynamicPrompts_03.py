import gradio as gr
import ollama
import re
import os
from datetime import datetime

MAX_ITEMS = 5


def query_ollama(prompt):
    response = ollama.generate(model='mistral', prompt=prompt)
    return response['response']


def parse_numbered_list(text):
    pattern = r'\d+\.\s*(.*)'
    matches = re.findall(pattern, text)
    return matches[:MAX_ITEMS]  # Limit to MAX_ITEMS


def process_first_prompt(zeroth_cue, first_prompt, second_prompt):
    full_prompt = f"{zeroth_cue} {first_prompt}"
    response = query_ollama(full_prompt)
    items = parse_numbered_list(response)

    outputs = []
    for i in range(MAX_ITEMS):
        if i < len(items):
            outputs.extend([
                gr.update(visible=True, value=items[i]),  # Item text
                gr.update(visible=True),  # Process button
                gr.update(visible=False, value="")  # Result text (initially hidden)
            ])
        else:
            outputs.extend([
                gr.update(visible=False, value=""),
                gr.update(visible=False),
                gr.update(visible=False, value="")
            ])

    return outputs


def process_item(zeroth_cue, item_text, second_prompt, item_index):
    full_prompt = f"{zeroth_cue} {second_prompt} {item_text}"
    response = query_ollama(full_prompt)

    return gr.update(visible=True, value=response)


def save_results(zeroth_cue, first_cue, second_cue, *components):
    words = first_cue.split()[:4]
    base_filename = ''.join(word.capitalize() for word in words)
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{base_filename}{date_str}.txt"

    counter = 1
    while os.path.exists(filename):
        filename = f"{base_filename}{date_str}_{counter}.txt"
        counter += 1

    with open(filename, 'w') as f:
        f.write(f"0th Cue: {zeroth_cue}\n")
        f.write(f"1st Cue: {first_cue}\n")
        f.write(f"2nd Cue: {second_cue}\n\n")

        for i in range(0, len(components), 3):
            item = components[i]
            result = components[i + 2]
            if item and hasattr(item, 'value') and item.value:
                f.write(f"Item: {item.value}\n")
                if result and hasattr(result, 'value') and result.value:
                    f.write("******\n")
                    f.write(f"Result: {result.value}\n")
                f.write("\n")

    return f"Results saved to {filename}"


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


with gr.Blocks() as demo:
    zeroth_cue = gr.Textbox(label="0th cue")
    first_cue = gr.Textbox(label="1st cue")
    second_cue = gr.Textbox(label="2nd cue")
    submit_btn = gr.Button("Submit")

    item_components = []
    for i in range(MAX_ITEMS):
        with gr.Row():
            item_text = gr.Textbox(visible=False, label=f"Item {i + 1}")
            process_btn = gr.Button("Process", visible=False)
            result_text = gr.Textbox(visible=False, label=f"Result {i + 1}")
            item_components.extend([item_text, process_btn, result_text])

    save_btn = gr.Button("Save Results")
    save_output = gr.Textbox(label="Save Status")

    open_input = gr.Textbox(label="File Path to Open")
    open_btn = gr.Button("Open File")

    submit_btn.click(
        process_first_prompt,
        inputs=[zeroth_cue, first_cue, second_cue],
        outputs=item_components
    )

    for i in range(MAX_ITEMS):
        item_components[i * 3 + 1].click(
            process_item,
            inputs=[zeroth_cue, item_components[i * 3], second_cue, gr.State(i)],
            outputs=item_components[i * 3 + 2]
        )

    save_btn.click(
        save_results,
        inputs=[zeroth_cue, first_cue, second_cue] + item_components,
        outputs=save_output
    )

    open_btn.click(
        open_file,
        inputs=[open_input],
        outputs=[zeroth_cue, first_cue, second_cue] + item_components
    )

demo.launch()
