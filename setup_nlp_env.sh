#!/bin/bash

# Script de configuration automatique de l'environnement NLP

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Vérification de Python
check_python() {
    if command -v python3.9 &> /dev/null; then
        echo -e "${GREEN}Python 3.9 est installé${NC}"
        return 0
    else
        echo -e "${RED}Python 3.9 n'est pas installé${NC}"
        return 1
    fi
}

# Installation de Python 3.9 si nécessaire
install_python() {
    echo "Installation de Python 3.9..."

    # Détection du système d'exploitation
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install python@3.9
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux (Ubuntu/Debian)
        sudo apt-get update
        sudo apt-get install -y python3.9 python3.9-venv python3.9-dev
    else
        echo -e "${RED}Système d'exploitation non supporté${NC}"
        exit 1
    fi
}

# Configuration de l'environnement virtuel
setup_virtual_env() {
    echo "Configuration de l'environnement virtuel..."

    # Créer l'environnement virtuel
    python3.9 -m venv nlp_env

    # Activer l'environnement
    source nlp_env/bin/activate

    # Mise à jour de pip
    pip install --upgrade pip setuptools wheel

    # Installation des dépendances
    pip install -r requirements.txt

    echo -e "${GREEN}Environnement NLP configuré avec succès!${NC}"
}

# Script principal
main() {
    if ! check_python; then
        install_python
    fi

    setup_virtual_env

    # Informations supplémentaires
    echo -e "${GREEN}Pour activer l'environnement : source nlp_env/bin/activate${NC}"
}

# Exécution du script
main