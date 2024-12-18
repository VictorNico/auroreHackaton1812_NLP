import sys
import platform


def check_environment():
    print("🔍 Vérification de l'environnement NLP")
    print("-" * 40)

    # Informations système
    print(f"Système d'exploitation: {platform.system()}")
    print(f"Version Python: {sys.version}")

    # Vérification des bibliothèques
    libraries = [
        'numpy', 'pandas', 'tensorflow', 'torch',
        'transformers', 'sklearn', 'spacy', 'nltk'
    ]

    print("\n📚 Vérification des bibliothèques:")
    for lib in libraries:
        try:
            __import__(lib)
            print(f"✅ {lib} installé")
        except ImportError:
            print(f"❌ {lib} non installé")

    # Test de base
    import numpy as np
    import tensorflow as tf

    print("\n🧪 Tests de base:")
    print("NumPy Array Test:", np.array([1, 2, 3]))
    print("TensorFlow Version:", tf.__version__)

    # GPU Check (TensorFlow)
    print("\n💻 GPU Configuration:")
    print("TensorFlow GPU Available:", tf.test.is_built_with_cuda())
    print("TensorFlow GPU Devices:", tf.config.list_physical_devices('GPU'))


if __name__ == "__main__":
    check_environment()