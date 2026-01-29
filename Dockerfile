# Image de base CUDA pour GPU (requis pour Coqui TTS XTTS_v2)
# Updated: 2026-01-29
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Installer Python et dépendances système
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    ffmpeg \
    wget \
    git \
    build-essential \
    cmake \
    libsndfile1 \
    espeak-ng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Créer un lien symbolique pour python
RUN ln -sf /usr/bin/python3.11 /usr/bin/python && \
    ln -sf /usr/bin/python3.11 /usr/bin/python3

# Définir le répertoire de travail
WORKDIR /app

# Copier les requirements et installer les dépendances Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY handler.py .

# Cloner Wav2Lip et télécharger le modèle (on utilise MediaPipe pour la détection, pas besoin de s3fd)
RUN git clone https://github.com/Rudrabha/Wav2Lip.git /app/Wav2Lip && \
    mkdir -p /app/Wav2Lip/checkpoints && \
    wget -q -O /app/Wav2Lip/checkpoints/wav2lip_gan.pth \
        https://github.com/Rudrabha/Wav2Lip/releases/download/models/wav2lip_gan.pth

# Créer les répertoires pour les modèles
RUN mkdir -p /app/models /app/temp

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV TEMP_DIR=/app/temp
ENV COQUI_TOS_AGREED=1

# Test de démarrage pour debug
RUN python --version && pip list

# Commande pour démarrer le worker
CMD ["python", "-u", "handler.py"]
