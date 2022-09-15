import asyncio
import os.path
import random
import shutil

import pytest

from bas_api import BasApi, BasApiSettings, BrowserOptions
from bas_api.browser.exceptions import BrowserWaitTimeout


async def clean_dir(dir_path):
    for _ in range(0, 60):
        try:
            shutil.rmtree(dir_path)
        except PermissionError:
            await asyncio.sleep(1)
            continue
        except FileNotFoundError:
            break

    return True


@pytest.mark.dependency()
def test_api_basic_env_set(transport_options):
    assert transport_options.remote_script_name is not None
    assert transport_options.remote_script_user is not None
    assert transport_options.remote_script_password is not None
    assert transport_options.working_dir is not None
    assert os.path.exists(transport_options.working_dir) is True


# @pytest.mark.dependency(depends=["test_api_basic_env_set"])
@pytest.mark.asyncio
class TestApiBasic:
    async def test_api_basic(self, transport_options):
        """
        Default simple logic.

        :param transport_options:
        :return:
        """
        api = BasApi(transport_options=transport_options)

        await api.set_up()

        await api.browser.load("https://www.google.com/")
        await api.waiters.wait_full_page_load()

        await api.clean_up()

        browser_options = api.browser.options_get()
        await clean_dir(browser_options.profile_folder_path)
        assert os.path.exists(browser_options.profile_folder_path) is False

    async def test_api_browser_profile_dir_new(self, transport_options):
        """
        Extended settings to api: custom profile folder for new profile.

        :param transport_options:
        :return:
        """
        bas_api_settings = BasApiSettings(working_dir=transport_options.working_dir)
        profile_folder_path = os.path.join(bas_api_settings.working_profile_dir, "%s" % random.randint(10000, 99999))
        browser_options = BrowserOptions(profile_folder_path=profile_folder_path)

        api = BasApi(
            transport_options=transport_options, bas_api_settings=bas_api_settings, browser_options=browser_options
        )
        await api.set_up()

        assert os.path.exists(profile_folder_path) is True
        assert os.path.isdir(profile_folder_path) is True
        assert os.path.isfile(os.path.join(profile_folder_path, "lockfile"))

        await api.browser.close()
        await api.clean_up()

        browser_options = api.browser.options_get()
        await clean_dir(browser_options.profile_folder_path)
        assert os.path.exists(browser_options.profile_folder_path) is False

    async def test_api_browser_profile_dir_old(self, transport_options):
        """
        Extended settings to api: custom profile folder for existing profile.
        :param transport_options:
        :return:
        """

        """create new profile"""
        api = BasApi(transport_options=transport_options)

        await api.set_up()

        await api.browser.load("https://www.google.com/?hl=en")
        await api.waiters.wait_full_page_load()
        cookies_first_obj = await api.network.save_cookies()
        await api.clean_up()

        browser_options = api.browser.options_get()
        profile_folder_path = browser_options.profile_folder_path

        assert os.path.exists(profile_folder_path) is True

        # wait for browser closed
        while os.path.exists(os.path.join(profile_folder_path, "lockfile")):
            await asyncio.sleep(0.5)

        """using old profile"""
        bas_api_settings = BasApiSettings(working_dir=transport_options.working_dir)
        browser_options = BrowserOptions(profile_folder_path=profile_folder_path)

        api = BasApi(
            transport_options=transport_options, bas_api_settings=bas_api_settings, browser_options=browser_options
        )
        await api.set_up()

        await api.browser.load("https://duckduckgo.com/")
        await api.waiters.wait_full_page_load()
        cookies_second_obj = await api.network.save_cookies()

        # old profile loaded
        assert os.path.exists(os.path.join(profile_folder_path, "lockfile"))
        await api.clean_up()

        # wait for browser closed
        while os.path.exists(os.path.join(profile_folder_path, "lockfile")):
            await asyncio.sleep(0.5)

        await clean_dir(profile_folder_path)
        assert os.path.exists(profile_folder_path) is False

        # old cookies exists
        for one in cookies_first_obj.cookies:
            assert one in cookies_second_obj.cookies

    async def test_api_browser(self, transport_options):
        """
        Default simple logic.

        :param transport_options:
        :return:
        """
        api = BasApi(transport_options=transport_options)

        await api.set_up()

        await api.browser.load("https://www.google.com/?hl=en")
        try:
            await api.waiters.wait_full_page_load()
        except BrowserWaitTimeout:
            pass

        current_url = await api.browser.current_url()
        assert current_url == "https://www.google.com/?hl=en"

        page_html = await api.browser.page_html()

        await api.browser.load("https://en.wikipedia.org/wiki/Main_Page")
        try:
            await api.waiters.wait_full_page_load()
        except BrowserWaitTimeout:
            pass

        await api.browser.previous_page()
        try:
            await api.waiters.wait_full_page_load()
        except BrowserWaitTimeout:
            pass
        current_url = await api.browser.current_url()
        assert current_url == "https://www.google.com/?hl=en"

        await api.clean_up()

        browser_options = api.browser.options_get()
        await clean_dir(browser_options.profile_folder_path)
        assert os.path.exists(browser_options.profile_folder_path) is False
