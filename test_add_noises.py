import os
import numpy as np
import soundfile as sf

def charger_audio(filepath):
    """
    Charge un fichier audio.

    :param filepath: Chemin vers le fichier audio
    :return: Signal audio et fréquence d'échantillonnage
    """
    audio, fs = sf.read(filepath)
    return audio, fs

def verifier_bruit(original_audio, modifie_audio, seuil_diff):
    """
    Vérifie si du bruit a été ajouté en comparant les signaux audio originaux et modifiés.

    :param original_audio: Signal audio original
    :param modifie_audio: Signal audio modifié
    :param seuil_diff: Seuil de différence pour considérer qu'il y a du bruit
    :return: True si du bruit a été ajouté, sinon False
    """
    difference = np.mean(np.abs(original_audio - modifie_audio))
    return difference > seuil_diff

def tester_ajout_bruit(input_dir, output_dir, seuil_diff=0.01):
    """
    Teste tous les fichiers audio dans un répertoire pour vérifier l'ajout de bruit.

    :param input_dir: Répertoire contenant les fichiers audio originaux
    :param output_dir: Répertoire contenant les fichiers audio modifiés
    :param seuil_diff: Seuil de différence pour considérer qu'il y a du bruit
    """
    fichiers_non_bruites = []

    for filename in os.listdir(input_dir):
        if filename.endswith('.wav'):
            original_filepath = os.path.join(input_dir, filename)
            modifie_filepath = os.path.join(output_dir, filename)

            original_audio, fs = charger_audio(original_filepath)
            modifie_audio, _ = charger_audio(modifie_filepath)

            bruit_ajoute = verifier_bruit(original_audio, modifie_audio, seuil_diff)
            if not bruit_ajoute:
                fichiers_non_bruites.append(filename)

    if not fichiers_non_bruites:
        print("Le bruit a été ajouté à tous les fichiers.")
    else:
        print("Le bruit n'a pas été ajouté aux fichiers suivants :")
        for fichier in fichiers_non_bruites:
            print(f"- {fichier}")

def main():
    # Répertoire des fichiers audio originaux
    input_dir = r'C:\Users\Christian\Desktop\hackathon\Nouveau dossier'
    
    # Répertoire des fichiers audio modifiés
    output_dir = r'C:\Users\Christian\Desktop\hackathon\Nouveau dossier (2)'

    # Appeler la fonction de test
    tester_ajout_bruit(input_dir, output_dir)

if __name__ == "__main__":
    main()
