import asyncio
import os.path
import random
import shutil

import pytest

from bas_api import BasApi, BasApiSettings, BrowserOptions
from tests.functional import test_api_basic_env_set


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


@pytest.mark.dependency(depends=[test_api_basic_env_set])
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
        await api.browser.close()
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

        # old profile loaded
        assert os.path.join(profile_folder_path, "lockfile")

        await api.browser.close()
        await api.clean_up()

        await clean_dir(profile_folder_path)
        assert os.path.exists(profile_folder_path) is False
