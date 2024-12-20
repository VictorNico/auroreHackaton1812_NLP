# Contributing to [Nom du projet]

Nous sommes ravis que vous souhaitiez contribuer à notre projet ! Avant de commencer, veuillez lire ces lignes directrices pour que le processus se passe bien.

## Comment contribuer

### Signaler un bug
Si vous trouvez un bug, veuillez ouvrir un problème en utilisant le modèle de bug fourni. Décrivez le problème de manière détaillée pour que nous puissions le reproduire facilement.

### Soumettre une fonctionnalité
Si vous souhaitez proposer une nouvelle fonctionnalité, ouvrez une "issue" pour en discuter d'abord. Nous voulons nous assurer que nous comprenons bien la fonctionnalité avant de commencer à coder.

### Soumettre un pull request
1. Choisir une tache das l'obglet issues
2. ``creer une branche`` en blue en bas à droite
3. ``creer`` le bouton bleu
4. Copiez la commande fournie
5. Collez locallement pour créer la branche aussocié à l'issue
6. Faites vos modifications et ajoutez-les à votre commit avec : `git commit -am '#<numéro_d'édition> | <nom_de_l'auteur> | <description_du_travail>'`.
7. Poussez vos modifications : `git push`.
8. Créez une pull request dans la branche principale du dépôt.

### Code de conduite
Nous attendons de tous les contributeurs qu'ils se comportent de manière respectueuse et professionnelle. Toute forme de harcèlement ou d'intolérance ne sera pas tolérée.

## Tests
Avant de soumettre votre pull request, assurez-vous que tous les tests passent en local. Si nécessaire, ajoutez de nouveaux tests pour vos fonctionnalités ou corrections.

Pour exécuter les tests, vous pouvez utiliser la commande suivante :
```bash
pytest tests --junit-xml=tests/reports/reports.yml
```
