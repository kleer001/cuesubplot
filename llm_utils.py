import configparser
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from findLLM import find_local_LLM
from text_utils import parse_list

def load_config(file_path='settings.cfg'):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config


def check_llm(name, url, endpoint):
    try:
        full_url = f"{url}{endpoint}"
        print(f"Checking {name} at {full_url}")
        response = requests.get(full_url, timeout=2)
        if response.status_code == 200:
            print(f"{name} is available")
            return name
        else:
            print(f"{name} returned status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Error checking {name}: {e}")
    return None

def build_payload(prompt, settings):
    payload = {}
    payload_structure = eval(settings.get('payload_structure', '{}'))

    for key, value in payload_structure.items():
        if isinstance(value, str):
            payload[key] = prompt if value == 'prompt' else settings.get(value, '')
        elif isinstance(value, list):
            payload[key] = [
                {sub_key: (prompt if sub_value == 'prompt' else settings.get(sub_value, ''))
                 for sub_key, sub_value in item.items()}
                for item in value if isinstance(item, dict)
            ]
    return payload


def query_llm(prompt, active_llm, config=None):
    config = config or load_config()

    if not active_llm:
        print("Error: No active LLM specified")
        return None

    print(f"Active LLM: {active_llm}")
    print(f"Config Sections: {config.sections()}")

    if active_llm not in config:
        print(f"Error: {active_llm} not found in config")
        return None

    settings = {**config['DEFAULT'], **config[active_llm]}
    print(f"Settings: {settings}")

    url = settings['url']
    endpoint = settings.get('endpoint', '')
    full_url = f"{url}{endpoint}"

    headers = {"Content-Type": "application/json"}
    payload = {
        "model": settings.get('model', 'mistral:latest'),
        "prompt": prompt,
        "stream": settings.get('stream', 'false').lower() == 'true'
    }

    print(f"URL: {full_url}")
    print(f"Payload: {payload}")

    try:
        response = requests.post(full_url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        return response.json()
    except requests.RequestException as e:
        print(f"Error querying {active_llm}: {e}")
        if e.response:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        else:
            print("No response received")
        return None
def extract_response(response, response_key):
    keys = response_key.split('.')
    for key in keys:
        if key.isdigit():
            response = response[int(key)]
        else:
            response = response.get(key, {})
    return response


def get_response(response, active_llm, config=None):
    config = config or load_config()
    settings = {**config['DEFAULT'], **config[active_llm]}
    response_key = settings.get('response_key', '')
    return extract_response(response, response_key)


def get_llm_response(prompt):
    config = load_config()
    active_llm = find_local_LLM()

    if active_llm:
        response = query_llm(prompt, active_llm, config)
        if response:
            content = get_response(response, active_llm, config)
            return parse_list(content)
        return "Error: Failed to get a response from the LLM"
    return "Error: No active Local LLM found"
