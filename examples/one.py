import asyncio
import logging
import os
import sys

ABS_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))  # root project directory

try:
    from bas_api.version import __version__ as _v
except ImportError:
    sys.path.insert(0, ABS_PATH)

from bas_api import BasApi, RemoteTransportOptions
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

dotenv_path = os.path.join(ABS_PATH, "examples", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)

remote_script_name = os.environ.get("TEST_REMOTE_SCRIPT_NAME", "BasPythonApi")
remote_script_user = os.environ.get("TEST_REMOTE_SCRIPT_USER", None)
remote_script_password = os.environ.get("TEST_REMOTE_SCRIPT_PASSWORD", None)


async def main():
    options = RemoteTransportOptions(
        remote_script_name=remote_script_name,
        remote_script_user=remote_script_user,
        remote_script_password=remote_script_password,
    )
    api = BasApi(options=options)
    await api.connect()

    await api.browser.load(url="https://www.google.com/", referer="https://www.google.com/")
    current_url = api.browser.current_url()
    print(current_url)

    page_html = await  api.browser.page_html()
    print(page_html[:100])

    await api.browser.load(url="https://www.python.org/", referer="https://www.google.com/")
    current_url = api.browser.current_url()
    print(current_url)

    await  api.browser.previous_page()
    current_url = api.browser.current_url()
    print(current_url)

    await api.close_transport()


if __name__ == "__main__":
    asyncio.run(main())
