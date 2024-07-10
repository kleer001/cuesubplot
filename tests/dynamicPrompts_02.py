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


def process_first_prompt(first_prompt, second_prompt):
    response = query_ollama(first_prompt)
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


def process_item(item_text, second_prompt, item_index):
    full_prompt = f"{second_prompt} {item_text}"
    response = query_ollama(full_prompt)

    return gr.update(visible=True, value=response)


with gr.Blocks() as demo:
    first_prompt = gr.Textbox(label="1st cue")
    second_prompt = gr.Textbox(label="2nd cue")
    submit_btn = gr.Button("Submit")

    item_components = []
    for i in range(MAX_ITEMS):
        with gr.Row():
            item_text = gr.Textbox(visible=False, label=f"Item {i + 1}")
            process_btn = gr.Button("Process", visible=False)
            result_text = gr.Textbox(visible=False, label=f"Result {i + 1}")
            item_components.extend([item_text, process_btn, result_text])

    submit_btn.click(
        process_first_prompt,
        inputs=[first_prompt, second_prompt],
        outputs=item_components
    )

    for i in range(MAX_ITEMS):
        item_components[i * 3 + 1].click(
            process_item,
            inputs=[item_components[i * 3], second_prompt, gr.State(i)],
            outputs=item_components[i * 3 + 2]
        )

demo.launch()
