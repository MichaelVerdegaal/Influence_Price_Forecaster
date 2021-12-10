import os

# Project
PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
APP_FOLDER = os.path.join(PROJECT_FOLDER, 'source')
STATIC_FOLDER = os.path.join(PROJECT_FOLDER, 'static')
DATA_FOLDER = os.path.join(STATIC_FOLDER, 'data')
MODEL_FOLDER = os.path.join(STATIC_FOLDER, 'models')