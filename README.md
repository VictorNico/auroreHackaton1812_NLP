# auroreHackaton1812_NLP - Projet NLP

## Description
Reconnaissance Vocal de la langue Yemba

## Membres du Projet
<table>
  <thead>
    <tr>
      <th>Profil</th>
      <th>Nom</th>
      <th>Rôle</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><img src="https://avatars.githubusercontent.com/u/50924368?v=4" alt="DJIEMBOU TIENTCHEU Victor Nico" width="50" height="50" style="border-radius: 50%;"></td>
      <td><a href="https://github.com/VictorNico">DJIEMBOU TIENTCHEU Victor Nico</a></td>
      <td>Chef d'équipe et maintaineur, Étudiant chercheur en Science des données, M2, UY1</td>
    </tr>
    <tr>
      <td><img src="https://avatars.githubusercontent.com/u/109069930?v=4" alt="FOTSING ENGOULOU Simon Gaetan" width="50" height="50" style="border-radius: 50%;"></td>
      <td><a href="https://github.com/FESG3002">FOTSING ENGOULOU Simon Gaetan</a></td>
      <td>Collaborateur, Étudiant chercheur en Science des données, M1, UY1</td>
    </tr>
    <tr>
      <td><img src="https://avatars.githubusercontent.com/u/50924368?v=4" alt="LONTSI LAMBOU Ronaldino" width="50" height="50" style="border-radius: 50%;"></td>
      <td><a href="https://github.com/LLontsi">LONTSI LAMBOU Ronaldino</a></td>
      <td>Collaborateur, Étudiant chercheur en Science des données, M1, UY1</td>
    </tr>
    <tr>
      <td><img src="https://avatars.githubusercontent.com/u/167098974?v=4" alt="NOUBISSI FOPA Christian Junior" width="50" height="50" style="border-radius: 50%;"></td>
      <td><a href="https://github.com/NFChristianJ">NOUBISSI FOPA Christian Junior</a></td>
      <td>Collaborateur, Étudiant chercheur en Science des données, M1, UY1</td>
    </tr>
  </tbody>
</table>



## **table of content**

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
- Dependencies installation Linux/Mac

```bash
chmod +x setup_nlp_env.sh
./setup_nlp_env.sh
```

- Windows
Executer ``setup_nlp_env.bat``

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
├── .gitignore            # Configuration git
├── main.py
├── setup_nlp_env.sh       # Pour Linux/Mac
├── setup_nlp_env.bat      # Pour Windows
└── Dockerfile
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

    - @exemple est `|#1 | @VictorNico | installer la sztructure du projet|`

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
