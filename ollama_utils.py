import ollama
import settings

def query_ollama(prompt):
    response = ollama.generate(model=settings.current_model, prompt=prompt)
    return response['response']


