import asyncio
import logging
import os
import sys

ABS_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))  # root project directory

try:
    from bas_api.version import __version__ as _v
except ImportError:
    sys.path.insert(0, ABS_PATH)

from bas_api import BasApi
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

dotenv_path = os.path.join(ABS_PATH, "examples", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)

remote_script_name = os.environ.get("TEST_REMOTE_SCRIPT_NAME", "BasPythonApi")
remote_script_user = os.environ.get("TEST_REMOTE_SCRIPT_USER", None)
remote_script_password = os.environ.get("TEST_REMOTE_SCRIPT_PASSWORD", None)


async def main():
    api = BasApi(
        remote_script_name=remote_script_name,
        remote_script_user=remote_script_user,
        remote_script_password=remote_script_password,
    )
    await api.connect()

    # current_url = await api.run_function("_basBrowserLoad", {"url": "https://www.google.com/"})
    # print(current_url)
    await api.browser.load(url="https://www.google.com/", referer="https://www.google.com/")
    current_url = api.browser.current_url()
    print(current_url)

    await api.close_transport()


if __name__ == "__main__":
    asyncio.run(main())
