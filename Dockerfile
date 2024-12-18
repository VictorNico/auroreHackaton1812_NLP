# Image de base Python
FROM python:3.9-slim-bullseye
LABEL authors="@VictorNico"

# Métadonnées
LABEL maintainer="Votre Nom"
LABEL description="Environnement NLP Python"

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Répertoire de travail
WORKDIR /nlp_workspace

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Port pour Jupyter (optionnel)
EXPOSE 8888

# Commande par défaut
CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--no-browser", "--allow-root"]