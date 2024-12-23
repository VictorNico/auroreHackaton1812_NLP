import numpy as np
import os
import shutil
import soundfile as sf

def ajouter_bruit(audio, snr_db):
    """
    Ajoute du bruit à un signal audio en fonction d'un rapport signal-bruit spécifié (SNR).

    :param audio: Signal audio original
    :param snr_db: Rapport signal-bruit en dB
    :return: Signal audio avec bruit ajouté
    """
    # Si l'audio est stéréo, alors on traite chaque canal séparément
    if audio.ndim == 2:
        audio_bruite = np.zeros_like(audio)
        for i in range(audio.shape[1]):
            signal_power = np.mean(audio[:, i]**2)
            snr_linear = 10**(snr_db / 10)
            noise_power = signal_power / snr_linear

            bruit = np.sqrt(noise_power) * np.random.randn(len(audio[:, i]))
            audio_bruite[:, i] = audio[:, i] + bruit
    else:
        signal_power = np.mean(audio**2)
        snr_linear = 10**(snr_db / 10)
        noise_power = signal_power / snr_linear

        bruit = np.sqrt(noise_power) * np.random.randn(len(audio))
        audio_bruite = audio + bruit
    
    return audio_bruite

def charger_audio(filepath):
    """
    Charge un fichier audio.

    :param filepath: Chemin vers le fichier audio
    :return: Signal audio et fréquence d'échantillonnage
    """
    audio, fs = sf.read(filepath)
    return audio, fs

def sauvegarder_audio(filepath, audio, fs):
    """
    Sauvegarde un fichier audio.

    :param filepath: Chemin vers le fichier de sauvegarde
    :param audio: Signal audio
    :param fs: Fréquence d'échantillonnage
    """
    sf.write(filepath, audio, fs)

def traiter_repertoire(input_dir, output_dir, niveau_bruit, sauvegarder=False):
    """
    Traite tous les fichiers audio dans un répertoire, ajoute du bruit et sauvegarde les fichiers modifiés.

    :param input_dir: Répertoire contenant les fichiers audio originaux
    :param output_dir: Répertoire où sauvegarder les fichiers audio modifiés
    :param niveau_bruit: Niveau de bruit à ajouter (SNR en dB)
    :param sauvegarder: Booléen indiquant si les fichiers modifiés doivent être sauvegardés
    """
    if sauvegarder and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.wav'):
            input_filepath = os.path.join(input_dir, filename)
            output_filepath = os.path.join(output_dir, filename)

            audio, fs = charger_audio(input_filepath)
            audio_bruite = ajouter_bruit(audio, niveau_bruit)
            
            if sauvegarder:
                sauvegarder_audio(output_filepath, audio_bruite, fs)
                print(f"Fichier traité et sauvegardé : {filename}")
            else:
                print(f"Fichier traité : {filename}")

def verifier_bruit(original_audio, modifie_audio, seuil_diff): 
    """ Vérifie si du bruit a été ajouté en comparant les signaux audio originaux et modifiés. 
    :param original_audio: Signal audio original 
    :param modifie_audio: Signal audio modifié 
    :param seuil_diff: Seuil de différence pour considérer qu'il y a du bruit :return: True si du bruit a été ajouté, sinon False """ 
    difference = np.mean(np.abs(original_audio - modifie_audio)) 
    return difference > seuil_diff