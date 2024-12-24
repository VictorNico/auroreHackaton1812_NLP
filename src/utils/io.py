"""
Module I/O du son

Auteur : Victor Nico
Version : 1.0.0
Date de création : 2024-12-19

Module de chargement ou exportation du son : contient des fonctions pour charger et enregistrer des fichiers audio.

Ce module inclut des fonctionnalités pour manipulation I/O audio tels que :
- Charger un fichier audio.
- Enregistrer un fichier audio.

Exemple d'utilisation 1 :
    from src.preprocessing.speed import load_audio, decelerate_audio
    audio = load_audio("file.wav")
    slow_audio = decelerate_audio(audio, slow_factor=0.5)
    slow_audio.export("slowed_file.wav", format="wav")

"""

__author__ = "Victor Nico"
__version__ = "1.0.0"
__date__ = "2024-12-19"

import librosa
import soundfile as sf
from pydub import AudioSegment
from pydub.utils import which
import logging
import pandas as pd
import os
import time

# Configurer le chemin vers ffmpeg
AudioSegment.ffmpeg = which("ffmpeg")

# Fonctions pour charger un fichier audio
def load_audio(file_path):
    """
    Charge un fichier audio à partir du chemin spécifié.

    Args:
        file_path (str): Le chemin vers le fichier audio à charger.

    Returns:
        librosa-audio: L'objet audio chargé.
    """
    return librosa.load(file_path, sr=None)

def load_audio_v2(file_path):
    """
    Charge un fichier audio à partir du chemin spécifié.

    Args:
        file_path (str): Le chemin vers le fichier audio à charger.

    Returns:
        AudioSegment: L'objet audio chargé.
    """
    return AudioSegment.from_wav(file_path) # .from_file



def save_audio(audio, file_path):
    """
    Sauvegarde un objet audio dans un fichier au format spécifié.

    Args:
        audio (AudioSegment): L'objet audio à sauvegarder.
        file_path (str): Le chemin où le fichier audio doit être sauvegardé.
    """
    try:
        audio.export(file_path, format="wav")  # Sauvegarde au format WAV
        print(f"Fichier audio sauvegardé sous {file_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier audio : {e}")



def save_audio_v2(audio, file_path, sr):
    """
    Sauvegarde un objet audio dans un fichier au format spécifié.

    Args:
        audio (AudioSegment): L'objet audio à sauvegarder.
        file_path (str): Le chemin où le fichier audio doit être sauvegardé.
    """
    try:
        sf.write(file_path, audio, sr)
        print(f"Fichier audio sauvegardé sous {file_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier audio : {e}")


def load_meta(path, na_values, sep=',', encoding='utf-8', index_col=None, verbose=False):
    """Lire un jeu de données à partir d'un format multiple
    Args :
      path : chemin vers le jeu de données
      sep : le délimiteur dans le fichier
      encoding : encodage utilisé pour enregistrer le fichier
      index_col : colonne contenant les valeurs de l'index

    Retourne :
      L'instance du jeu de données chargé
    """

    extension = os.path.splitext(path)[1] if isinstance(path, str) else None

    if extension is None:
        extension = '.csv'

    print(f"file ext know as {extension}") if verbose else None

    readers = {
        ".csv": pd.read_csv,
        ".xlsx": pd.read_excel,
        ".json": pd.read_json,

    }

    dataset = (readers[extension](path, sep=sep, encoding='utf-8', index_col=index_col,
                                  na_values=na_values) if '.csv' in extension else readers[extension](path,
                                                                                                      index_col=index_col,
                                                                                                      na_values=na_values)) if \
    readers[extension] else f"no reader define for the extension {extension}"

    return dataset


def save_dataset(dir, dataframe, name, prefix=None, sep='\t'):
    """Sauvegarder un cadre de données
    Args :
      dataframe : Une instance de dataframe
      name : le nom
      sep : le séparateur

    Retourne :
      filename : chemin d'accès au fichier sauvegardé
    """

    create_domain(dir)

    timestr = time.strftime("%Y_%m_%d_%H_%M_%S")
    filename = dir + (prefix if prefix != None else '') + name + '_' + timestr + '.csv'
    dataframe.to_csv(filename, sep=sep, encoding='utf-8')

    return filename

def create_domain(directory, verbose=True):
    """Créer un répertoire d'analyse de domaine
    Args :
      directory : chemin d'accès au répertoire
      verbose : si une console d'impression est nécessaire

    Retourne :
      L'état de la création
    """

    state=False
    try:
        os.makedirs(directory)
        state=True
        print(f"Répertoire '{directory}' créé avec succès.") if verbose else None
    except FileExistsError:
        print(f"Le répertoire '{directory}' existe déjà.") if verbose else None
    except OSError as e:
        print(f"Une erreur s'est produite lors de la création du répertoire '{directory}': {e}") if verbose else None
    return state