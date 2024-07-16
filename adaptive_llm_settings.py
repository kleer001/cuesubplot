import json
import configparser
from llm_utils import query_llm
from findLLM import find_local_LLM


def load_config():
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    return config


def query_llm_format(active_llm, config):
    prompt = """
    Please respond with a JSON object that describes your preferred response format.
    Include the following keys:
    1. 'content_key': The key used for the main generated text content.
    2. 'metadata_keys': An array of keys used for any metadata in the response.
    3. 'error_key': The key used for error messages.
    4. 'structure': A brief description of the overall response structure.

    Example:
    {
        "content_key": "generated_text",
        "metadata_keys": ["model_name", "timestamp", "token_count"],
        "error_key": "error_message",
        "structure": "Top-level object with content and metadata as direct keys"
    }
    """
    response = query_llm(prompt, active_llm, config)
    try:
        format_info = json.loads(response)
        return format_info
    except json.JSONDecodeError:
        print(f"Failed to parse response format from {active_llm}")
        return None


def get_llm_format(active_llm=None):
    config = load_config()
    if active_llm is None:
        active_llm = find_local_LLM()

    if active_llm:
        format_info = query_llm_format(active_llm, config)
        if format_info:
            return format_info
        else:
            return {"error": f"Failed to get format information from {active_llm}"}
    else:
        return {"error": "No active Local LLM found"}


def print_format_info(format_info):
    if 'error' in format_info:
        print(f"Error: {format_info['error']}")
    else:
        print("LLM Response Format:")
        print(f"Content Key: {format_info.get('content_key', 'N/A')}")
        print(f"Metadata Keys: {', '.join(format_info.get('metadata_keys', ['N/A']))}")
        print(f"Error Key: {format_info.get('error_key', 'N/A')}")
        print(f"Structure: {format_info.get('structure', 'N/A')}")


if __name__ == "__main__":
    llm_format = get_llm_format()
    print_format_info(llm_format)
