from decouple import config
from dataclasses import dataclass
from tensorflow import keras
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = config("DEBUG", default=False, cast=bool)
