# AI API Service

A FastAPI-based API that provides endpoints to interact with AI models through OpenAI and Ollama.

## Features

- RESTful API with FastAPI
- Support for OpenAI API
- Support for Ollama (local AI models)
- Interactive documentation with Swagger UI

## Requirements

- Python 3.8+
- OpenAI API Key (for OpenAI endpoints)
- Ollama installed locally (for Ollama endpoints)

## Installation

1. Clone the repository:
```bash
git clone [REPOSITORY_URL]
cd ai-api-service
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```
Edit the `.env` file and add the necessary API keys.

## Usage

1. Start the development server:
```bash
python run.py
```

2. Access the API documentation:
```
http://localhost:8000/docs
```

## Endpoints

### OpenAI

- `POST /api/openai/chat`: Send a chat request to the OpenAI API
- `GET /api/openai/models`: Get available OpenAI models

### Ollama

- `POST /api/ollama/chat`: Send a chat request to the Ollama API
- `GET /api/ollama/models`: Get available Ollama models

## Usage Example

### OpenAI Chat Request

```python
import requests
import json

url = "http://localhost:8000/api/openai/chat"
payload = {
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ],
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(json.dumps(response.json(), indent=2))
```

### Ollama Chat Request

```python
import requests
import json

url = "http://localhost:8000/api/ollama/chat"
payload = {
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ],
    "model": "llama3",
    "temperature": 0.7,
    "max_tokens": 500
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(json.dumps(response.json(), indent=2))
```

## License

[MIT](LICENSE)
