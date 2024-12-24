import os
import wave
import pytest
import shutil
import numpy as np
from pathlib import Path
from src.preprocessing.speedup import change_speed, process_directory

# Constants
TEST_DIR = "testsfiles/folders"
INPUT_DIR = os.path.join(TEST_DIR, "input")
OUTPUT_DIR = os.path.join(TEST_DIR, "output")
TEST_FILE = os.path.join(INPUT_DIR, "test_audio.wav")
TEST_STEREO_FILE = os.path.join(INPUT_DIR, "test_stereo.wav")

def create_test_wav(filename, stereo=False, duration=1, sample_rate=44100):
    """Helper function to create test WAV files."""
    # Créer le dossier parent s'il n'existe pas
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    n_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    if stereo:
        audio_data = np.vstack((
            np.sin(2 * np.pi * 440 * t),
            np.sin(2 * np.pi * 880 * t)
        )).T
        n_channels = 2
    else:
        audio_data = np.sin(2 * np.pi * 440 * t)
        n_channels = 1

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())

def ensure_dir_exists(directory):
    """S'assure qu'un dossier existe, le crée si nécessaire."""
    Path(directory).mkdir(parents=True, exist_ok=True)

def clean_directory(directory):
    """Nettoie un dossier et tous ses contenus."""
    if os.path.exists(directory) and (" " in directory)==False: #verifier qui ya aucune espace dans le destination du fichier
        shutil.rmtree(directory)

@pytest.fixture(autouse=True)
def setup_teardown():
    """Create and clean up test directories."""
    # Nettoyage préalable si les dossiers existent
    clean_directory(TEST_DIR)
    
    # Création des dossiers de test
    ensure_dir_exists(INPUT_DIR)
    ensure_dir_exists(OUTPUT_DIR)
    
    yield
    
    # Nettoyage final
    clean_directory(TEST_DIR)

class TestChangeSpeed:
    @pytest.fixture
    def sample_wav(self):
        """Create a sample mono WAV file."""
        ensure_dir_exists(os.path.dirname(TEST_FILE))
        create_test_wav(TEST_FILE)
        return TEST_FILE

    @pytest.fixture
    def sample_stereo_wav(self):
        """Create a sample stereo WAV file."""
        ensure_dir_exists(os.path.dirname(TEST_STEREO_FILE))
        create_test_wav(TEST_STEREO_FILE, stereo=True)
        return TEST_STEREO_FILE

    def test_change_speed_mono(self, sample_wav):
        """Test speed change on mono file."""
        output_file = os.path.join(OUTPUT_DIR, "output_mono.wav")
        speed_factor = 2.0
        
        assert change_speed(sample_wav, output_file, speed_factor)
        
        # Vérifier le fichier de sortie
        with wave.open(sample_wav, 'rb') as wf_in:
            with wave.open(output_file, 'rb') as wf_out:
                # Vérifier que les paramètres sont conservés
                assert wf_in.getnchannels() == wf_out.getnchannels()
                assert wf_in.getsampwidth() == wf_out.getsampwidth()
                assert wf_in.getframerate() == wf_out.getframerate()
                # Vérifier que la durée est divisée par 2
                assert wf_out.getnframes() == int(wf_in.getnframes() / speed_factor)

    def test_change_speed_stereo(self, sample_stereo_wav):
        """Test speed change on stereo file."""
        ensure_dir_exists(OUTPUT_DIR)
        output_file = os.path.join(OUTPUT_DIR, "output_stereo.wav")
        speed_factor = 0.5
        
        assert change_speed(sample_stereo_wav, output_file, speed_factor)
        
        with wave.open(sample_stereo_wav, 'rb') as wf_in:
            with wave.open(output_file, 'rb') as wf_out:
                assert wf_out.getnchannels() == 2
                assert wf_out.getnframes() == int(wf_in.getnframes() / speed_factor)

    @pytest.mark.parametrize("speed_factor", [-1.0, 0.0])
    def test_change_speed_invalid_factors(self, sample_wav, speed_factor):
        """Test avec des facteurs de vitesse invalides."""
        ensure_dir_exists(OUTPUT_DIR)
        output_file = os.path.join(OUTPUT_DIR, "output_invalid.wav")
        result = change_speed(sample_wav, output_file, speed_factor)
        assert not result or not os.path.exists(output_file)

    def test_change_speed_nonexistent_file(self):
        """Test avec un fichier d'entrée inexistant."""
        ensure_dir_exists(OUTPUT_DIR)
        result = change_speed("nonexistent.wav", os.path.join(OUTPUT_DIR, "output.wav"), 1.5)
        assert not result

class TestProcessDirectory:
    def setup_test_files(self, num_files=3):
        """Helper to create multiple test files."""
        ensure_dir_exists(INPUT_DIR)
        for i in range(num_files):
            create_test_wav(os.path.join(INPUT_DIR, f"test_{i}.wav"))
            if i % 2 == 0:  # Créer quelques fichiers stéréo
                create_test_wav(os.path.join(INPUT_DIR, f"test_stereo_{i}.wav"), stereo=True)

    def test_process_directory_basic(self):
        """Test basique du traitement de dossier."""
        self.setup_test_files(3)
        speed_factor = 1.5
        
        process_directory(INPUT_DIR, OUTPUT_DIR, speed_factor)
        
        # Vérifier que tous les fichiers WAV ont été traités
        input_wavs = [f for f in os.listdir(INPUT_DIR) if f.endswith('.wav')]
        output_wavs = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.wav')]
        assert len(output_wavs) == len(input_wavs)
        
        # Vérifier le format des noms de fichiers de sortie
        for file in output_wavs:
            assert f"_{int(speed_factor*100)}percent.wav" in file

    def test_process_directory_empty(self):
        """Test avec un dossier vide."""
        ensure_dir_exists(INPUT_DIR)
        ensure_dir_exists(OUTPUT_DIR)
        process_directory(INPUT_DIR, OUTPUT_DIR, 1.5)
        assert len(os.listdir(OUTPUT_DIR)) == 0

    def test_process_directory_non_wav_files(self):
        """Test avec des fichiers non-WAV dans le dossier."""
        self.setup_test_files(2)
        
        # Créer un fichier non-WAV
        non_wav_file = os.path.join(INPUT_DIR, "test.txt")
        with open(non_wav_file, 'w') as f:
            f.write("Not a WAV file")
            
        process_directory(INPUT_DIR, OUTPUT_DIR, 1.5)
        
        input_wavs = [f for f in os.listdir(INPUT_DIR) if f.endswith('.wav')]
        output_wavs = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.wav')]
        assert len(output_wavs) == len(input_wavs)

    def test_process_directory_nonexistent_input(self):
        """Test avec un dossier d'entrée inexistant."""
        nonexistent_dir = os.path.join(TEST_DIR, "nonexistent")
        ensure_dir_exists(OUTPUT_DIR)
        
        # Le dossier d'entrée sera créé automatiquement
        process_directory(nonexistent_dir, OUTPUT_DIR, 1.5)
        
        # Vérifier que le dossier a été créé
        assert os.path.exists(nonexistent_dir)
        assert len(os.listdir(OUTPUT_DIR)) == 0

    def test_process_directory_create_output(self):
        """Test de la création automatique du dossier de sortie."""
        self.setup_test_files(1)
        output_dir = os.path.join(TEST_DIR, "new_output")
        
        process_directory(INPUT_DIR, output_dir, 1.5)
        
        assert os.path.exists(output_dir)
        assert len(os.listdir(output_dir)) > 0