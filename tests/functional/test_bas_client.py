import asyncio
import os.path
import random

import pytest

from bas_client import BasClient, BasClientSettings, BrowserOptions
from tests.functional.utils import clean_dir_async


@pytest.mark.asyncio
class TestBasClient:
    async def test_client_basic(self, transport_options, google_url):
        """
        Default simple logic.

        :param transport_options:
        :return:
        """
        client = BasClient(transport_options=transport_options)

        await client.set_up()

        await client.browser.load(google_url)
        await client.waiters.wait_full_page_load()

        await client.clean_up()

        browser_options = client.browser.options_get()
        await clean_dir_async(browser_options.profile_folder_path)
        assert os.path.exists(browser_options.profile_folder_path) is False

    async def test_client_browser_profile_dir_new(self, transport_options, google_url):
        """
        Extended settings to bas client: custom profile folder for new profile.

        :param transport_options:
        :return:
        """
        bas_client_settings = BasClientSettings(working_dir=transport_options.working_dir)
        profile_folder_path = os.path.join(bas_client_settings.working_profile_dir, "%s" % random.randint(10000, 99999))
        browser_options = BrowserOptions(profile_folder_path=profile_folder_path)

        client = BasClient(
            transport_options=transport_options,
            bas_client_settings=bas_client_settings,
            browser_options=browser_options,
        )
        await client.set_up()

        assert os.path.exists(profile_folder_path) is True
        assert os.path.isdir(profile_folder_path) is True
        assert os.path.isfile(os.path.join(profile_folder_path, "lockfile"))

        await client.browser.close()
        await client.clean_up()

        browser_options = client.browser.options_get()
        await clean_dir_async(browser_options.profile_folder_path)
        assert os.path.exists(browser_options.profile_folder_path) is False

    async def test_client_browser_profile_dir_old(self, transport_options, google_url):
        """
        Extended settings to bas client: custom profile folder for existing profile.
        :param transport_options:
        :return:
        """

        """create new profile"""
        client = BasClient(transport_options=transport_options)

        await client.set_up()

        await client.browser.load(google_url)
        await client.waiters.wait_full_page_load()
        cookies_first_obj = await client.network.save_cookies()
        await client.clean_up()

        browser_options = client.browser.options_get()
        profile_folder_path = browser_options.profile_folder_path

        assert os.path.exists(profile_folder_path) is True

        # wait for browser closed
        while os.path.exists(os.path.join(profile_folder_path, "lockfile")):
            await asyncio.sleep(0.5)
        """using old profile"""

        bas_api_settings = BasClientSettings(working_dir=transport_options.working_dir)
        browser_options = BrowserOptions(profile_folder_path=profile_folder_path)

        client = BasClient(
            transport_options=transport_options, bas_client_settings=bas_api_settings, browser_options=browser_options
        )
        await client.set_up()

        await client.browser.load("https://duckduckgo.com/")
        await client.waiters.wait_full_page_load()
        cookies_second_obj = await client.network.save_cookies()

        # old profile loaded
        assert os.path.exists(os.path.join(profile_folder_path, "lockfile"))
        await client.clean_up()

        # wait for browser closed
        while os.path.exists(os.path.join(profile_folder_path, "lockfile")):
            await asyncio.sleep(0.5)

        await clean_dir_async(profile_folder_path)
        assert os.path.exists(profile_folder_path) is False

        # old cookies exists
        for one in cookies_first_obj.cookies:
            assert one in cookies_second_obj.cookies
