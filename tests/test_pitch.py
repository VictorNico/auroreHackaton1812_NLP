import os
import unittest
from src.preprocessing.pitch import changer_hauteur_audio
import soundfile as sf
import librosa
import pytest

class TestAudioProcessing(unittest.TestCase):
    def setUp(self):
        """
        Prépare un fichier audio temporaire pour les tests.
        """
        self.fichier_entree = "test_input.wav"
        self.fichier_sortie = "test_output.wav"
        self.n_steps = 2

        # Générer un fichier audio temporaire
        sr = 22050  # Fréquence d'échantillonnage
        duration = 1.0  # Durée en secondes
        tone = (440.0, )  # Fréquence du ton en Hz
        sf.write(self.fichier_entree, librosa.tone(tone[0], sr=sr, duration=duration), sr)

    def tearDown(self):
        """
        Supprime les fichiers créés après les tests.
        """
        if os.path.exists(self.fichier_entree):
            os.remove(self.fichier_entree)
        if os.path.exists(self.fichier_sortie):
            os.remove(self.fichier_sortie)

    def test_changer_hauteur_audio(self):
        """
        Teste si la fonction modifie correctement l'audio.
        """
        changer_hauteur_audio(self.fichier_entree, self.fichier_sortie, self.n_steps)

        # Vérifier si le fichier de sortie a été créé
        self.assertTrue(os.path.exists(self.fichier_sortie))

        # Charger le fichier de sortie
        y_orig, sr_orig = librosa.load(self.fichier_entree, sr=None)
        y_mod, sr_mod = librosa.load(self.fichier_sortie, sr=None)

        # Vérifier si la hauteur a changé
        self.assertEqual(sr_orig, sr_mod)
        self.assertNotEqual(y_orig.tolist(), y_mod.tolist())  # Les données doivent être différentes

if __name__ == "__main__":
    unittest.main()
