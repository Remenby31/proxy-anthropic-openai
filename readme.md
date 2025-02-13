# Proxy Anthropic-OpenAI

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
docker run -d \
  --name proxy-anthropic \
  -p 5000:5000 \
  -e ANTHROPIC_API_KEY=your_api_key \
  remenby/proxy-anthropic:latest
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
docker run -d \
  --name proxy-anthropic \
  -p 5000:5000 \
  -e ANTHROPIC_API_KEY=your_api_key \
  proxy-anthropic
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

### Example Calls

#### Non-streaming mode

```bash
curl -X POST http://0.0.0.0:5000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "your-model",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

#### Streaming mode

```bash
curl -N -X POST http://0.0.0.0:5000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "your-model",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": true
  }'
```

#### Example using OpenAI Python library

```python
import openai

openai.api_base = "http://0.0.0.0:5000"
openai.api_key = "YOUR_API_KEY"

response = openai.ChatCompletion.create(
    model="your-model",
    messages=[{"role": "user", "content": "Hello"}]
)

print(response)
```

## Architecture

- **claude_proxy.py**: Application entry point and endpoint routing.
- **utils_proxy.py**: Utility functions for request/response validation and transformation.
- **readme.md** (this file): Complete project documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
