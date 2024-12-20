import math
import os
import pytest
import numpy as np
from src.utils.io import load_audio, load_audio_v2, save_audio, save_audio_v2
from src.preprocessing.speed import decelerate_audio, decelerate_audio_v2
from pydub import AudioSegment
import librosa
import soundfile as sf


# Chemins de fichiers pour les tests
TEST_FILE = "tests/test_audio.wav"
SOURCE_S = "/Users/djiemboutienctheuvictornico/Documents/MyFolders/DevProjects/Contributions/auroreHackaton1812_NLP/data/Yemba_Dataset/audios/speaker_1/group_1/spkr_1_group_1_statement_1.wav"
OUTPUT_FILE = "tests/output_audio.wav"
OUTPUT_FILE_1 = "tests/output_audio_1.wav"


# Fixtures pour pytest
@pytest.fixture
def sample_audio():
    # Crée un fichier audio d'exemple pour les tests
    sr = 44100  # Fréquence d'échantillonnage
    duration = 2  # Durée en secondes
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    y = 0.5 * np.sin(2 * np.pi * 440 * t)  # Signal sinusoïdal
    sf.write(TEST_FILE, y, sr)
    yield TEST_FILE
    os.remove(TEST_FILE)


def test_integration_decelerate_audio(sample_audio):
    # Test d'intégration : charger, ralentir et sauvegarder un fichier audio
    # y, sr = load_audio(SOURCE_S)
    y, sr = load_audio(sample_audio)
    slowed_audio = decelerate_audio(y, slow_factor=0.2)

    # Sauvegarder l'audio ralenti
    save_audio_v2(slowed_audio, OUTPUT_FILE, sr)

    # Vérifier que le fichier de sortie a été créé
    assert os.path.exists(OUTPUT_FILE), "Le fichier de sortie n'a pas été créé"

    # Vérifier que l'audio a été ralenti en comparant les longueurs
    slow_y, slow_sr = load_audio(OUTPUT_FILE)
    assert len(slow_y) > len(y), "L'audio ne doit pas être plus court après ralentissement"

    os.remove(OUTPUT_FILE)


def test_integration_decelerate_audio_v2(sample_audio):
    # Test d'intégration avec la méthode audio v2 (AudioSegment)
    # audio = load_audio_v2(SOURCE_S)
    audio = load_audio_v2(sample_audio)
    slowed_audio = decelerate_audio_v2(audio, slow_factor=0.5)

    # Sauvegarder l'audio ralenti
    save_audio(slowed_audio, OUTPUT_FILE_1)

    # Vérifier que le fichier de sortie a été créé
    assert os.path.exists(OUTPUT_FILE_1), "Le fichier de sortie n'a pas été créé"

    # Vérifier que l'audio a été ralenti
    slow_audio = AudioSegment.from_wav(OUTPUT_FILE_1)
    assert math.ceil(slow_audio.duration_seconds) == math.ceil(audio.duration_seconds)*2, "L'audio ne doit pas être plus court après ralentissement"

    os.remove(OUTPUT_FILE_1)
