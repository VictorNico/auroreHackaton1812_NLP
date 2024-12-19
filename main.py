import logging
import argparse
import sys
import os
from tqdm import tqdm  # Import de tqdm pour les barres de progression
import importlib

# Ajouter le répertoire racine du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nlp_project.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Dictionnaire pour stocker les modules importés
imported_modules = {}

def load_modules(module_list):
    """
    Charge les modules à partir d'une liste en affichant une barre de progression
    """
    global imported_modules
    logger.info("Début du chargement des modules")
    # Charger les bibliothèques en utilisant importlib
    with tqdm(module_list, total=len(module_list), desc="Chargement des modules",unit="module") as pbar:
        for module_name in module_list:
            try:
                # exec(f'from {module_name} import * as {module_name.split(".")[-1]}')
                # Importer dynamiquement le module
                module = importlib.import_module(module_name)
                # Stocker le module dans un dictionnaire global
                imported_modules[module_name] = module

            except ImportError as e:
                # En cas d'erreur lors du chargement de la bibliothèque
                pbar.set_description(f"Erreur lors du chargement du module {module_name}: {e}")
                logger.error(f"Erreur lors du chargement du module {module_name}: {e}")
            else:
                # Succès lors du chargement de la bibliothèque
                pbar.set_description(f"Module {module_name} chargé avec succès.")
                logger.error(f"Module {module_name} chargé avec succès.")
            finally:
                pbar.set_description(f"Module terminé avec succès.")
                pbar.update(1)
                logger.info("Fin du chargement des modules")

def load_configuration():
    """
    Charge la configuration du projet
    """
    try:
        config = {
            'model_path': os.getenv('MODEL_PATH', 'models/default_model'),
            'data_path': os.getenv('DATA_PATH', 'data/'),
        }
        return config
    except Exception as e:
        logger.error(f"Erreur de chargement de la configuration : {e}")
        sys.exit(1)


def main(args):
    """
    Fonction principale du projet NLP
    """
    try:
        # Configuration
        config = load_configuration()
        logger.info("Configuration chargée avec succès")

        # Exemple de modules à charger
        modules_to_load = ['src.preprocessing.speed']

        # Chargement des modules avec tqdm pour afficher la progression
        load_modules(modules_to_load)

        # Appeler une fonction du module chargé
        if 'src.preprocessing.speed' in imported_modules:
            module_speed = imported_modules['src.preprocessing.speed']
            print(imported_modules.keys())
            print(module_speed)
            if hasattr(module_speed, 'help_soundFileDecelerate'):
                module_speed.help_soundFileDecelerate()
            else:
                logger.error("La fonction 'help_soundFileDecelerate' n'existe pas dans le module.")

        # Votre logique principale ici
        if args.mode == 'train':
            train_model(config)
        elif args.mode == 'predict':
            predict(config)
        else:
            logger.warning(f"Mode non reconnu : {args.mode}")

    except Exception as e:
        logger.error(f"Erreur fatale : {e}")
        sys.exit(1)


def train_model(config):
    """
    Entraînement du modèle NLP
    """
    logger.info("Début de l'entraînement du modèle")
    # Votre code d'entraînement ici


def predict(config):
    """
    Prédiction avec le modèle
    """
    logger.info("Début de la prédiction")
    # Votre code de prédiction ici


def parse_arguments():
    """
    Analyse des arguments en ligne de commande
    """
    parser = argparse.ArgumentParser(description='Aurore de la recherche - NLP')
    parser.add_argument(
        '-m', '--mode',
        choices=['train', 'predict'],
        default='train',
        help='Mode d\'exécution (train ou predict)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mode verbeux'
    )
    return parser.parse_args()


if __name__ == '__main__':
    # Point d'entrée du script
    args = parse_arguments()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    main(args)
