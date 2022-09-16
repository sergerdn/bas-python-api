import psutil
import pytest
from pydantic import HttpUrl

from bas_client import BasClient
from bas_client.browser.exceptions import BrowserTimeout


@pytest.mark.asyncio
class TestBrowser:
    @pytest.mark.skip("not implemented")
    def test_options_get(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_options_set(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_options_update(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_set_visible(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_open(self):
        assert False

    async def test_close(self, client: BasClient):
        await client.browser.load("about:blank")
        options = client.browser.options_get()

        p = psutil.Process(options.worker_pid)
        assert p.status() == psutil.STATUS_RUNNING
        await client.browser.close()

        options = client.browser.options_get()
        assert options.worker_pid == 0

        with pytest.raises(psutil.NoSuchProcess):
            psutil.Process(options.worker_pid)

    async def test_load(self, client: BasClient, google_url: HttpUrl):
        await client.browser.load(google_url)
        await client.waiters.wait_full_page_load()

    async def test_current_url(self, client: BasClient, google_url: HttpUrl):
        await client.browser.load(google_url)
        await client.waiters.wait_full_page_load()
        current_url = await client.browser.current_url()
        assert current_url == google_url

    async def test_previous_page(self, client: BasClient, google_url: HttpUrl):
        await client.browser.load(google_url)
        await client.waiters.wait_full_page_load()
        current_url = await client.browser.current_url()
        assert current_url == google_url

        await client.browser.load("https://en.wikipedia.org/wiki/Main_Page")
        await client.waiters.wait_full_page_load()
        try:
            await client.browser.previous_page()
        except BrowserTimeout as exc:
            # FIXME: this is a bug
            pass

        current_url = await client.browser.current_url()
        assert current_url == google_url

    async def test_page_html(self, client: BasClient, google_url: HttpUrl):
        await client.browser.load(google_url)
        page_html = await client.browser.page_html()
        page_html_str = str(page_html)
        assert page_html_str.strip().endswith("</script></body></html>")

    @pytest.mark.skip("not implemented")
    def test_type(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_resize(self):
        assert False

    async def test_get_resolution_and_cursor_position(self, client: BasClient):
        await client.browser.load("about:blank")
        obj_model = await client.browser.get_resolution_and_cursor_position()
        assert obj_model.browser_height >= 600
        assert obj_model.browser_width >= 1024

    @pytest.mark.skip("not implemented")
    def test_proxy(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_javascript(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_execute_on_every_page_load_in_browser(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_reset(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_open_file_result(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_start_drag_file(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_prompt_result(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_http_auth(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_scroll(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_render(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_solve_captcha(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_recaptcha_v3(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_solve_captcha_with_clicks(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_captcha_failed(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_timeout(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_browser_settings(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_click_extension_button(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_touch_screen_mode(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_mouse_settings(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_notifications(self):
        assert False
