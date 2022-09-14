import os
from typing import Union


class BasApiSettings:
    working_dir: str
    profile_dir: str

    def __init__(self, working_dir: Union[str, None] = None):
        if working_dir is None:
            self.working_dir = os.path.normpath(os.path.join(os.getcwd(), ".data"))
        else:
            self.working_dir = working_dir

        self.profile_dir = os.path.join(self.working_dir, "prof")

        if not os.path.exists(self.profile_dir):
            os.makedirs(self.profile_dir)
