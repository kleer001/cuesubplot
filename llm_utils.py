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

    llm_config = config[active_llm]

    url = f"{llm_config['url']}{llm_config['endpoint']}"

    headers = {"Content-Type": "application/json"}

    if active_llm == 'LM Studio':
        payload = {
            "model": llm_config['model'],
            "messages": [
                {"role": "system", "content": llm_config['system_message']},
                {"role": "user", "content": prompt}
            ],
            "temperature": float(llm_config['temperature']),
            "max_tokens": int(llm_config['max_tokens']),
        }
    elif active_llm == 'oobabooga':
        payload = {
            "model": llm_config['model'],
            "prompt": prompt,
            "max_new_tokens": int(llm_config['max_tokens']),
            "temperature": float(llm_config['temperature']),
        }
    else:
        payload = {
            "model": llm_config['model'],
            "prompt": prompt,
            "max_tokens": int(llm_config['max_tokens']),
            "temperature": float(llm_config['temperature']),
        }

    if 'top_p' in llm_config and active_llm != 'LM Studio':
        payload['top_p'] = float(llm_config['top_p'])

    if 'stop' in llm_config and active_llm != 'LM Studio':
        payload['stop'] = llm_config['stop'].split(',')

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
        return response['content']
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

