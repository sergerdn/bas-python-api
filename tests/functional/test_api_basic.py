import asyncio
import os.path
import random
import shutil

import pytest

from bas_api import BasApi, BasApiSettings, BrowserOptions, RemoteTransportOptions


def test_api_basic_env_set(remote_script_name, remote_script_user, remote_script_password, working_dir):
    assert remote_script_name is not None
    assert remote_script_user is not None
    assert remote_script_password is not None
    assert working_dir is not None
    assert os.path.exists(working_dir) is True
    assert os.path.isdir(working_dir) is True


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


class TestApiBasic:
    @pytest.mark.asyncio
    async def test_api_basic(self, remote_script_name, remote_script_user, remote_script_password, working_dir):
        transport_options = RemoteTransportOptions(
            remote_script_name=remote_script_name,
            remote_script_user=remote_script_user,
            remote_script_password=remote_script_password,
            working_dir=working_dir,
        )
        api = BasApi(transport_options=transport_options)

        await api.set_up()
        await api.browser.close_browser()
        await api.close_transport()

        browser_options = api.browser.options_get()
        await clean_dir(browser_options.profile_folder_path)
        assert os.path.exists(browser_options.profile_folder_path) is False

    @pytest.mark.asyncio
    async def test_api_browser_profile_dir(
            self, remote_script_name, remote_script_user, remote_script_password, working_dir
    ):
        transport_options = RemoteTransportOptions(
            remote_script_name=remote_script_name,
            remote_script_user=remote_script_user,
            remote_script_password=remote_script_password,
            working_dir=working_dir,
        )

        bas_api_settings = BasApiSettings(working_dir=transport_options.working_dir)
        profile_dir = os.path.join(bas_api_settings.working_profile_dir, "%s" % random.randint(10000, 99999))
        browser_options = BrowserOptions(profile_folder_path=profile_dir)

        api = BasApi(
            transport_options=transport_options, bas_api_settings=bas_api_settings, browser_options=browser_options
        )
        await api.set_up()

        assert os.path.exists(profile_dir) is True
        assert os.path.isdir(profile_dir) is True
        assert os.path.isfile(os.path.join(profile_dir, "lockfile"))

        await api.browser.close_browser()
        await api.close_transport()

        browser_options = api.browser.options_get()
        await clean_dir(browser_options.profile_folder_path)
        assert os.path.exists(browser_options.profile_folder_path) is False
