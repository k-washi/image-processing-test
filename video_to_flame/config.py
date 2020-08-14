from pathlib import Path
import os

ROOT_PATH = Path(os.path.join(os.path.dirname(__file__), '..'))
DATASET_PATH = ROOT_PATH / 'data'
IMG_PATH = ROOT_PATH / 'data/imgs'
VIDEO_FILE_NAME = 'nagasaki_1080p.mp4'

VIDEO_FILE = DATASET_PATH / VIDEO_FILE_NAME

WIDTH = 1920
HEIGHT = 1020
EXTRACT_FPS = 5

START_FRAME = 0
END_FRAME = -1

CHUNK_SIZE = 200

IMAGE_NAME = "test"
