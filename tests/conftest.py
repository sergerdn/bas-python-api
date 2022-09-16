import asyncio
import logging
import os

import psutil
import pytest
from dotenv import load_dotenv

from bas_client import BasClient, RemoteTransportOptions
from tests import ABS_PATH, DATA_DIR
from tests.functional.tools import clean_dir

dotenv_path = os.path.join(ABS_PATH, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)


@pytest.fixture(scope="class")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="class")
def client(request, transport_options, event_loop: asyncio.AbstractEventLoop):
    client_api = BasClient(transport_options=transport_options, loop=event_loop)

    def fin():
        async def afin():
            logging.debug("teardown bas client....")
            await client_api.clean_up()

            browser_options = client_api.browser.options_get()

            logging.debug("teardown bas client: killing browser process....")
            p = psutil.Process(browser_options.worker_pid)
            try:
                p.terminate()
            except psutil.NoSuchProcess:
                pass

            logging.debug("teardown bas client: clean profile dir....")
            await clean_dir(browser_options.profile_folder_path)

        event_loop.run_until_complete(afin())

    request.addfinalizer(fin)
    event_loop.run_until_complete(client_api.set_up())

    return client_api


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
