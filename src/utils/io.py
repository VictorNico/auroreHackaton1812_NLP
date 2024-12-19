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
    from soundFileDecelerate import load_audio, decelerate_audio
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