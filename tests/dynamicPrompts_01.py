import gradio as gr
import ollama
import re

MAX_ITEMS = 5
MAX_LEVELS = 3


def query_ollama(prompt):
    response = ollama.generate(model='mistral', prompt=prompt)
    return response['response']


def parse_numbered_list(text):
    pattern = r'\d+\.\s*(.*)'
    matches = re.findall(pattern, text)
    return matches[:MAX_ITEMS]  # Limit to MAX_ITEMS


def process_prompt(prompt, level, *previous_levels):
    response = query_ollama(prompt)
    items = parse_numbered_list(response)

    outputs = []
    for i in range(MAX_ITEMS * MAX_LEVELS * 4):
        outputs.append(gr.update(visible=False))

    for i, item in enumerate(items):
        base_index = level * MAX_ITEMS * 4 + i * 4
        outputs[base_index] = gr.update(visible=True, value=f"Level {level}, Item {i + 1}")  # Header
        outputs[base_index + 1] = gr.update(visible=True, value=item)  # Item text
        outputs[base_index + 2] = gr.update(visible=True, value="")  # Follow-up prompt
        outputs[base_index + 3] = gr.update(visible=True)  # Process button

    return outputs


with gr.Blocks() as demo:
    initial_prompt = gr.Textbox(label="Initial Prompt")
    submit_btn = gr.Button("Submit")

    all_components = []
    for level in range(MAX_LEVELS):
        for item in range(MAX_ITEMS):
            all_components.extend([
                gr.Text(visible=False),  # Header
                gr.Textbox(visible=False),  # Item text
                gr.Textbox(visible=False),  # Follow-up prompt
                gr.Button("Process", visible=False)  # Process button
            ])

    submit_btn.click(
        process_prompt,
        inputs=[initial_prompt, gr.State(0)] + all_components,
        outputs=all_components
    )

    for level in range(MAX_LEVELS):
        for item in range(MAX_ITEMS):
            base_index = level * MAX_ITEMS * 4 + item * 4
            all_components[base_index + 3].click(
                process_prompt,
                inputs=[all_components[base_index + 2], gr.State(level + 1)] + all_components,
                outputs=all_components
            )

demo.launch()
