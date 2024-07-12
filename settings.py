import gradio as gr
import os
import configparser
from findLLM import find_local_LLM
from llm_models import get_models

# Global settings
settings = {}
active_llm = find_local_LLM()

def update_max_items(value):
    global MAX_ITEMS
    MAX_ITEMS = value
    save_settings()
    return f"MAX_ITEMS updated to {value}. Please refresh your browser for the changes to take effect."

def load_settings():
    global settings, active_llm
    config = configparser.ConfigParser()
    if os.path.exists("settings.cfg"):
        config.read("settings.cfg")
    else:
        # Create a default settings file if it doesn't exist
        config["DEFAULT"] = {
            "active_llm": active_llm or "Unknown",
            "current_model": "",
            "messy": "False",
            "max_items": "5"
        }
        with open("settings.cfg", "w") as configfile:
            config.write(configfile)

    # Load general settings
    settings = dict(config["DEFAULT"])

    # Load LLM-specific settings
    if active_llm and active_llm in config:
        settings.update(dict(config[active_llm]))

    # Convert types
    settings["messy"] = settings.get("messy", "False").lower() == "true"
    settings["max_items"] = int(settings.get("max_items", "5"))


def save_settings():
    config = configparser.ConfigParser()
    config.read("settings.cfg")

    # Update general settings
    if "DEFAULT" not in config:
        config["DEFAULT"] = {}
    config["DEFAULT"].update({
        "active_llm": active_llm,
        "current_model": settings.get("current_model", ""),
        "messy": str(settings.get("messy", False)),
        "max_items": str(settings.get("max_items", 5))
    })

    # Update LLM-specific settings
    if active_llm:
        if active_llm not in config:
            config[active_llm] = {}
        for key, value in settings.items():
            if key not in ["active_llm", "current_model", "messy", "max_items"]:
                config[active_llm][key] = str(value)

    with open("settings.cfg", "w") as configfile:
        config.write(configfile)


def create_settings_interface():
    gr.Markdown(f"## Settings for {active_llm}")

    input_components = []

    # General settings
    input_components.append(gr.Dropdown(choices=get_models(active_llm), value=settings.get("current_model", ""), label="Model"))
    input_components.append(gr.Checkbox(value=settings.get("messy", False), label="Messy"))
    input_components.append(gr.Number(value=settings.get("max_items", 5), label="Maximum number of items", precision=0))

    # Ollama-specific settings
    input_components.append(gr.Textbox(value=settings.get("model", ""), label="Ollama Model"))
    input_components.append(gr.Number(value=settings.get("max_tokens", 100), label="Max Tokens"))
    input_components.append(gr.Slider(minimum=0, maximum=1, value=settings.get("temperature", 0.7), label="Temperature"))
    input_components.append(gr.Checkbox(value=settings.get("stream", False), label="Stream"))

    gr.Markdown("""
    **Note:** Changes to MAX_ITEMS will require a browser refresh to take effect on the UI layout.
    """)

    def update_settings(current_model, messy, max_items, ollama_model, max_tokens, temperature, stream):
        settings.update({
            "current_model": current_model,
            "messy": messy,
            "max_items": int(max_items),
            "model": ollama_model,
            "max_tokens": int(max_tokens),
            "temperature": float(temperature),
            "stream": stream
        })
        save_settings()
        return f"Settings updated. MAX_ITEMS is now {settings['max_items']}. Please refresh your browser for the changes to take effect."

    update_button = gr.Button("Update Settings")
    update_output = gr.Textbox(label="Update Status")

    update_button.click(
        update_settings,
        inputs=input_components,
        outputs=update_output
    )

# Load settings on module import
load_settings()

if __name__ == "__main__":
    with gr.Blocks() as demo:
        create_settings_interface()
    demo.launch()
