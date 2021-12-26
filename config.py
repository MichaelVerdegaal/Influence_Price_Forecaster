import os
import pickle

from tensorflow.keras.models import load_model

# Project
PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
APP_FOLDER = os.path.join(PROJECT_FOLDER, 'source')
STATIC_FOLDER = os.path.join(PROJECT_FOLDER, 'static')
DATA_FOLDER = os.path.join(STATIC_FOLDER, 'data')
MODEL_FOLDER = os.path.join(STATIC_FOLDER, 'models')


def pickle_obj(obj, name, folder=DATA_FOLDER):
    """
    Pickles an object
    :param obj: object to pickle
    :param name: name to give to file
    :param folder: which folder to store pickle file
    """
    path = os.path.join(folder, f"{name}.pkl")
    with open(path, 'wb') as f:
        pickle.dump(obj, f)


def unpickle_obj(name, folder=DATA_FOLDER):
    """
    Unpickles and returns an object
    :param name: name to give to file
    :param folder: which folder to store pickle file
    :return: unpickled object
    """
    path = os.path.join(folder, f"{name}.pkl")
    with open(path, 'rb') as f:
        obj = pickle.load(f)
        return obj


def save_model(model, filename):
    """
    Saves a keras model as a file
    :param model: keras model
    :param filename: filename to save it at
    """
    filepath = os.path.join(MODEL_FOLDER, f"{filename}.h5")
    model.save(filepath, overwrite=True)


def read_model(filename):
    """
    Reads a saved keras model
    :param filename: filename of model
    :return: keras model
    """
    filepath = os.path.join(MODEL_FOLDER, f"{filename}.h5")
    model = load_model(filepath)
    return model
