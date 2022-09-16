import pytest


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

    @pytest.mark.skip("not implemented")
    def test_close(self):
        assert False

    async def test_load(self, client, google_url):
        await client.browser.load(google_url)
        await client.waiters.wait_full_page_load()

    @pytest.mark.skip("not implemented")
    async def test_current_url(self, client, google_url):
        await client.browser.load(google_url)
        current_url = await client.waiters.wait_full_page_load()
        assert current_url == google_url

    @pytest.mark.skip("not implemented")
    def test_previous_page(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_page_html(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_type(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_resize(self):
        assert False

    @pytest.mark.skip("not implemented")
    def test_get_resolution_and_cursor_position(self):
        assert False

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
