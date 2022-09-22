import os.path
import random

import pytest

from bas_client import BasClient, BasClientSettings, BrowserOptions
from bas_client.transport import AbstractTransportOptions


@pytest.mark.asyncio
class TestBasClient:
    async def test_client_basic(self, transport_options, google_url):
        """
        Default simple logic.

        :param transport_options:
        :return:
        """
        client = BasClient(transport_options=transport_options)

        await client.setup()

        await client.browser.load(google_url)
        await client.waiters.wait_full_page_load()

        await client.clean_up()

    async def test_client_browser_profile_created(self, transport_options, google_url):
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
        await client.setup()

        assert os.path.exists(profile_folder_path) is True
        assert os.path.isdir(profile_folder_path) is True
        assert os.path.isfile(os.path.join(profile_folder_path, "lockfile"))

        await client.browser.close()
        await client.clean_up()
        """ closed profile"""
        assert not os.path.isfile(os.path.join(profile_folder_path, "lockfile"))

    async def test_client_browser_profile_old_used(self, transport_options: AbstractTransportOptions, google_url: str):
        """
        Extended settings to bas client: custom profile folder for existing profile.
        :param transport_options:
        :return:
        """

        """create new profile"""
        client = BasClient(transport_options=transport_options)

        await client.setup()

        await client.browser.load(google_url)
        await client.waiters.wait_full_page_load()
        cookies_first_obj = await client.network.save_cookies()

        browser_options = client.browser.bas_options_get()
        profile_folder_path = browser_options.profile_folder_path
        await client.browser.close()

        assert os.path.exists(profile_folder_path) is True

        """using old profile"""
        await client.browser.bas_options_set()
        await client.browser.set_visible(force=True)
        await client.browser.load("about:blank")
        await client.waiters.wait_full_page_load()
        cookies_second_obj = await client.network.save_cookies()

        # old profile loaded
        assert os.path.exists(os.path.join(profile_folder_path, "lockfile"))
        await client.clean_up()

        # old cookies exists
        for one in cookies_first_obj.cookies:
            assert one in cookies_second_obj.cookies
