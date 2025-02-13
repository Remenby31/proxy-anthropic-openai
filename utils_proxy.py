import time
import uuid
from flask import jsonify
import json

def verify_header(request):
    """
    Vérifie la présence de la clé API dans les headers de la requête.

    Paramètres :
      - request : La requête Flask.

    Renvoie :
        - Un booléen indiquant si la clé API est présente.
        - La clé API ou un message d'erreur.
    """
    try:
        auth_header = request.headers["Authorization"]
        if not auth_header.startswith("Bearer "):
            print(f" Header : {request.headers}")
            return False, "Format de clé API invalide"
        api_key = auth_header.split(" ")[1]
        return True, api_key
    except KeyError:
        print(f" Header : {request.headers}")
        return False, "Clé API manquante"
    

def verify_request(data):
    if 'model' not in data:
        return False, "Le champ 'model' est requis."
    if 'messages' not in data:
        return False, "Le champ 'messages' est requis."
    if not data['messages']:
        return False, "Le champ 'messages' ne peut pas être vide."
    return True, ""

def create_param_dict(openai_payload):
    """
    Crée un dictionnaire de paramètres à partir de la charge utile OpenAI.

    Paramètres :
      - openai_payload (dict) : La charge utile OpenAI.

    Renvoie :
      - Un dictionnaire de paramètres pour l'appel API.
    """
    # Messages
    messages = openai_payload.get("messages", [])
    if "system_prompt" in openai_payload:
        messages = [{"role": "system", "content": openai_payload["system_prompt"]}] + messages

    # Dictionnaire de paramètres avec les champs requis
    params = {
        "messages": messages,
        "model": openai_payload.get("model"),
        "max_tokens": openai_payload.get("max_tokens", 4096)
    }

    # Ajout des paramètres optionnels s'ils existent dans la requête
    for param in ["temperature", "top_p"]:
        if param in openai_payload:
            params[param] = openai_payload[param]

    # Gestion des séquences d'arrêt
    if "stop" in openai_payload:
        stop = openai_payload["stop"]
        params["stop_sequences"] = [stop] if not isinstance(stop, list) else stop

    return params

def transform_response(cl_response, model):
    """
    Transforme une réponse complète de Claude au format OpenAI.
    """
    def safe_get(obj, key, default=None):
        if hasattr(obj, 'get'):
            return obj.get(key, default)
        return getattr(obj, key, default)
    
    text = ""
    content = safe_get(cl_response, "content")
    if isinstance(content, list):
        for block in content:
            if safe_get(block, "type") == "text":
                text += safe_get(block, "text", "")
    elif isinstance(content, str):
        text = content

    usage = safe_get(cl_response, "usage", {})
    input_tokens = safe_get(usage, "input_tokens", 0)
    output_tokens = safe_get(usage, "output_tokens", 0)
    total_tokens = input_tokens + output_tokens

    stop_reason = safe_get(cl_response, "stop_reason")
    finish_reason = "stop" if stop_reason == "end_turn" else stop_reason

    openai_resp = {
        "id": "chatcmpl-" + safe_get(cl_response, "id", str(uuid.uuid4())),
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": text},
                "finish_reason": finish_reason
            }
        ],
        "usage": {
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": total_tokens
        }
    }
    return openai_resp


def create_chunk(text, model, unique_id=None):
    """
    Crée un chunk de réponse formaté selon le standard OpenAI.
    
    Args:
        text (str): Le fragment de texte à envoyer.
        model (str): Le nom du modèle utilisé.
        unique_id (str): Identifiant unique du chunk (à générer dynamiquement en production).
    
    Returns:
        str: Une chaîne formatée pour SSE.
    """
    if unique_id is None:
        unique_id = f"chatcmpl-{uuid.uuid4().hex}"
    chunk = {
        "id": unique_id,  # Remplacer par une génération dynamique d'identifiant si besoin
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "delta": {"content": text},
                "index": 0,
                "finish_reason": None
            }
        ]
    }
    return f"data: {json.dumps(chunk)}\n\n"

def create_final_chunk(model, unique_id=None):
    """
    Crée un chunk de fin de réponse formaté selon le standard OpenAI.
    
    Args:
        model (str): Le nom du modèle utilisé.
        unique_id (str): Identifiant unique du chunk (à générer dynamiquement en production).
    
    Returns:
        str: Une chaîne formatée pour SSE.
    """
    if unique_id is None:
        unique_id = f"chatcmpl-{uuid.uuid4().hex}"
    chunk = {
        "id": unique_id,  # Remplacer par une génération dynamique d'identifiant si besoin
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "delta": {},
                "index": 0,
                "finish_reason": "stop"
            }
        ]
    }
    return f"data: {json.dumps(chunk)}\n\n"