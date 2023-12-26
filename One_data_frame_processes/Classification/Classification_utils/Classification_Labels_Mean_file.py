import json
import os
import numpy as np

from ..PANN_files.Config import PATH_TO_ROOT
from ..PANN_files.inference import wav_path_to_audio, ast

DEFAULT_PATH_TO_LIST_LABELS_MEAN = "C:\\Users\\Public\\Documents\\Classification\\PANN_files\\labels_means"
PATH_TO_SETS_FOLDER = "C:\\Users\\Public\\Documents\\Classification\\PANN_files\\classification sets"

def save_labels_means(dict_of_labels_means, file_path=DEFAULT_PATH_TO_LIST_LABELS_MEAN):
    # Save the dictionary of labels means and standard deviations to a JSON file
    data_to_save = {k: {"mean": v["mean"].tolist(), "std": v["std"].tolist()} for k, v in dict_of_labels_means.items()}
    with open(file_path, 'w') as file:
        json.dump(data_to_save, file)

def load_labels_means(file_path=DEFAULT_PATH_TO_LIST_LABELS_MEAN):
    # Read the dictionary of labels means and standard deviations from the JSON file
    with open(file_path, 'r') as file:
        loaded_data = json.load(file)

    # Convert the loaded data back to the original format
    loaded_dict = {k: {"mean": np.array(v["mean"]), "std": np.array(v["std"])} for k, v in loaded_data.items()}
    return loaded_dict

def calc_mean_and_std_of_label(sub_support_folder_path):
    # Get a list of file names in the folder
    support_audio = os.listdir(PATH_TO_ROOT + "\\" + sub_support_folder_path)
    sum_emb = None
    sum_squared_diff = None
    count = 0

    # Iterate over the file names
    for file_name in support_audio:
        audio = wav_path_to_audio(sub_support_folder_path + "\\" + file_name)
        emb = ast.encode(audio)

        # Calculate mean
        if sum_emb is None:
            sum_emb = emb
        else:
            sum_emb += emb

        count += 1

    mean = sum_emb / count
    dist_sum = 0
    for file_name in support_audio:
        audio = wav_path_to_audio(sub_support_folder_path + "\\" + file_name)
        emb = ast.encode(audio)

        dist_sum += np.linalg.norm(emb-mean)**2

    std = np.sqrt(dist_sum/count)

    return {"mean": mean, "std": std}

def pretrain(support_folder_path):
    # Get a list of subfolder names in the folder
    labels_folder = os.listdir(PATH_TO_ROOT + "\\" + support_folder_path)
    labels_means = {}

    # Iterate over the subfolder names
    for subfolder_label in labels_folder:
        stats = calc_mean_and_std_of_label(support_folder_path + "\\" + subfolder_label)
        labels_means[subfolder_label] = stats

    print(labels_means)
    save_labels_means(labels_means)