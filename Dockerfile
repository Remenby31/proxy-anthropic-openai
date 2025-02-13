FROM python:3.8-alpine

WORKDIR /app

# Installation des dépendances système nécessaires
RUN apk add --no-cache gcc musl-dev linux-headers

COPY requierement.txt .

RUN pip install --no-cache-dir -r requierement.txt

COPY . .

EXPOSE 5000

# Remplacer la commande python par gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "claude_proxy:app"]
