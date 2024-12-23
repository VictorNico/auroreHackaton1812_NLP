import sys
import os
import numpy as np
import soundfile as sf
import pytest
import shutil

# Ajouter le chemin du répertoire contenant add_noises.py
sys.path.insert(0, r'C:\Users\Christian\Desktop\hackathon\add_noises')

# Importer les fonctions depuis add_noises.py
from add_noises import ajouter_bruit, charger_audio, traiter_repertoire, verifier_bruit

# Constantes pour les tests
input_dir = r'C:\Users\Christian\Desktop\hackathon\Nouveau dossier'
output_dir = r'C:\Users\Christian\Desktop\hackathon\Nouveau dossier (2)'
niveau_bruit = 10  # Spécifier le niveau de bruit souhaité
seuil_diff = 0.01  # Seuil de différence pour considérer qu'il y a du bruit

@pytest.fixture
def setup_directories(): 
    # Vérifier que output_dir n'est pas un répertoire critique 
    if output_dir in ('/', 'C:\\', '','/ '): 
        raise ValueError("output_dir ne doit pas être '/' ou 'C:\\' ou une chaîne vide.") 
    if not os.path.exists(output_dir): 
        os.makedirs(output_dir) 
    yield 
    shutil.rmtree(output_dir)

def test_ajouter_bruit():
    audio, fs = charger_audio(os.path.join(input_dir, 'fichier_test.wav'))
    audio_bruite = ajouter_bruit(audio, niveau_bruit)
    assert audio_bruite is not None
    assert len(audio_bruite) == len(audio)

def test_verifier_bruit():
    original_audio, fs = charger_audio(os.path.join(input_dir, 'fichier_test.wav'))
    modifie_audio = ajouter_bruit(original_audio, niveau_bruit)
    assert verifier_bruit(original_audio, modifie_audio, seuil_diff) == True

def test_traiter_repertoire(setup_directories):
    traiter_repertoire(input_dir, output_dir, niveau_bruit, True)
    fichiers_non_bruites = []
    for filename in os.listdir(input_dir):
        if filename.endswith('.wav'):
            original_filepath = os.path.join(input_dir, filename)
            modifie_filepath = os.path.join(output_dir, filename)
            original_audio, fs = charger_audio(original_filepath)
            modifie_audio, _ = charger_audio(modifie_filepath)
            if not verifier_bruit(original_audio, modifie_audio, seuil_diff):
                fichiers_non_bruites.append(filename)
    assert len(fichiers_non_bruites) == 0
