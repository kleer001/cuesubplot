import requests
import configparser


def load_config():
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    return config


def get_models(llm_name):
    config = load_config()

    if llm_name not in config:
        print(f"No configuration found for LLM: {llm_name}")
        return []

    settings = config[llm_name]

    if 'models_endpoint' not in settings:
        print(f"No models endpoint configured for LLM: {llm_name}")
        return []

    url = f"{settings['url']}{settings['models_endpoint']}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        models_key = settings.get('models_key', 'data')
        model_name_key = settings.get('model_name_key', 'id')

        if models_key in data:
            return [model[model_name_key] for model in data[models_key]]
        elif isinstance(data, list):
            return [model[model_name_key] for model in data]
        else:
            print(f"Unexpected response structure from {llm_name}")
            return []
    except requests.RequestException as e:
        print(f"Error fetching {llm_name} models: {e}")
        return []


# Example usage
if __name__ == "__main__":
    llms = ["Ollama", "LM Studio", "GPT4All", "LocalAI", "oobabooga"]
    for llm in llms:
        models = get_models(llm)
        print(f"{llm} models: {models}")
