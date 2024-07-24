import gradio as gr
import configparser
from file_utils import open_file_wrapper, save_results_wrapper
from llm_utils import get_llm_response
from settings import create_settings_interface, load_settings, settings
from backup_utils import toggle_auto_backup, load_latest_backup

# Load configuration
config = configparser.ConfigParser()
config.read('settings.cfg')
MAX_ITEMS = int(config['DEFAULT']['max_items'])
load_settings()  # Load settings before creating the Gradio interface


def get_current_data():
    data = {
        "zeroth_cue": zeroth_cue.value,
        "first_cue": first_cue.value,
        "second_cue": second_cue.value,
        "items": []
    }

    for i in range(0, len(item_components), 4):
        item = item_components[i + 1]  # The item textbox
        result = item_components[i + 3]  # The result textbox
        if item.visible:
            data["items"].append({
                "Item": item.value if item.value is not None else "",
                "Result": result.value if result.value is not None else ""
            })

    return data


def initialize_backup():
    try:
        if settings["auto_load_backup"]:
            backup_data = load_latest_backup()
            if backup_data:
                return load_backup_data(backup_data)
    except Exception as e:
        print(f"Error initializing backup: {e}")

    return [gr.update()] * (3 + settings['max_items'] * 4)


def load_backup_data(data):
    updates = []
    try:
        updates = [
            gr.update(value=data.get("zeroth_cue", "")),
            gr.update(value=data.get("first_cue", "")),
            gr.update(value=data.get("second_cue", ""))
        ]

        items = data.get("items", [])
        for i in range(MAX_ITEMS):
            # Update for Row (visibility)
            updates.append(gr.update(visible=i < len(items)))

            # Update for Item Textbox
            if i < len(items):
                updates.append(gr.update(value=items[i]["Item"], visible=True))
            else:
                updates.append(gr.update(value="", visible=False))

            # Update for Button (visibility)
            updates.append(gr.update(visible=i < len(items)))

            # Update for Result Textbox
            if i < len(items):
                updates.append(gr.update(value=items[i].get("Result", ""), visible=True))
            else:
                updates.append(gr.update(value="", visible=False))
    except Exception as e:
        print(f"Error loading backup data: {e}")
        updates = [gr.update()] * (3 + MAX_ITEMS * 4)

    return updates


def process_item(zeroth_cue, item_text, second_prompt, item_index):
    full_prompt = f"{zeroth_cue} {second_prompt} {item_text}"
    response = get_llm_response(full_prompt)
    return gr.update(visible=True, value=response)


def clear_stage():
    outputs = [gr.update(value="") for _ in range(3)]  # zeroth_cue, first_cue, second_cue
    for _ in range(MAX_ITEMS):
        outputs.extend([
            gr.update(visible=False),  # Row
            gr.update(value="", visible=False),  # Item text
            gr.update(visible=False),  # Process button
            gr.update(value="", visible=False)  # Result text
        ])
    return outputs + [gr.update(value="Stage cleared")]  # Status message


def process_first_prompt(zeroth, first, second):
    items = get_llm_response(f"{zeroth} {first}").split('\n')
    outputs = []
    for i, item_text in enumerate(items[:MAX_ITEMS]):
        has_content = bool(item_text.strip())
        outputs.extend([
            gr.update(visible=has_content),  # Row
            gr.update(value=item_text, visible=has_content),  # Item
            gr.update(visible=has_content),  # Process button
            gr.update(visible=False, value="")  # Result
        ])
    # Hide remaining slots
    for _ in range(MAX_ITEMS - len(items)):
        outputs.extend([gr.update(visible=False) for _ in range(4)])  # Row, Item, Button, Result
    outputs.append("Items generated")  # Status message
    return outputs


with gr.Blocks(title="cuesubplot") as demo:
    with gr.Tab("Stage"):
        zeroth_cue = gr.Textbox(label="Role (applied to all prompts)", lines=1)
        first_cue = gr.Textbox(label="List generation (ask for a numbered list)", lines=1)
        second_cue = gr.Textbox(label="Riff on the list (is applied before the list item)", lines=1)
        submit_btn = gr.Button("Submit Request for List")
        status_message = gr.Textbox(label="Status", interactive=False)

        item_components = []
        for i in range(MAX_ITEMS):
            with gr.Row(visible=False) as item_row:
                item = gr.Textbox(label=f"List Item {i + 1}", visible=False, lines=1)
                process_btn = gr.Button(f"Riff On List Item {i + 1}", visible=False)
            result = gr.Textbox(label=f"Riffing Result {i + 1}", visible=False, lines=1)
            item_components.extend([item_row, item, process_btn, result])

        submit_btn.click(
            process_first_prompt,
            inputs=[zeroth_cue, first_cue, second_cue],
            outputs=item_components + [status_message]
        )

        for i in range(MAX_ITEMS):
            process_btn = item_components[i * 4 + 2]
            process_btn.click(
                process_item,
                inputs=[zeroth_cue, item_components[i * 4 + 1], second_cue, gr.State(i)],
                outputs=[item_components[i * 4 + 3]]
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
            inputs=[zeroth_cue, first_cue, second_cue] + [comp for comp in item_components if
                                                          isinstance(comp, gr.Textbox)],
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
            outputs=[zeroth_cue, first_cue, second_cue] + [comp for comp in item_components if
                                                           isinstance(comp, gr.Textbox)] + [library_status_message]
        )

    with gr.Tab("Settings"):
        create_settings_interface()

    with gr.Tab("Backup"):
        backup_status = gr.Textbox(label="Backup Status", interactive=False)
        backup_button = gr.Button("Toggle Auto-backup")
        backup_button.click(lambda: toggle_auto_backup(get_current_data, settings["auto_backup_interval"]), outputs=backup_status)

        # Load the latest backup when the app starts
        demo.load(initialize_backup, outputs=[zeroth_cue, first_cue, second_cue] + item_components)

    if __name__ == "__main__":
        demo.launch()