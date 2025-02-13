import anthropic
from utils_proxy import transform_response, verify_header, verify_request, create_param_dict, create_chunk, create_final_chunk
from flask import Flask, request, jsonify, Response
import os

app = Flask(__name__)


CLAUDE_BASE_URL = "https://api.anthropic.com"


@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    """
    Proxy pour /v1/chat/completions.
    Pour des échanges (champ "messages")
    """
    # Récupération de la requête
    data = request.get_json(force=True)

    # Vérification du header
    is_valid, api_key = verify_header(request)
    if not is_valid:
        return jsonify({"error": {"message": api_key}}), 401
    

    # Vérification de la requête
    is_valid, error_message = verify_request(data)
    if not is_valid:
        return jsonify({"error": {"message": error_message}}), 400
    
    param = create_param_dict(data)

    # Appel de l'API Claude
    client = anthropic.Anthropic(api_key=api_key)

    # Traitement de la réponse
    if data.get("stream", False):  # Mode streaming activé
        def generate():
            with client.messages.stream(**param) as stream:
                for text in stream.text_stream:
                    print(f"=== Chunk reçu : {text}")
                    yield create_chunk(text, model=data["model"])
                print("=== Fin de la réponse ===")
                yield create_final_chunk(model=data["model"])

        return Response(generate(), mimetype="text/event-stream")
    
    else:  # Mode non-streaming
        response = client.messages.create(**param)
        print(f"=== Réponse brute de Claude : {response}")
        openai_response = transform_response(response, data["model"])
        return jsonify(openai_response)

@app.route("/v1/models", methods=["GET"])
def list_models():
    """
    Proxy pour /v1/models.
    Renvoie la liste des 20 premiers modèles disponibles.
    """
    # Vérification du header
    is_valid, api_key = verify_header(request)
    if not is_valid:
        return jsonify({"error": {"message": api_key}}), 401

    limit = request.args.get("limit", default=20, type=int)
    client = anthropic.Anthropic(api_key=api_key)
    models = client.models.list(limit=limit)
    models_dict = {"data": [{"id": model.id, "name": model.display_name} for model in models.data]}
    return jsonify(models_dict)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT", 5000))
