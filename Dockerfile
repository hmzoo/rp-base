# Image de base Python optimisée
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système si nécessaire
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY handler.py .

# Commande pour démarrer le worker RunPod
CMD ["python", "-u", "handler.py"]
