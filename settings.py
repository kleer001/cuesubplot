import gradio as gr
import ollama
import os

# Default settings
current_model = None
messy = False
MAX_ITEMS = 5  # Default value


def load_settings():
    global current_model, messy, MAX_ITEMS
    if os.path.exists("settings.cfg"):
        with open("settings.cfg", "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("current_model"):
                    current_model = line.split("=")[1].strip()
                elif line.startswith("messy"):
                    messy = line.split("=")[1].strip().lower() == "true"
                elif line.startswith("max_items"):
                    MAX_ITEMS = int(line.split("=")[1].strip())
    else:
        save_settings()


def save_settings():
    with open("settings.cfg", "w") as f:
        f.write("# Ollama model being used\n")
        f.write(f"current_model={current_model}\n")
        f.write("# Visibility of items, results, and process boxes\n")
        f.write(f"messy={messy}\n")
        f.write("# Maximum number of items\n")
        f.write(f"max_items={MAX_ITEMS}\n")


def update_max_items(value):
    global MAX_ITEMS
    MAX_ITEMS = value
    save_settings()
    return f"MAX_ITEMS updated to {value}. Please refresh your browser for the changes to take effect."


def create_settings_interface():
    global current_model, messy

    # Get the list of models
    models = ollama.list()
    if isinstance(models, dict) and 'models' in models:
        model_names = [model['name'] for model in models['models']]
    else:
        model_names = models  # Assuming it's already a list of model names

    if not model_names:
        model_names = ["No models found"]

    current_model = model_names[0] if current_model is None else current_model
    if current_model not in model_names:
        current_model = model_names[0]

    model_dropdown = gr.Dropdown(choices=model_names, value=current_model, label="Ollama Model")
    messy_switch = gr.Checkbox(value=messy, label="Messy")
    max_items_input = gr.Number(value=MAX_ITEMS, label="Maximum number of items", precision=0)

    gr.Markdown("""
    **Note:** Changes to MAX_ITEMS will require a browser refresh to take effect on the UI layout.
    """)

    def update_settings(model, messy_value, max_items):
        global current_model, messy
        current_model = model
        messy = messy_value
        max_items_status = update_max_items(max_items)
        save_settings()
        return f"Settings updated. {max_items_status}"

    update_button = gr.Button("Update Settings")
    update_output = gr.Textbox(label="Update Status")

    update_button.click(
        update_settings,
        inputs=[model_dropdown, messy_switch, max_items_input],
        outputs=update_output
    )


# Load settings on module import
load_settings()

if __name__ == "__main__":
    with gr.Blocks() as demo:
        create_settings_interface()
    demo.launch()
