# Proxy Anthropic-OpenAI

<img src="docs/logo_makehub.png" width="200" alt="Logo MakeHub"/>

This project implements a proxy to interact with Anthropic's API while providing an OpenAI-compatible interface.
It intercepts requests, validates them, and transforms them to match the expected formats.

## Features

- Proxy for the `/v1/chat/completions` endpoint with support for streaming and non-streaming modes.
- Conversion of Anthropic responses to OpenAI format.
- `/v1/models` endpoint to list available models (limited to top 20).
- Headers and payload validation.

## Deployment

### Option 1: Using the public Docker image

The Docker image is available on Docker Hub. To use it:

```bash
docker run -d --name proxy-anthropic -p 5000:5000 -e ANTHROPIC_API_KEY=your_api_key remenby/proxy-anthropic:latest
```

### Option 2: Building the local image

If you want to build the image yourself:

```bash
# Clone the repository
git clone https://your-repo-url.git
cd proxy-anthropic-openai

# Build the image
docker build -t proxy-anthropic . 

# Run the container
docker run -d --name proxy-anthropic -p 5000:5000 -e ANTHROPIC_API_KEY=your_api_key proxy-anthropic
```

### Container Management

```bash
# Check logs
docker logs -f proxy-anthropic

# Stop container
docker stop proxy-anthropic

# Remove container
docker rm proxy-anthropic
```

## Usage

The proxy will be accessible at `http://0.0.0.0:5000`.

### Example Calls using OpenAI Python library

```python
from openai import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get("CLAUDE_API_KEY")
base_url = "http://0.0.0.0:5000/v1"
client = Client(api_key=api_key, base_url=base_url)
model = "claude-3-5-haiku-latest"
```

#### Non-streaming mode

```python
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Hello !"}]
)
print(response.choices[0].message.content)
```

#### Streaming mode

```python
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Hello !"}],
    stream=True,
    max_tokens=250
)

for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end='', flush=True)
```

#### List available models

```python
models = client.models.list()
print(models)
```

## Architecture

- **claude_proxy.py**: Application entry point and endpoint routing.
- **utils_proxy.py**: Utility functions for request/response validation and transformation.
- **readme.md** (this file): Complete project documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
