import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def check_llm(name, url, headers=None):
    try:
        response = requests.get(url, headers=headers, timeout=2)
        if response.status_code in [200, 405, 422]:
            return name
    except requests.RequestException:
        pass
    return None


def find_local_LLM():
    llms = [
        ("Ollama", "http://localhost:11434/api/version"),
        ("LM Studio", "http://localhost:1234/v1/models"),
        ("GPT4All", "http://localhost:4891/v1/models"),
        ("LocalAI", "http://localhost:8080/v1/models"),
        ("llama.cpp", "http://localhost:8000/v1/models"),
        ("oobabooga", "http://127.0.0.1:5000/v1/completions")
    ]

    try:
        with open('key.api', 'r') as key_file:
            api_key = key_file.read().strip()
    except FileNotFoundError:
        api_key = None

    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None

    with ThreadPoolExecutor(max_workers=6) as executor:
        future_to_llm = {executor.submit(check_llm, name, url, headers): name for name, url in llms}
        for future in as_completed(future_to_llm):
            result = future.result()
            if result:
                return result

    return None


if __name__ == "__main__":
    start_time = time.time()
    active_llm = find_local_LLM()
    end_time = time.time()

    if active_llm:
        print(f"Active Local LLM found: {active_llm}")
    else:
        print("No active Local LLM found")

    print(f"Time taken: {end_time - start_time:.2f} seconds")
