import ollama
import settings
import configparser

config = configparser.ConfigParser()
config.read('settings.cfg')
model_value = config['DEFAULT']['model']
current_model = str(model_value)

def query_ollama(prompt):
    response = ollama.generate(model=model, prompt=prompt)
    print(prompt)
    return response['response']


def extract_key_words(text, num_words=4):
    prompt = f"""Given the following text, extract the {num_words} most important words or short phrases that capture its essence. Provide these words or phrases as a comma-separated list, without numbering or additional explanation:

    Text: {text}

    Important words/phrases:"""

    response = query_ollama(prompt)
    words = [word.strip() for word in response.split(',')]
    return words[:num_words]  # Ensure we don't exceed the requested number of words


