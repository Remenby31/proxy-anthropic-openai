# Proxy Anthropic-OpenAI

Ce projet implémente un proxy pour interagir avec l'API d'Anthropic et offrir une interface compatible avec OpenAI.  
Il permet d'intercepter les requêtes, de les vérifier et de les transformer pour les adapter aux formats attendus.

## Fonctionnalités

- Proxy pour l'endpoint `/v1/chat/completions` avec support du mode streaming et non-streaming.
- Conversion des réponses d'Anthropic au format OpenAI.
- Endpoint `/v1/models` pour lister les modèles disponibles (limité aux 20 premiers).
- Vérification des headers et de la charge utile.

## Déploiement

### Option 1 : Utilisation de l'image Docker publique

L'image Docker est disponible sur Docker Hub. Pour l'utiliser :

```bash
docker run -d \
  --name proxy-anthropic \
  -p 5000:5000 \
  -e ANTHROPIC_API_KEY=votre_clé_api \
  remenby/proxy-anthropic:latest
```

### Option 2 : Construction de l'image locale

Si vous souhaitez construire l'image vous-même :

```bash
# Cloner le dépôt
git clone https://votre-repo-url.git
cd proxy-anthropic-openai

# Construire l'image
docker build -t proxy-anthropic .

# Lancer le conteneur
docker run -d \
  --name proxy-anthropic \
  -p 5000:5000 \
  -e ANTHROPIC_API_KEY=votre_clé_api \
  proxy-anthropic
```

### Gestion du conteneur

```bash
# Vérifier les logs
docker logs -f proxy-anthropic

# Arrêter le conteneur
docker stop proxy-anthropic

# Supprimer le conteneur
docker rm proxy-anthropic
```

## Utilisation

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

## Architecture

- **claude_proxy.py** : Le point d'entrée de l'application et le routage des endpoints.
- **utils_proxy.py** : Fonctions utilitaires pour vérifier et transformer les requêtes/réponses.
- **readme.md** (ce fichier) : Documentation complète du projet.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
