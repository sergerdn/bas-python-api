import logging
import os

from dotenv import load_dotenv

from bas_client import RemoteTransportOptions

ABS_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))  # root project directory
DATA_DIR = os.path.join(ABS_PATH, "tools", ".tools_data")
logging.basicConfig(level=logging.DEBUG)

dotenv_path = os.path.join(ABS_PATH, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)


def get_tr_options() -> RemoteTransportOptions:
    def working_dir():
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)

        return DATA_DIR

    remote_script_name = os.environ.get("TEST_REMOTE_SCRIPT_NAME", "BasPythonApi")
    remote_script_user = os.environ.get("TEST_REMOTE_SCRIPT_USER")
    remote_script_password = os.environ.get("TEST_REMOTE_SCRIPT_PASSWORD")

    return RemoteTransportOptions(
        remote_script_name=remote_script_name,
        remote_script_user=remote_script_user,
        remote_script_password=remote_script_password,
        working_dir=working_dir(),
    )
