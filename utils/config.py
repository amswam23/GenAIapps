import os

def load_model_options():
    return ["gpt-5","gpt-4-turbo", "gpt-3.5-turbo", "llama3"]

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-key-here")
