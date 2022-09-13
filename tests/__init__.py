import logging
import os

ABS_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))  # root project directory
logging.basicConfig(level=logging.DEBUG)
DATA_DIR = os.path.join(ABS_PATH, "tests", ".tests_data")
STORAGE_DIR = os.path.join(ABS_PATH, "tests", "fixtures", "storage")
