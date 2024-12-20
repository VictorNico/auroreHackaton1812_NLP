import pytest
import os
import numpy as np
from src.preprocessing.speed import decelerate_audio, decelerate_audio_v2
from src.utils.io import load_audio, load_audio_v2
from pydub import AudioSegment
import librosa
import soundfile as sf


# Chemin du fichier pour les tests
TEST_FILE = "tests/test_audio.wav"
OUTPUT_FILE = "tests/output_audio.wav"


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


def test_decelerate_audio(sample_audio):
    # Test de la fonction decelerate_audio
    y, sr = load_audio(sample_audio)
    y_slow = decelerate_audio(y, slow_factor=0.5)

    # Vérifier que l'audio ralenti est plus long que l'original
    assert len(y_slow) > len(y), "L'audio ne doit pas être plus court après ralentissement"


def test_decelerate_audio_v2(sample_audio):
    # Test de la fonction decelerate_audio_v2
    audio = load_audio_v2(sample_audio)
    slowed_audio = decelerate_audio_v2(audio, slow_factor=0.5)

    # Vérifier que l'audio ralenti est plus long que l'original
    assert slowed_audio.duration_seconds > audio.duration_seconds, "L'audio ne doit pas être plus court après ralentissement"


def test_decelerate_audio_1(sample_audio):
    # Test de la fonction decelerate_audio
    y, sr = load_audio(sample_audio)
    y_slow = decelerate_audio(y, slow_factor=0.5)

    # Vérifier que l'audio ralenti est plus long que l'original
    assert len(y_slow) > len(y), "L'audio ne doit pas être plus court après ralentissement"


def test_decelerate_audio_v2_1(sample_audio):
    # Test de la fonction decelerate_audio_v2
    audio = load_audio_v2(sample_audio)
    slowed_audio = decelerate_audio_v2(audio, slow_factor=0.5)

    # Vérifier que l'audio ralenti est plus long que l'original
    assert slowed_audio.duration_seconds > audio.duration_seconds, "L'audio ne doit pas être plus court après ralentissement"