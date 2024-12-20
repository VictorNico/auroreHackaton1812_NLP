import os
from audio_processing import changer_hauteur_audio

def traiter_fichiers_audio(dossier_principal, dossier_sortie, n_steps):
    """
    Parcourt un dossier principal, applique un traitement de pitch shifting
    sur tous les fichiers audio `.wav`, et sauvegarde dans un dossier de sortie.
    
    Args:
        dossier_principal (str): Dossier contenant les fichiers audio à traiter.
        dossier_sortie (str): Dossier où sauvegarder les fichiers traités.
        n_steps (int): Nombre de demi-tons pour le pitch shifting.
    """
    for racine, _, fichiers in os.walk(dossier_principal):
        for fichier_audio in fichiers:
            if fichier_audio.endswith('.wav'):  # Vérifiez uniquement les fichiers .wav
                fichier_entree = os.path.join(racine, fichier_audio)
                
                # Conserver la structure des dossiers dans le dossier de sortie
                chemin_sortie = os.path.relpath(racine, dossier_principal)
                fichier_sortie = os.path.join(dossier_sortie, chemin_sortie, fichier_audio)
                
                # Créer le dossier de sortie si nécessaire
                os.makedirs(os.path.dirname(fichier_sortie), exist_ok=True)
                
                # Appliquer le pitch shifting
                changer_hauteur_audio(fichier_entree, fichier_sortie, n_steps)
                print(f'Fichier traité : {fichier_entree} -> {fichier_sortie}')
