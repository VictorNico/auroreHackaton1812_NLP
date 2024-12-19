import os
import pytest
from src.utils.io import load_audio, load_audio_v2, save_audio, save_audio_v2
from pydub import AudioSegment
import librosa
import numpy as np
import soundfile as sf

# Chemins de fichiers pour les tests
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

def test_load_audio(sample_audio):
    # Test de la fonction load_audio
    y, sr = load_audio(sample_audio)
    assert len(y) > 0, "L'audio chargé est vide"
    assert sr > 0, "Fréquence d'échantillonnage incorrecte"

def test_load_audio_v2(sample_audio):
    # Test de la fonction load_audio_v2
    audio = load_audio_v2(sample_audio)
    assert isinstance(audio, AudioSegment), "L'objet retourné n'est pas un AudioSegment"
    assert audio.frame_rate > 0, "Frame rate incorrect"

def test_save_audio(sample_audio):
    # Test de la fonction save_audio
    audio = load_audio_v2(sample_audio)
    save_audio(audio, OUTPUT_FILE)
    assert os.path.exists(OUTPUT_FILE), "Le fichier de sortie n'a pas été créé"
    os.remove(OUTPUT_FILE)

def test_save_audio_v2(sample_audio):
    # Test de la fonction save_audio_v2
    y, sr = load_audio(sample_audio)
    save_audio_v2(y, OUTPUT_FILE, sr)
    assert os.path.exists(OUTPUT_FILE), "Le fichier de sortie n'a pas été créé"
    os.remove(OUTPUT_FILE)
