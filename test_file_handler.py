import os
import unittest
from file_handler import traiter_fichiers_audio
from audio_processing import changer_hauteur_audio
import soundfile as sf
import librosa

class TestFileHandler(unittest.TestCase):
    def setUp(self):
        """
        Prépare un dossier temporaire avec des fichiers audio.
        """
        self.dossier_principal = "test_input_folder"
        self.dossier_sortie = "test_output_folder"
        self.n_steps = 3

        # Créer le dossier principal
        os.makedirs(self.dossier_principal, exist_ok=True)

        # Ajouter des fichiers audio
        self.fichier_audio1 = os.path.join(self.dossier_principal, "audio1.wav")
        self.fichier_audio2 = os.path.join(self.dossier_principal, "audio2.wav")
        sr = 22050
        sf.write(self.fichier_audio1, librosa.tone(440.0, sr=sr, duration=1.0), sr)
        sf.write(self.fichier_audio2, librosa.tone(880.0, sr=sr, duration=1.0), sr)

    def tearDown(self):
        """
        Supprime les fichiers et dossiers créés après les tests.
        """
        for dossier in [self.dossier_principal, self.dossier_sortie]:
            if os.path.exists(dossier):
                for racine, _, fichiers in os.walk(dossier, topdown=False):
                    for fichier in fichiers:
                        os.remove(os.path.join(racine, fichier))
                    os.rmdir(racine)

    def test_traiter_fichiers_audio(self):
        """
        Teste si tous les fichiers audio sont correctement traités et sauvegardés.
        """
        traiter_fichiers_audio(self.dossier_principal, self.dossier_sortie, self.n_steps)

        # Vérifier si les fichiers de sortie existent
        sortie1 = os.path.join(self.dossier_sortie, "audio1.wav")
        sortie2 = os.path.join(self.dossier_sortie, "audio2.wav")
        self.assertTrue(os.path.exists(sortie1))
        self.assertTrue(os.path.exists(sortie2))

if __name__ == "__main__":
    unittest.main()
