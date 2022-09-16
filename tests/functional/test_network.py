import asyncio
import logging
import os
from io import StringIO

import pytest
import yaml
from lxml import etree

from bas_api import BasClient


@pytest.mark.dependency()
def test_api_basic_env_set(transport_options):
    assert transport_options.remote_script_name is not None
    assert transport_options.remote_script_user is not None
    assert transport_options.remote_script_password is not None
    assert transport_options.working_dir is not None
    assert os.path.exists(transport_options.working_dir) is True


@pytest.fixture(scope="class", autouse=True)
def api_bas(request, transport_options, event_loop: asyncio.AbstractEventLoop):
    api = BasClient(transport_options=transport_options, loop=event_loop)

    def fin():
        async def afin():
            logging.debug("teardown api....")
            await api.clean_up()

        event_loop.run_until_complete(afin())

    request.addfinalizer(fin)
    event_loop.run_until_complete(api.set_up())

    return api


# @pytest.mark.dependency(depends=["test_api_basic_env_set"])
@pytest.mark.asyncio
class TestApiNetwork:
    @pytest.mark.skip("not implemented")
    def test_save_cookies(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_restore_cookies(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_load_cookies_from_http_client(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_cache_mask_allow(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_cache_mask_deny(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_request_mask_allow(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_request_mask_deny(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_clear_cached_data(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_clear_cache_masks(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_get_status(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_is_loaded(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_get_last_item_from_cache(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_restrict_popups(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_allow_popups(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_restrict_downloads(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_allow_downloads(self):
        assert False

    async def test_set_header(self, api_bas: BasClient):
        await api_bas.network.set_header(name="Accept-Custom-Header-Name", value="AcceptCustomHeaderValue")

        await api_bas.browser.load("https://httpbin.org/anything")
        await api_bas.waiters.wait_full_page_load()
        page_html = await api_bas.browser.page_html()

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(str(page_html)), parser)
        page_data = tree.xpath("//pre")[0].text
        data_json = yaml.load(page_data, Loader=yaml.UnsafeLoader)

        assert "Accept-Custom-Header-Name" in data_json["headers"].keys()
        assert data_json["headers"]["Accept-Custom-Header-Name"] == "AcceptCustomHeaderValue"
