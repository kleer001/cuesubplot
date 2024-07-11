import gradio as gr
from file_utils import open_file_wrapper, save_results_wrapper
from ollama_utils import query_ollama
from settings import MAX_ITEMS, create_settings_interface


def process_item(zeroth_cue, item_text, second_prompt, item_index):
    full_prompt = f"{zeroth_cue} {second_prompt} {item_text}"
    response = query_ollama(full_prompt)
    return gr.update(visible=True, value=response)


def clear_stage():
    outputs = [
        gr.update(value=""),  # zeroth_cue
        gr.update(value=""),  # first_cue
        gr.update(value="")  # second_cue
    ]
    for _ in range(MAX_ITEMS):
        outputs.extend([
            gr.update(visible=False),  # Row
            gr.update(value="", visible=False),  # Item text
            gr.update(visible=False),  # Process button
            gr.update(value="", visible=False)  # Result text
        ])
    return outputs + [gr.update(value="Stage cleared")]  # Status message


with gr.Blocks(title="cuesubplot") as demo:
    with gr.Tab("Stage"):
        zeroth_cue = gr.Textbox(label="0th Cue")
        first_cue = gr.Textbox(label="1st Cue")
        second_cue = gr.Textbox(label="2nd Cue")
        submit_btn = gr.Button("Submit")

        status_message = gr.Textbox(label="Status", interactive=False)

        item_components = []
        for i in range(MAX_ITEMS):
            with gr.Row(visible=False) as item_row:
                process_btn = gr.Button(f"Process {i + 1}", visible=False)
                item = gr.Textbox(label=f"Item {i + 1}", visible=False)
            result = gr.Textbox(label=f"Result {i + 1}", visible=False)
            item_components.extend([item_row, item, process_btn, result])


        def process_first_prompt(zeroth, first, second):
            items = query_ollama(f"{zeroth} {first}")
            item_list = items.split('\n')
            outputs = []
            for i, item_text in enumerate(item_list[:MAX_ITEMS]):
                outputs.extend([
                    gr.update(visible=True),  # For the Row
                    gr.update(value=item_text, visible=True),  # For the Item
                    gr.update(visible=True),  # For the Process button
                    gr.update(visible=True, value="")  # For the Result
                ])
            # Fill remaining slots with hidden components
            for _ in range(MAX_ITEMS - len(item_list)):
                outputs.extend([gr.update(visible=False)] * 4)
            outputs.append("Items generated")  # Status message
            return outputs


        submit_btn.click(
            process_first_prompt,
            inputs=[zeroth_cue, first_cue, second_cue],
            outputs=item_components + [status_message]
        )

        for i in range(MAX_ITEMS):
            process_btn = item_components[i * 4 + 2]  # The process button is the third component in each group
            process_btn.click(
                process_item,
                inputs=[zeroth_cue, item_components[i * 4 + 1], second_cue, gr.State(i)],
                outputs=[item_components[i * 4 + 3]]  # The result textbox
            )

    with gr.Tab("Library"):
        gr.Markdown("# File Management")

        with gr.Row():
            with gr.Column():
                save_btn = gr.Button("Save Results")
                save_output = gr.File(label="Saved File")

            with gr.Column():
                open_input = gr.File(label="File to Open")
                open_btn = gr.Button("Open File")

        with gr.Row():
            clear_btn = gr.Button("Clear Stage")

        library_status_message = gr.Textbox(label="Library Status", interactive=False)

        save_btn.click(
            save_results_wrapper,
            inputs=[zeroth_cue, first_cue, second_cue] + item_components,
            outputs=[save_output, library_status_message]
        )

        open_btn.click(
            open_file_wrapper,
            inputs=[open_input],
            outputs=[zeroth_cue, first_cue, second_cue] + item_components + [library_status_message]
        )

        clear_btn.click(
            clear_stage,
            inputs=[],
            outputs=[zeroth_cue, first_cue, second_cue] + item_components + [library_status_message]
        )

    with gr.Tab("Settings"):
        create_settings_interface()

if __name__ == "__main__":
    demo.launch()
