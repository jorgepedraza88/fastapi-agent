# AI API Service

Una API basada en FastAPI que proporciona endpoints para interactuar con modelos de IA a través de OpenAI y Ollama.

## Características

- API RESTful con FastAPI
- Soporte para OpenAI API
- Soporte para Ollama (modelos de IA locales)
- Documentación interactiva con Swagger UI

## Requisitos

- Python 3.8+
- OpenAI API Key (para los endpoints de OpenAI)
- Ollama instalado localmente (para los endpoints de Ollama)

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd ai-api-service
```

2. Crear un entorno virtual e instalar las dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
```
Editar el archivo `.env` y agregar las claves de API necesarias.

## Uso

1. Iniciar el servidor de desarrollo:
```bash
python run.py
```

2. Acceder a la documentación de la API:
```
http://localhost:8000/docs
```

## Endpoints

### OpenAI

- `POST /api/openai/chat`: Enviar una solicitud de chat a la API de OpenAI
- `GET /api/openai/models`: Obtener modelos disponibles de OpenAI

### Ollama

- `POST /api/ollama/chat`: Enviar una solicitud de chat a la API de Ollama
- `GET /api/ollama/models`: Obtener modelos disponibles de Ollama

## Ejemplo de Uso

### Solicitud de chat a OpenAI

```python
import requests
import json

url = "http://localhost:8000/api/openai/chat"
payload = {
    "messages": [
        {"role": "system", "content": "Eres un asistente útil."},
        {"role": "user", "content": "Hola, ¿cómo estás?"}
    ],
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(json.dumps(response.json(), indent=2))
```

### Solicitud de chat a Ollama

```python
import requests
import json

url = "http://localhost:8000/api/ollama/chat"
payload = {
    "messages": [
        {"role": "system", "content": "Eres un asistente útil."},
        {"role": "user", "content": "Hola, ¿cómo estás?"}
    ],
    "model": "llama3",
    "temperature": 0.7,
    "max_tokens": 500
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(json.dumps(response.json(), indent=2))
```

## Licencia

[MIT](LICENSE)
