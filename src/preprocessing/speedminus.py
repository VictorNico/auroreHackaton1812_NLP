"""
Module de traitement du son

Auteur : Victor Nico
Version : 1.0.0
Date de création : 2024-12-19

Module de traitement du son : contient des fonctions pour charger, accélérer ou ralentir des fichiers audio.

Ce module inclut des fonctionnalités pour manipuler des fichiers audio tels que :
- Charger un fichier audio.
- Appliquer des transformations (accélérer ou ralentir).
- Sauvegarder les fichiers audio modifiés.

Exemple d'utilisation 1 :
    from soundFileDecelerate import load_audio, decelerate_audio
    audio = load_audio("file.wav")
    slow_audio = decelerate_audio(audio, slow_factor=0.5)
    slow_audio.export("slowed_file.wav", format="wav")



"""

__author__ = "Victor Nico"
__version__ = "1.0.0"
__date__ = "2024-12-19"
__license__ = "APACHE LICENSE"

import logging

import librosa
import soundfile as sf
from pydub import AudioSegment
from pydub.utils import which

# Fonctions pour ralentir l'audio


def decelerate_audio(y, slow_factor=1.5):
    """
    Ralentit un fichier audio en fonction du facteur spécifié.

    Args:
        y : L'objet audio à ralentir.
        slow_factor (float): Le facteur de ralentissement. Par défaut, 0.5 signifie moitié moins rapide.

    Returns: (y_slow,sr)
        y_slow: L'objet audio ralenti.
    """
    # Réduire la vitesse (facteur > 1 diminue la vitesse, ex: 1.5 réduit de 50%)
    y_slow = librosa.effects.time_stretch(y, rate=slow_factor)

    # Retourner l'audio ralenti
    return y_slow

def decelerate_audio_v2(audio, slow_factor=0.5):

    # Réduire la vitesse (ex: slow_factor plus lent)
    slower_audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * slow_factor)})

    # Maintenir le même taux d'échantillonnage
    slower_audio = slower_audio.set_frame_rate(audio.frame_rate)

    # Retourner l'audio ralenti
    return slower_audio

def help_soundFileDecelerate():
    logging.info("Usage: python soundFileDecelerate.py <audio_path> <slow_factor>")