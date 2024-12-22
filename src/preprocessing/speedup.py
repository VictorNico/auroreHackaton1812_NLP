from ..utils.lib import *

def change_speed(input_file, output_file, speed_factor):
    """
    Change la vitesse d'un fichier WAV.
    
    Parameters:
    input_file (str): Chemin du fichier WAV d'entrée
    output_file (str): Chemin du fichier WAV de sortie
    speed_factor (float): Facteur de multiplication de la vitesse
                         (0.5 = vitesse divisée par 2, 2.0 = vitesse doublée)
    """
    try:
        with wave.open(input_file, 'rb') as wf:
            # Obtenir les paramètres du fichier
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            
            # Lire tous les frames
            frames = wf.readframes(n_frames)
            
            # Convertir les frames en tableau numpy
            signal = np.frombuffer(frames, dtype=np.int16)
            
            # Remodeler le signal si stéréo
            if n_channels == 2:
                signal = signal.reshape(-1, 2)
            
            # Calculer le nombre de frames à conserver
            new_length = int(len(signal) / speed_factor)
            
            # Rééchantillonner le signal
            indices = np.round(np.linspace(0, len(signal) - 1, new_length)).astype(int)
            new_signal = signal[indices]
            
            # Écrire le signal modifié dans le fichier de sortie
            with wave.open(output_file, 'wb') as wf_out:
                wf_out.setnchannels(n_channels)
                wf_out.setsampwidth(sampwidth)
                wf_out.setframerate(framerate)
                wf_out.writeframes(new_signal.tobytes())
        return True
    except Exception as e:
        print(f"Erreur lors du traitement de {input_file}: {str(e)}")
        return False
    
    
def process_directory(input_dir, output_dir, speed_factor):
    """
    Traite tous les fichiers WAV dans un dossier.
    
    Parameters:
    input_dir (str): Chemin du dossier contenant les fichiers WAV
    output_dir (str): Chemin du dossier où sauvegarder les fichiers modifiés
    speed_factor (float): Facteur de multiplication de la vitesse
    """
    # Créer le dossier de sortie s'il n'existe pas
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(input_dir).mkdir(parents=True, exist_ok=True)
    
    # Compteurs pour le suivi
    total_files = 0
    successful_files = 0
    
    # Parcourir tous les fichiers WAV du dossier
    for file in os.listdir(input_dir):
        if file.lower().endswith('.wav'):
            total_files += 1
            input_path = os.path.join(input_dir, file)
            # Créer le nom du fichier de sortie avec indication de la vitesse
            speed_indicator = f"_{int(speed_factor*100)}percent"
            output_filename = file.rsplit('.', 1)[0] + speed_indicator + '.wav'
            output_path = os.path.join(output_dir, output_filename)
            
            print(f"Traitement de: {file}")
            if change_speed(input_path, output_path, speed_factor):
                successful_files += 1
    
    # Afficher le résumé
    print(f"\nRésumé du traitement:")
    print(f"Fichiers traités: {successful_files}/{total_files}")
    if total_files > 0:
        print(f"Taux de réussite: {(successful_files/total_files)*100:.1f}%")