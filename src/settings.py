import os

SRC_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(SRC_PATH)
IN_PROCESS_DIR = os.path.join(BASE_PATH, 'in_process')
FINISHED_DIR = os.path.join(BASE_PATH, 'finished')
MODELS_DIR = os.path.join(BASE_PATH, 'models')
AUDACITY_DIR = os.path.join(BASE_PATH, 'audacity')
