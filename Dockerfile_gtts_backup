# Image de base Python légère (pour TTS uniquement)
# Utilisez nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04 quand vous ajouterez Wav2Lip
FROM python:3.11-slim

# Installer ffmpeg pour traitement audio/vidéo
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les requirements et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY handler.py .

# Créer les répertoires pour les modèles
RUN mkdir -p /app/models /app/temp

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV TEMP_DIR=/app/temp

# Commande pour démarrer le worker
CMD ["python", "-u", "handler.py"]
