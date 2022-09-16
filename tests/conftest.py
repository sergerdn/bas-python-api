import asyncio
import os

import pytest
from dotenv import load_dotenv

from bas_api import RemoteTransportOptions
from tests import ABS_PATH, DATA_DIR

dotenv_path = os.path.join(ABS_PATH, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def working_dir():
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    return DATA_DIR


@pytest.fixture(scope="module")
def transport_options():
    remote_script_name = os.environ.get("TEST_REMOTE_SCRIPT_NAME", "BasPythonApi")
    remote_script_user = os.environ.get("TEST_REMOTE_SCRIPT_USER")
    remote_script_password = os.environ.get("TEST_REMOTE_SCRIPT_PASSWORD")

    return RemoteTransportOptions(
        remote_script_name=remote_script_name,
        remote_script_user=remote_script_user,
        remote_script_password=remote_script_password,
        working_dir=working_dir(),
    )


@pytest.fixture(scope="module")
def fixtures_dir():
    return os.path.join(ABS_PATH, "tests", "fixtures")


@pytest.fixture(scope="module")
def google_url():
    return "https://www.google.com/?gl=us&hl=en"
