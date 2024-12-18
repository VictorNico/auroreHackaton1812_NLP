# auroreHackaton1812_NLP - Projet NLP

## Description
Reconnaissance Vocal de la langue Yemba

**table of content**

- [Prérequis](#Prérequis)
- [Clonage](#Clonage)
- [Usage](#Usage)
- [Installation](#Installation)
- [Configuration](#Configuration)
- [Utilisation](#Utilisation)
- [Structure du Projet](#Structure-du-Projet)
- [Licence](#Licence)
- [Contacts](#Contacts)
- [Remerciements](#Remerciements)
- [Contribution](#Contribution)


## Prérequis
- Python 3.9+
- pip
- virtualenv

## Clonage

- Clone repo with

  ```bash
    git clone git@github.com:VictorNico/auroreHackaton1812_NLP.git aurore
  ```

- Navigate to project with from your terminal

  ```bash
    cd aurore
  ```

## Usage
- Dependencies installation Linux/Mac

```bash
chmod +x setup_nlp_env.sh
./setup_nlp_env.sh
```

- Windows
Executer ``setup_nlp_env.bat``

- requirements checking
```zsh
python check_nlp_env.py
```

## Installation

### Création de l'environnement virtuel
```bash
python3.9 -m venv nlp_env
source nlp_env/bin/activate  # Linux/Mac
# ou 
nlp_env\Scripts\activate  # Windows
```

### Installation des dépendances
```bash
pip install -r requirements.txt
```

## Configuration

### Variables d'environnement
Créez un fichier `.env` avec vos configurations sensibles :
```
API_KEY=votre_clé_api
MODEL_PATH=/chemin/vers/modele
```

## Utilisation

### Lancement du projet
```bash
python main.py
```

### Tests
```bash
pytest tests/
```

## Structure du Projet
```
project_root/
│
├── src/                  # Code source principal
│   ├── models/           # Modèles de ML
│   ├── utils/            # Utilitaires
│   └── preprocessing/    # Prétraitement des données
│
├── notebooks/            # Jupyter notebooks
├── tests/                # Tests unitaires
├── data/                 # Données (ignoré par git)
├── models/               # Modèles sauvegardés
│
├── requirements.txt      # Dépendances
├── README.md             # Ce fichier
└── .gitignore            # Configuration git
```

## Licence
Distribué sous licence Apache 2.

## Contacts
Victor DJIEMBOU - viclegranddab@gmail.com

## Remerciements
- Python
- TensorFlow
- Transformers
- Spacy




## Contribution

- **Git flow**

  - Les branches doivent être nommées avec le format `feature/<task>`.

  - Écrire des commits

    - Les messages de validation doivent suivre le format for mat `#<numéro_d'édition> | <nom_de_l'auteur> | <description_du_travail>`

    - @exemple est `|#1 | @VictorNico | installer la structure du projet|`

    - La numérotation se fait par rapport au numéro de la question sur laquelle vous travaillez.

  - Lors de la création d'un `PR` ;

    - Si ce PR est pour un problème existant, assurez-vous de marquer le problème dans la description du PR, pour fermer automatiquement le problème s'il est approuvé, vous pouvez utiliser n'importe laquelle de ces commandes

      - `Resolves #<numéro_de_problème>`

      - `Fixes #<numéro_de_problème>` ou

      - `Closes #<numéro_de_question>`

  - Attribuez toujours le PR à vous-même et à votre coéquipier.


|
---

**Happy Coding Everyone 🚀**
