import gradio as gr
import time
from ollama_utils import query_ollama
from file_utils import save_results, open_file
from text_utils import parse_numbered_list
from constants import MAX_ITEMS
import settings


def process_first_prompt(zeroth_cue, first_prompt, second_prompt, progress=gr.Progress()):
    full_prompt = f"{zeroth_cue} {first_prompt}"

    progress(0, desc="Preparing...")
    time.sleep(0.5)

    progress(0.2, desc="Sending request to Ollama...")
    response = query_ollama(full_prompt)

    progress(0.6, desc="Processing response...")
    time.sleep(0.5)

    items = parse_numbered_list(response)

    progress(0.8, desc="Preparing output...")
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

    progress(1.0, desc="Done!")
    return outputs + [gr.update(value="Processing complete!")]


def process_item(zeroth_cue, item_text, second_prompt, item_index):
    full_prompt = f"{zeroth_cue} {second_prompt} {item_text}"
    response = query_ollama(full_prompt)
    return gr.update(visible=True, value=response)


def reset_interface():
    return [gr.update(visible=False, value="")] * (MAX_ITEMS * 3) + [gr.update(value="")]


with gr.Blocks() as demo:
    with gr.Tab("stage"):
        zeroth_cue = gr.Textbox(label="0th cue")
        first_cue = gr.Textbox(label="1st cue")
        second_cue = gr.Textbox(label="2nd cue")
        submit_btn = gr.Button("Submit")

        status_message = gr.Textbox(label="Status", interactive=False)

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
            reset_interface,
            outputs=item_components + [status_message]
        ).then(
            process_first_prompt,
            inputs=[zeroth_cue, first_cue, second_cue],
            outputs=item_components + [status_message],
            show_progress=True
        )

        for i in range(MAX_ITEMS):
            item_components[i * 3 + 1].click(
                process_item,
                inputs=[zeroth_cue, item_components[i * 3], second_cue, gr.State(i)],
                outputs=item_components[i * 3 + 2]
            )

        save_btn.click(
            save_results,
            inputs=[zeroth_cue, first_cue, second_cue] + [comp for comp in item_components if
                                                          isinstance(comp, gr.Textbox)],
            outputs=save_output
        )

        open_btn.click(
            open_file,
            inputs=[open_input],
            outputs=[zeroth_cue, first_cue, second_cue] + item_components
        )

    with gr.Tab("settings"):
        settings.create_settings_interface()

if __name__ == "__main__":
    demo.launch()
