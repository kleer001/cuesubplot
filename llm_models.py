import requests

def get_ollama_models():
    try:
        import ollama
        models = ollama.list()
        if isinstance(models, dict) and 'models' in models:
            return [model['name'] for model in models['models']]
        return models  # Assuming it's already a list of model names
    except ImportError:
        print("Ollama module not found. Please install it to use Ollama.")
        return []
    except Exception as e:
        print(f"Error fetching Ollama models: {e}")
        return []


def get_lm_studio_models():
    try:
        response = requests.get("http://localhost:1234/v1/models")
        if response.status_code == 200:
            return [model['id'] for model in response.json()['data']]
        return []
    except Exception as e:
        print(f"Error fetching LM Studio models: {e}")
        return []


def get_gpt4all_models():
    try:
        response = requests.get("http://localhost:4891/v1/models")
        if response.status_code == 200:
            return [model['id'] for model in response.json()['data']]
        return []
    except Exception as e:
        print(f"Error fetching GPT4All models: {e}")
        return []


def get_localai_models():
    try:
        response = requests.get("http://localhost:8080/v1/models")
        if response.status_code == 200:
            return [model['id'] for model in response.json()['data']]
        return []
    except Exception as e:
        print(f"Error fetching LocalAI models: {e}")
        return []


def get_oobabooga_models():
    try:
        response = requests.get("http://localhost:5000/api/v1/model")
        if response.status_code == 200:
            return response.json()['model_names']
        return []
    except Exception as e:
        print(f"Error fetching oobabooga models: {e}")
        return []


def get_models(llm_name):
    model_fetchers = {
        "Ollama": get_ollama_models,
        "LM Studio": get_lm_studio_models,
        "GPT4All": get_gpt4all_models,
        "LocalAI": get_localai_models,
        "oobabooga": get_oobabooga_models
    }

    if llm_name in model_fetchers:
        return model_fetchers[llm_name]()
    else:
        print(f"No model fetcher available for LLM: {llm_name}")
        return []
