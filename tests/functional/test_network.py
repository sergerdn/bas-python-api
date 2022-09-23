import asyncio

import pytest
from pydantic import HttpUrl

from bas_client import BasClient
from tests.functional.utils import json_from_httpbin


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

    async def test_clear_cached_data(self, client: BasClient, google_url: HttpUrl, wikipedia_url: HttpUrl):
        await client.network.cache_mask_allow(mask="*")
        await client.browser.load(google_url)
        await client.waiters.wait_full_page_load()

        items = await client.network.get_all_items_from_cache(mask="*")
        await asyncio.sleep(0)
        assert len(items) > 1

        await client.network.clear_cached_data()
        items = await client.network.get_all_items_from_cache(mask="*")
        assert len(items) == 0

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
    def test_get_all_items_from_cache(self):
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

    async def test_set_header(self, client: BasClient):
        await client.network.set_header(name="Accept-Custom-Header-Name", value="AcceptCustomHeaderValue")

        await client.browser.load("https://httpbin.org/anything")
        await client.waiters.wait_full_page_load()
        page_html = await client.browser.page_html()

        data_json = json_from_httpbin(str(page_html))

        assert "Accept-Custom-Header-Name" in data_json["headers"].keys()
        assert data_json["headers"]["Accept-Custom-Header-Name"] == "AcceptCustomHeaderValue"
