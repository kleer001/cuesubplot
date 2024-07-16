import configparser
import requests
from findLLM import find_local_LLM

def load_config():
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    return config

def query_llm(prompt, active_llm, config=None):
    if config is None:
        config = load_config()

    settings = dict(config["DEFAULT"])
    if active_llm in config:
        settings.update(dict(config[active_llm]))

    url = f"{settings['url']}{settings['endpoint']}"

    headers = {"Content-Type": "application/json"}

    if active_llm == 'LM Studio':
        payload = {
            "model": settings.get('model', ''),
            "messages": [
                {"role": "system", "content": settings.get('system_message', '')},
                {"role": "user", "content": prompt}
            ],
            "temperature": float(settings.get('temperature', 0.7)),
            "max_tokens": int(settings.get('max_tokens', 100)),
        }
    elif active_llm == 'oobabooga':
        payload = {
            "model": settings.get('model', ''),
            "prompt": prompt,
            "max_new_tokens": int(settings.get('max_tokens', 100)),
            "temperature": float(settings.get('temperature', 0.7)),
        }
    elif active_llm == 'LocalAI':
        payload = {
            "model": settings.get('model', ''),
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": float(settings.get('temperature', 0.7)),
            "max_tokens": int(settings.get('max_tokens', 100)),
        }
    elif active_llm == 'llama.cpp':
        payload = {
            "prompt": prompt,
            "max_tokens": int(settings.get('max_tokens', 100)),
            "temperature": float(settings.get('temperature', 0.7)),
            "stop": settings.get('stop', '').split(',') if settings.get('stop') else [],
            "n_predict": int(settings.get('max_tokens', 100)),
            "stream": settings.get('stream', 'False').lower() == 'true',
        }
    else:
        payload = {
            "model": settings.get('model', ''),
            "prompt": prompt,
            "max_tokens": int(settings.get('max_tokens', 100)),
            "temperature": float(settings.get('temperature', 0.7)),
        }

    if 'top_p' in settings and active_llm not in ['LM Studio', 'LocalAI']:
        payload['top_p'] = float(settings.get('top_p', 1.0))

    if 'stop' in settings and active_llm not in ['LM Studio', 'LocalAI', 'llama.cpp']:
        payload['stop'] = settings.get('stop', '').split(',')

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error querying {active_llm}: {e}")
        return None


def get_response(response, active_llm):
    if active_llm == 'Ollama':
        return response['response']
    elif active_llm in ['LM Studio', 'LocalAI']:
        return response['choices'][0]['message']['content']
    elif active_llm == 'GPT4All':
        return response['choices'][0]['text']
    elif active_llm == 'llama.cpp':
        # Try different possible keys for the generated text
        for key in ['content', 'text', 'generated_text', 'completion', 'output']:
            if key in response:
                return response[key]

        # Check for command-line style keys
        if 'args' in response:
            args = response['args']
            for key in ['--prompt', '-p', '--output', '-o']:
                if key in args:
                    return args[key]

        # If no matching key is found, return an empty string
        return ''
    elif active_llm == 'oobabooga':
        return response['results'][0]['text']
    else:
        return "Unsupported LLM response format"


def get_llm_response(prompt):
    config = load_config()
    active_llm = find_local_LLM()

    if active_llm:
        response = query_llm(prompt, active_llm, config)
        if response:
            return get_response(response, active_llm)
        else:
            return "Error: Failed to get a response from the LLM"
    else:
        return "Error: No active Local LLM found"
