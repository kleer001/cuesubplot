import gradio as gr
import ollama
import os

# Default settings
current_model = None
messy = False

def load_settings():
    global current_model, messy
    if os.path.exists("settings.cfg"):
        with open("settings.cfg", "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("current_model"):
                    current_model = line.split("=")[1].strip()
                elif line.startswith("messy"):
                    messy = line.split("=")[1].strip().lower() == "true"
    else:
        save_settings()

def save_settings():
    with open("settings.cfg", "w") as f:
        f.write("# Ollama model being used\n")
        f.write(f"current_model={current_model}\n")
        f.write("# Visibility of items, results, and process boxes\n")
        f.write(f"messy={messy}\n")

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

    def update_settings(model, messy_value):
        global current_model, messy
        current_model = model
        messy = messy_value
        save_settings()
        return "Settings updated"

    update_button = gr.Button("Update Settings")
    update_output = gr.Textbox(label="Update Status")

    update_button.click(update_settings, inputs=[model_dropdown, messy_switch], outputs=update_output)

# Load settings on module import
load_settings()
