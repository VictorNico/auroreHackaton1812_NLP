import logging
import argparse
import re
import sys
import os
from tqdm import tqdm  # Import de tqdm pour les barres de progression
import importlib
import pandas as pd
from datasets import Dataset, concatenate_datasets
from sklearn.model_selection import train_test_split
import json
from transformers import Wav2Vec2CTCTokenizer, Wav2Vec2ForCTC, Wav2Vec2Processor, Trainer, TrainingArguments, \
    Wav2Vec2FeatureExtractor
import soundfile as sf
import numpy as np
import random

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
import torch
from evaluate import load

os.environ['WANDB_DISABLED '] = 'True'

wer_metric = load("wer")
# Ajouter le répertoire racine du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nlp_project.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Dictionnaire pour stocker les modules importés
imported_modules = {}

# Constate utilisé dans le projet

YEMBA_TONE_ROOT_AUDIO = './data/Yemba_Dataset/'
YEMBA_ROOT_AUDIO = './data/YembaEGRA/'
YEMBA_META = './data/YembaEGRA/metadata/words_corpus.csv'
YEMBA_TONE_META = './data/Yemba_Dataset/metadata/isolated_words_dictionary.xlsx'

"""
    class definition
    
"""


@dataclass
class DataCollatorCTCWithPadding:
    """
    Data collator that will dynamically pad the inputs received.
    Args:
        processor (:class:`~transformers.Wav2Vec2Processor`)
            The processor used for proccessing the data.
        padding (:obj:`bool`, :obj:`str` or :class:`~transformers.tokenization_utils_base.PaddingStrategy`, `optional`, defaults to :obj:`True`):
            Select a strategy to pad the returned sequences (according to the model's padding side and padding index)
            among:
            * :obj:`True` or :obj:`'longest'`: Pad to the longest sequence in the batch (or no padding if only a single
              sequence if provided).
            * :obj:`'max_length'`: Pad to a maximum length specified with the argument :obj:`max_length` or to the
              maximum acceptable input length for the model if that argument is not provided.
            * :obj:`False` or :obj:`'do_not_pad'` (default): No padding (i.e., can output a batch with sequences of
              different lengths).
        max_length (:obj:`int`, `optional`):
            Maximum length of the ``input_values`` of the returned list and optionally padding length (see above).
        max_length_labels (:obj:`int`, `optional`):
            Maximum length of the ``labels`` returned list and optionally padding length (see above).
        pad_to_multiple_of (:obj:`int`, `optional`):
            If set will pad the sequence to a multiple of the provided value.
            This is especially useful to enable the use of Tensor Cores on NVIDIA hardware with compute capability >=
            7.5 (Volta).
    """

    processor: Wav2Vec2Processor
    padding: Union[bool, str] = True
    max_length: Optional[int] = None
    max_length_labels: Optional[int] = None
    pad_to_multiple_of: Optional[int] = None
    pad_to_multiple_of_labels: Optional[int] = None

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        # split inputs and labels since they have to be of different lenghts and need
        # different padding methods
        input_features = [{"input_values": feature["input_values"]} for feature in features]
        label_features = [{"input_ids": feature["labels"]} for feature in features]

        batch = self.processor.pad(
            input_features,
            padding=self.padding,
            max_length=self.max_length,
            pad_to_multiple_of=self.pad_to_multiple_of,
            return_tensors="pt",
        )
        labels_batch = self.processor.pad(
            label_features,
            padding=self.padding,
            max_length=self.max_length_labels,
            pad_to_multiple_of=self.pad_to_multiple_of_labels,
            return_tensors="pt",
        )

        # replace padding with -100 to ignore loss correctly
        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)

        batch["labels"] = labels

        return batch


###################


def speech_file_to_array_fn(batch):
    speech_array, sampling_rate = sf.read(batch["path"])
    batch["speech"] = speech_array
    batch["sampling_rate"] = 16000
    batch["target_text"] = batch["sentence"]
    return batch


def load_modules(module_list):
    """
    Charge les modules à partir d'une liste en affichant une barre de progression
    """
    global imported_modules
    logger.info("Début du chargement des modules")
    # Charger les bibliothèques en utilisant importlib
    with tqdm(module_list, total=len(module_list), desc="Chargement des modules", unit="module") as pbar:
        for module_name in module_list:
            try:
                # exec(f'from {module_name} import * as {module_name.split(".")[-1]}')
                # Importer dynamiquement le module
                module = importlib.import_module(module_name)
                # Stocker le module dans un dictionnaire global
                imported_modules[module_name] = module
                # Succès lors du chargement de la bibliothèque
                pbar.set_description(f"Module {module_name} chargé avec succès.")
                # logger.info(f"Module {module_name} chargé avec succès.")
                pbar.update(1)
            except ImportError as e:
                # En cas d'erreur lors du chargement de la bibliothèque
                pbar.set_description(f"Erreur lors du chargement du module {module_name}: {e}")
                logger.error(f"Erreur lors du chargement du module {module_name}: {e}")
            # else:
            #
            # finally:
        pbar.set_description(f"Module terminé avec succès.")
        #     logger.info("Fin du chargement des modules")


def load_configuration():
    """
    Charge la configuration du projet
    """
    try:
        config = {
            'model_path': os.getenv('MODEL_PATH', 'models/default_model'),
            'data_path': os.getenv('DATA_PATH', 'data/'),
        }
        return config
    except Exception as e:
        logger.error(f"Erreur de chargement de la configuration : {e}")
        sys.exit(1)


def main(args):
    """
    Fonction principale du projet NLP
    """
    try:
        # Configuration
        config = load_configuration()
        logger.info("Configuration chargée avec succès")

        # Exemple de modules à charger
        modules_to_load = [
            'src.preprocessing.speedminus',
            'src.preprocessing.pitch',
            'src.preprocessing.speedup',
            'src.utils.io',
            'src.utils.language',
        ]

        # Chargement des modules avec tqdm pour afficher la progression
        load_modules(modules_to_load)

        # Load audios couple with the word associate
        files_registry = build_dataset(
            YEMBA_TONE_ROOT_AUDIO,
            YEMBA_TONE_META,
            pd.DataFrame(columns=['path', 'sentence']),
            'Yemba',
            'audios')

        logger.info(f'{len(files_registry)} files')
        files_registry = build_dataset(
            YEMBA_ROOT_AUDIO,
            YEMBA_META,
            files_registry,
            'Yemba',
            'audio')
        logger.info(f'{len(files_registry)} files')
        # convert into Dataset
        train, test = train_test_split(files_registry[:5], test_size=0.008, random_state=42)
        common_voice_train_1 = Dataset.from_pandas(train[int(len(train) / 2):])
        common_voice_train_2 = Dataset.from_pandas(train[0:int(len(train) / 2)])
        common_voice_test = Dataset.from_pandas(test)

        # remove special caracters
        if 'src.utils.language' in imported_modules:
            module_speed = imported_modules['src.utils.language']
            if hasattr(module_speed, 'remove_special_characters'):
                common_voice_train_1 = common_voice_train_1.map(module_speed.remove_special_characters)
                common_voice_train_2 = common_voice_train_2.map(module_speed.remove_special_characters)
                common_voice_test = common_voice_test.map(module_speed.remove_special_characters)
            else:
                logger.error("La fonction 'remove_special_characters' n'existe pas dans le module.")

        # count special caracters
        if 'src.utils.language' in imported_modules:
            module_speed = imported_modules['src.utils.language']
            if hasattr(module_speed, 'extract_all_chars'):
                vocab_train_1 = common_voice_train_1.map(
                    module_speed.extract_all_chars,
                    batched=True,
                    batch_size=-1,
                    keep_in_memory=True,
                    remove_columns=common_voice_train_2.column_names)
                vocab_train_2 = common_voice_train_2.map(
                    module_speed.extract_all_chars,
                    batched=True,
                    batch_size=-1,
                    keep_in_memory=True,
                    remove_columns=common_voice_train_2.column_names)
                vocab_test = common_voice_test.map(
                    module_speed.extract_all_chars,
                    batched=True,
                    batch_size=-1,
                    keep_in_memory=True,
                    remove_columns=common_voice_train_2.column_names)
            else:
                logger.error("La fonction 'extract_all_chars' n'existe pas dans le module.")

        vocab_list = list(set(vocab_train_2["vocab"][0]) | set(vocab_train_1["vocab"][0]) | set(vocab_test["vocab"][0]))
        logger.info(f'Vocabularies: {vocab_list}')

        vocab_dict = {v: k for k, v in enumerate(vocab_list)}
        logger.info(vocab_dict)
        vocab_dict["|"] = vocab_dict[" "]
        del vocab_dict[" "]
        vocab_dict["[UNK]"] = len(vocab_dict)  # unknown token
        vocab_dict["[PAD]"] = len(vocab_dict)  # epselon du language
        logger.info(f'Vocabularies: {len(vocab_dict)}')

        with open('vocab.json', 'w') as vocab_file:
            json.dump(vocab_dict, vocab_file)

        # creation of CTC
        tokenizer = Wav2Vec2CTCTokenizer("./vocab.json", unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")

        # start finetuning
        feature_extractor = Wav2Vec2FeatureExtractor(
            feature_size=1,
            sampling_rate=16000,
            padding_value=0.0,
            do_normalize=True,
            return_attention_mask=True)
        logger.info(f'sampling rate {feature_extractor.sampling_rate}')

        # build processor
        processor = Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)
        processor.save_pretrained("./Victor/wav2vec2-large-xlsr-Yemba")

        # convert speech file to array
        common_voice_train_1 = common_voice_train_1.map(speech_file_to_array_fn,
                                                        remove_columns=common_voice_train_1.column_names, num_proc=4)
        common_voice_train_2 = common_voice_train_2.map(speech_file_to_array_fn,
                                                        remove_columns=common_voice_train_2.column_names, num_proc=4)

        common_voice_test = common_voice_test.map(speech_file_to_array_fn,
                                                  remove_columns=common_voice_test.column_names, num_proc=4)
        # try to see what are new data for each row
        rand_int = random.randint(0, len(common_voice_train_1) - 1)
        logger.info(f'Random int: {rand_int}')
        logger.info(common_voice_train_1)

        logger.info(f'"Target text:", {common_voice_train_1[rand_int]["target_text"]}')
        logger.info(f'"Input array shape:", {np.asarray(common_voice_train_1[rand_int]["speech"]).shape}')
        logger.info(f'"Sampling rate:", {common_voice_train_1[rand_int]["sampling_rate"]}')

        # prepare data
        def prepare_dataset(batch):
            # check that all files have the correct sampling rate
            assert (
                    len(set(batch["sampling_rate"])) == 1
            ), f"Make sure all inputs have the same sampling rate of {processor.feature_extractor.sampling_rate}."

            batch["input_values"] = processor(batch["speech"], sampling_rate=batch["sampling_rate"][0], padding=True).input_values

            batch["labels"] = processor(text=batch["target_text"]).input_ids
            return batch

        logger.info(f'{common_voice_train_1.shape, common_voice_test.shape}')

        common_voice_train_1 = common_voice_train_1.map(prepare_dataset,
                                                        remove_columns=common_voice_train_1.column_names, batch_size=16,
                                                        num_proc=4, batched=True)
        common_voice_train_2 = common_voice_train_2.map(prepare_dataset,
                                                        remove_columns=common_voice_train_2.column_names, batch_size=16,
                                                        num_proc=4, batched=True)

        # from datasets import concatenate_datasets

        common_voice_train = concatenate_datasets([common_voice_train_1, common_voice_train_2])
        data_collator = DataCollatorCTCWithPadding(processor=processor, padding=True)

        # prediction
        def compute_metrics(pred):
            pred_logits = pred.predictions
            pred_ids = np.argmax(pred_logits, axis=-1)

            pred.label_ids[pred.label_ids == -100] = processor.tokenizer.pad_token_id

            pred_str = processor.batch_decode(pred_ids)
            # we do not want to group tokens when computing the metrics
            label_str = processor.batch_decode(pred.label_ids, group_tokens=False)

            wer = wer_metric.compute(predictions=pred_str, references=label_str)

            return {"wer": wer}

        logger.info(
            f'Computing metrics for {common_voice_train.shape}, {common_voice_test.shape}; {len(processor.tokenizer)}')

        model = Wav2Vec2ForCTC.from_pretrained(
            "./src/models/wav2vec2-xls-r-300m",
            attention_dropout=0.1,
            hidden_dropout=0.1,
            feat_proj_dropout=0.0,
            mask_time_prob=0.05,
            layerdrop=0.1,
            gradient_checkpointing=True,
            ctc_loss_reduction="mean",
            pad_token_id=processor.tokenizer.pad_token_id,
            vocab_size=len(processor.tokenizer),
            ignore_mismatched_sizes=True
        )

        model.freeze_feature_encoder()

        training_args = TrainingArguments(
            output_dir="./models/wav2vec2-large-xlsr-Yemba",
            run_name="yemba_asr",
            group_by_length=True,
            per_device_train_batch_size=16,
            gradient_accumulation_steps=2,
            eval_strategy="steps",
            num_train_epochs=40,
            fp16=False,
            save_steps=500,
            eval_steps=500,
            logging_steps=500,
            learning_rate=3e-4,
            warmup_steps=1000,
            save_total_limit=2,
            push_to_hub=False
        )

        trainer = Trainer(
            model=model,
            data_collator=data_collator,
            args=training_args,
            compute_metrics=compute_metrics,
            train_dataset=common_voice_train,
            eval_dataset=common_voice_test,
            processing_class=processor
        )

        logger.info(f'{common_voice_train.shape}')

        os.environ['WANDB_MODE'] = 'dryrun'
        os.environ['WANDB_DISABLED '] = 'True'

        trainer.train()

        # Votre logique principale ici
        if args.mode == 'train':
            train_model(config)
        elif args.mode == 'predict':
            predict(config)
        else:
            logger.warning(f"Mode non reconnu : {args.mode}")

    except Exception as e:
        logger.error(f"Erreur fatale : {e}")
        sys.exit(1)


def train_model(config):
    """
    Entraînement du modèle NLP
    """
    logger.info("Début de l'entraînement du modèle")
    # Votre code d'entraînement ici


def predict(config):
    """
    Prédiction avec le modèle
    """
    logger.info("Début de la prédiction")
    # Votre code de prédiction ici


def parse_arguments():
    """
    Analyse des arguments en ligne de commande
    """
    parser = argparse.ArgumentParser(description='Aurore de la recherche - NLP')
    parser.add_argument(
        '-m', '--mode',
        choices=['train', 'predict'],
        default='train',
        help='Mode d\'exécution (train ou predict)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mode verbeux'
    )
    return parser.parse_args()


def preproccess(args):
    pass


def extraire_infos(fichier):
    # Regex pour correspondre au format attendu
    pattern = r'.*word.*(\d+).*.wav'
    match = re.match(pattern, fichier)
    if match:
        return {
            "word": int(match.group(1)),
        }

    pattern = r'.*statement.*(\d+).*.wav'
    match = re.match(pattern, fichier)
    if match:
        return {
            "word": int(match.group(1))
        }
    pattern = r'.*eneonce.*(\d+).*.wav'
    match = re.match(pattern, fichier)
    if match:
        return {
            "word": int(match.group(1))
        }

    return {"word": None}


def build_dataset(src_files, src_meta, init_df, sentence_field, audio_root='audio'):
    """
    Construction du dataframe associé au dataset
    :param src_files: la racine vers les fichiers de source
    :param src_meta: le chemin vers le fichier de meta données
    :param init_df: le dataframe initial
    :param verbose: si oui ou non, nous voulons apparaittre des traces d'avancement de la tache de construction
    :return: df : dataframe
    """

    df = init_df.copy(deep=True)
    # print(df)
    # charger le fichier de meta données,
    if 'src.utils.io' in imported_modules:
        module_speed = imported_modules['src.utils.io']
        if hasattr(module_speed, 'load_meta'):
            dfmeta = module_speed.load_meta(src_meta, [])
        else:
            logger.error("La fonction 'load_meta' n'existe pas dans le module.")

    sentences = dfmeta[sentence_field]
    for racine, _, fichiers in os.walk(f'{src_files}/{audio_root}'):
        for fichier_audio in fichiers:
            if fichier_audio.endswith('.wav'):  # Vérifiez uniquement les fichiers .wav
                fichier_entree = os.path.join(racine, fichier_audio)
                audio_details = extraire_infos(fichier_audio.split('/')[-1])
                try:
                    if audio_details['word'] is not None and 0 <= audio_details['word'] < len(sentences):
                        word_sentence = sentences[audio_details['word']]
                        df.loc[len(df)] = {"path": fichier_entree, 'sentence': word_sentence}
                    else:
                        logger.error(f"Index {fichier_entree} - {audio_details['word']} invalide pour les sentences.")
                        continue

                    # df1 = pd.DataFrame({"path": [fichier_entree], "word": [sentences[audio_details['word']]]})
                    #
                    # # Concaténation
                    # df = pd.concat([df, df1], ignore_index=True)
                    #
                except Exception as e:
                    logger.error(e)
                # print(df)
    # print(len(df))
    return df


if __name__ == '__main__':
    # Point d'entrée du script
    args = parse_arguments()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    main(args)
