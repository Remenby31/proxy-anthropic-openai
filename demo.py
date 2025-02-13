from openai import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get("CLAUDE_API_KEY")
base_url = "http://localhost:5000/v1"
model = "claude-3-5-haiku-latest"


def streaming_mode():
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Hello !"}],
        stream=True,
        max_tokens=250
    )

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end='', flush=True)
    print("\n")

def non_streaming_mode():
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Hello !"}]
    )
    print(response.choices[0].message.content)

def list_models():
    response = client.models.list()
    return response


client = Client(api_key=api_key, base_url=base_url)

# List of models
print("=== Models list ===")
models = list_models()
print(models)

# Non streaming mode
print("=== Non streaming mode ===")
non_streaming_mode()


# Streaming mode
print("=== Streaming mode ===")
streaming_mode()