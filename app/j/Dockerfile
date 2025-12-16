# Image de base Python 3.11
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code source
COPY . .

# Exposer le port 8001
EXPOSE 8001

# Variables d'environnement par défaut (peuvent être surchargées)
ENV PYTHONUNBUFFERED=1

# Commande pour lancer le serveur
CMD ["python", "server.py"]