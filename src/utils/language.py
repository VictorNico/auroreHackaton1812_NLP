"""
Module Langage du modèle

Auteur : Victor Nico
Version : 1.0.0
Date de création : 2024-12-21

Module de construction du langage compris par le modèle.

Ce module inclut des fonctionnalités pour preparer et créer un dictionnaire d'alphabet tels que :
- suppression des caractère speciaux


Exemple de la suppression de caractère speciaux :
    from src.utils.language import remove_special_characters
    ...
    common_voice_train = common_voice_train.map(remove_special_characters)
    common_voice_test = common_voice_test.map(remove_special_characters)
    # Où common_voice_train et common_voice_test, sont les dataframe dataset pour le jeu de train et de test.

Exemple de remplacement de caractère avec signe :
    from src.utils.language import replace_hatted_characters
    ...
    common_voice_train = common_voice_train.map(replace_hatted_characters)
    common_voice_test = common_voice_test.map(replace_hatted_characters)
    # Où common_voice_train et common_voice_test, sont les dataframe dataset pour le jeu de train et de test.

Exemple d'extraction des caractères' :
    from src.utils.language import extract_all_chars
    ...
    vocab_train = common_voice_train.map(extract_all_chars, batched=True, batch_size=-1, keep_in_memory=True, remove_columns=common_voice_train.column_names)
    vocab_test = common_voice_test.map(extract_all_chars, batched=True, batch_size=-1, keep_in_memory=True, remove_columns=common_voice_test.column_names)

    vocab_list = list(set(vocab_train["vocab"][0]) | set(vocab_test["vocab"][0]))

    vocab_dict = {v: k for k, v in enumerate(sorted(vocab_list))}
    # Où common_voice_train et common_voice_test, sont les dataframe dataset pour le jeu de train et de test.

"""

__author__ = "Victor Nico"
__version__ = "1.0.0"
__date__ = "2024-12-21"

import re
chars_to_remove_regex = '[\,\?\.\!\-\;\:\"\“\%\‘\”\�\']'

def remove_special_characters(batch):
    batch["sentence"] = re.sub(chars_to_remove_regex, '', batch["sentence"]).lower()
    return batch


def replace_hatted_characters(batch):
    batch["sentence"] = re.sub('[â]', 'a', batch["sentence"])
    batch["sentence"] = re.sub('[î]', 'i', batch["sentence"])
    batch["sentence"] = re.sub('[ô]', 'o', batch["sentence"])
    batch["sentence"] = re.sub('[û]', 'u', batch["sentence"])
    return batch

def extract_all_chars(batch):
  all_text = " ".join(batch["sentence"])
  vocab = list(set(all_text))
  return {"vocab": [vocab], "all_text": [all_text]}