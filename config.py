import os
import pickle

# Project
PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
APP_FOLDER = os.path.join(PROJECT_FOLDER, 'source')
STATIC_FOLDER = os.path.join(PROJECT_FOLDER, 'static')
DATA_FOLDER = os.path.join(STATIC_FOLDER, 'data')
MODEL_FOLDER = os.path.join(STATIC_FOLDER, 'models')


def pickle_obj(obj, dataset_name, folder=DATA_FOLDER):
    path = os.path.join(folder, f"{dataset_name}.pkl")
    with open(path, 'wb') as f:
        pickle.dump(obj, f)


def unpickle_obj(dataset_name, folder=DATA_FOLDER):
    path = os.path.join(folder, f"{dataset_name}.pkl")
    with open(path, 'rb') as f:
        obj = pickle.load(f)
        return obj
