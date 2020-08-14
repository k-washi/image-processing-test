from decouple import config

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = config("DEBUG", default=False, cast=bool)
