# Proxy Anthropic-OpenAI

Ce projet implémente un proxy pour interagir avec l'API d'Anthropic et offrir une interface compatible avec OpenAI.  
Il permet d'intercepter les requêtes, de les vérifier et de les transformer pour les adapter aux formats attendus.

## Fonctionnalités

- Proxy pour l'endpoint `/v1/chat/completions` avec support du mode streaming et non-streaming.
- Conversion des réponses d'Anthropic au format OpenAI.
- Endpoint `/v1/models` pour lister les modèles disponibles (limité aux 20 premiers).
- Vérification des headers et de la charge utile.

## Prérequis

- Python 3.x
- Flask
- Bibliothèque `anthropic`
- Autres dépendances listées dans `requirements.txt` (à créer le cas échéant)

## Installation

```bash
# Cloner le dépôt
git clone https://votre-repo-url.git

# Se placer dans le répertoire du projet
cd proxy-anthropic-openai

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation

### Mode développement

```bash
python claude_proxy.py
```

### Mode production

```bash
gunicorn --bind 0.0.0.0:5000 claude_proxy:app
```

Pour lancer le proxy en mode développement :

```bash
python claude_proxy.py
```

Le proxy sera accessible sur `http://0.0.0.0:5000`.

### Exemple d'appel

#### Mode non-streaming

```bash
curl -X POST http://0.0.0.0:5000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_API_KEY" \
  -d '{
    "model": "votre-modele",
    "messages": [{"role": "user", "content": "Bonjour"}]
  }'
```

#### Mode streaming

```bash
curl -N -X POST http://0.0.0.0:5000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_API_KEY" \
  -d '{
    "model": "votre-modele",
    "messages": [{"role": "user", "content": "Bonjour"}],
    "stream": true
  }'
```

#### Exemple avec la librairie OpenAI en Python

Installez la librairie avec :
```bash
pip install openai
```

Utilisez le code suivant pour effectuer la requête :
```python
import openai

openai.api_base = "http://0.0.0.0:5000"
openai.api_key = "VOTRE_API_KEY"

response = openai.ChatCompletion.create(
    model="votre-modele",
    messages=[{"role": "user", "content": "Bonjour"}]
)

print(response)
```

## Déploiement avec Docker

### Construction de l'image

```bash
docker build -t proxy-anthropic .
```

### Lancement du conteneur

```bash
docker run -d --name proxy-anthropic -p 5000:5000 proxy-anthropic
```

### Vérification des logs

```bash
docker logs -f proxy-anthropic
```

### Arrêt du conteneur

```bash
docker stop proxy-anthropic
```

## Architecture

- **claude_proxy.py** : Le point d'entrée de l'application et le routage des endpoints.
- **utils_proxy.py** : Fonctions utilitaires pour vérifier et transformer les requêtes/réponses.
- **readme.md** (ce fichier) : Documentation complète du projet.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

# ...autres informations éventuelles...
