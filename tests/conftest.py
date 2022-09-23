import asyncio
import os
import random
import shutil

import pytest
from dotenv import load_dotenv

from bas_client import BasClient, RemoteTransportOptions
from tests import ABS_PATH, DATA_DIR, STORAGE_DIR
from tests.functional.utils import clean_dir

dotenv_path = os.path.join(ABS_PATH, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)


@pytest.fixture(scope="function")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def client(request, transport_options, event_loop: asyncio.AbstractEventLoop):
    client_api = BasClient(transport_options=transport_options, loop=event_loop)

    event_loop.run_until_complete(client_api.setup())

    yield client_api

    event_loop.run_until_complete(client_api.clean_up())


def working_dir():
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    return DATA_DIR


@pytest.fixture(scope="function")
def transport_options(request):
    remote_script_name = os.environ.get("TEST_REMOTE_SCRIPT_NAME", "BasPythonApi")
    remote_script_user = os.environ.get("TEST_REMOTE_SCRIPT_USER")
    remote_script_password = os.environ.get("TEST_REMOTE_SCRIPT_PASSWORD")
    dir_name = working_dir()

    dir_name = os.path.join(dir_name, "test_num_%s" % random.randint(1000000, 9999999))
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

    os.makedirs(dir_name)

    if os.path.exists(STORAGE_DIR):
        shutil.copytree(src=STORAGE_DIR, dst=dir_name, dirs_exist_ok=True)

    def fin(_dir_name):
        if os.path.exists(_dir_name) and os.path.isdir(_dir_name):
            clean_dir(_dir_name)

    yield RemoteTransportOptions(
        remote_script_name=remote_script_name,
        remote_script_user=remote_script_user,
        remote_script_password=remote_script_password,
        working_dir=dir_name,
    )

    fin(dir_name)


@pytest.fixture(scope="module")
def fixtures_dir():
    return os.path.join(ABS_PATH, "tests", "fixtures")


@pytest.fixture(scope="module")
def google_url():
    return "https://www.google.com/?gl=us&hl=en"


@pytest.fixture(scope="module")
def wikipedia_url():
    return "https://en.wikipedia.org/wiki/Main_Page"
