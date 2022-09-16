import os
from typing import Union

DEFAULT_DATA_DIR = ".data"
DEFAULT_PROFILE_DIR = "prof"


class BasClientSettings:
    working_dir: str
    working_profile_dir: str

    def __init__(self, working_dir: Union[str, None] = None):
        if working_dir is None:
            self.working_dir = os.path.normpath(os.path.join(os.getcwd(), DEFAULT_DATA_DIR))
        else:
            self.working_dir = working_dir

        self.working_profile_dir = os.path.join(self.working_dir, DEFAULT_PROFILE_DIR)

        if not os.path.exists(self.working_profile_dir):
            os.makedirs(self.working_profile_dir)
