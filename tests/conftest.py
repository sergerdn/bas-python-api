import os

import pytest
from dotenv import load_dotenv

from tests import ABS_PATH, DATA_DIR

dotenv_path = os.path.join(ABS_PATH, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)


@pytest.fixture(scope="module")
def remote_script_name():
    return os.environ.get("TEST_REMOTE_SCRIPT_NAME", "BasPythonApi")


@pytest.fixture(scope="module")
def remote_script_user():
    return os.environ.get("TEST_REMOTE_SCRIPT_USER")


@pytest.fixture(scope="module")
def remote_script_password():
    return os.environ.get("TEST_REMOTE_SCRIPT_PASSWORD")


@pytest.fixture(scope="module")
def working_dir():
    if not os.path.exists:
        os.makedirs(DATA_DIR)

    return DATA_DIR
