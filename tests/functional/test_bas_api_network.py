import os

import pytest

from bas_api import BasApi
from tests.functional.tools import clean_dir


@pytest.mark.dependency()
def test_api_basic_env_set(transport_options):
    assert transport_options.remote_script_name is not None
    assert transport_options.remote_script_user is not None
    assert transport_options.remote_script_password is not None
    assert transport_options.working_dir is not None
    assert os.path.exists(transport_options.working_dir) is True


# @pytest.mark.dependency(depends=["test_api_basic_env_set"])
@pytest.mark.asyncio
class TestApiNetwork:
    async def test_api_network_set_header(self, transport_options, google_url):
        api = BasApi(transport_options=transport_options)

        await api.set_up()

        await api.browser.load("https://httpbin.org/anything")
        await api.waiters.wait_full_page_load()
        page_html = await api.browser.page_html()


        await api.clean_up()

        browser_options = api.browser.options_get()
        await clean_dir(browser_options.profile_folder_path)
        assert os.path.exists(browser_options.profile_folder_path) is False
