import configparser
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


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
        print(f" {name}: {e}")
    return None


def find_local_LLM():
    config = load_config()

    llms = []
    for section in config.sections():
        if section == 'DEFAULT':
            continue
        url = config[section].get('url')
        endpoint = config[section].get('models_endpoint', '')
        if url:
            llms.append((section, url, endpoint))

    print(f"Found {len(llms)} potential LLMs in config")

    with ThreadPoolExecutor(max_workers=len(llms)) as executor:
        future_to_llm = {executor.submit(check_llm, name, url, endpoint): name for name, url, endpoint in llms}
        for future in as_completed(future_to_llm):
            result = future.result()
            if result:
                print(f"Returning active LLM: {result}")
                return result

    print("No active LLM found")
    return None


if __name__ == "__main__":
    active_llm = find_local_LLM()
    print(f"Active LLM: {active_llm}")
