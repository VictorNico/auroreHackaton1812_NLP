import librosa
import soundfile as sf

def changer_hauteur_audio(fichier_entree, fichier_sortie, n_steps):
    """
    Applique un changement de hauteur (pitch shifting) à un fichier audio.
    
    Args:
        fichier_entree (str): Chemin du fichier audio d'entrée.
        fichier_sortie (str): Chemin où sauvegarder le fichier audio modifié.
        n_steps (int): Nombre de demi-tons à décaler.
    """
    try:
        y, sr = librosa.load(fichier_entree, sr=None)  # Charger l'audio
        y_shifted = librosa.effects.pitch_shift(y, n_steps=n_steps, sr=sr)  # Appliquer pitch shifting
        sf.write(fichier_sortie, y_shifted, sr)  # Sauvegarder le fichier
    except Exception as e:
        raise RuntimeError(f"Erreur lors du traitement de {fichier_entree}: {e}")
