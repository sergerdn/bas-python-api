import asyncio
import inspect
from abc import ABC, abstractmethod
from typing import Optional, Union

import bas_remote
import psutil
import yaml

from bas_client.browser.exceptions import BrowserProcessNotFound, BrowserTimeout
from bas_client.browser.gui import window_set_visible
from bas_client.function import BasFunction
from bas_client.models.browser import BrowserResolutionCursorScroll
from bas_client.transport import AbstractTransport


class BrowserOptions:
    profile_folder_path: str
    load_fingerprint_from_profile_folder: bool = True
    load_proxy_from_profile_folder: bool = True
    worker_pid: int = 0
    show_browser: bool = True

    def __init__(
            self,
            profile_folder_path: str,
            load_fingerprint_from_profile_folder: bool = True,
            load_proxy_from_profile_folder: bool = True,
    ):
        self.profile_folder_path = profile_folder_path
        self.load_fingerprint_from_profile_folder = load_fingerprint_from_profile_folder
        self.load_proxy_from_profile_folder = load_proxy_from_profile_folder


class AbstractBrowser(ABC):
    """
    All actions to work with browser, which do not require a specific element for use. For example, load the url,
    set proxy, make a screenshot, etc. To click on an element or enter text in a specific field, click on this item and
    select an action from the menu.
    """

    _tr: Union[AbstractTransport]
    _options: BrowserOptions

    def __init__(self, tr: Union[AbstractTransport], *args, **kwargs):
        self._tr = tr

    @abstractmethod
    async def open(self):
        """
        Create a browser if it has not already been created. This action is not mandatory for use to work with browser.
        :return:
        """

    @abstractmethod
    async def close(self):
        """
        Close browser which was created with 'Open Browser' action. This action is not mandatory for use to work with
        browser.

        :return:
        """

    @abstractmethod
    async def load(self, url: str, referer: Optional[str]):
        """
        Loads specified url into browser. Examples: Load google.com, Load instagram.com.
        :param url:
        :param referer:
        :return:
        """

    @abstractmethod
    async def current_url(self) -> BasFunction:
        """
        Get current url from browser address bar.
        :return:
        """

    @abstractmethod
    async def previous_page(self) -> BasFunction:
        """
        Loads previous url from a history list.
        :return:
        """

    @abstractmethod
    async def page_html(self) -> BasFunction:
        """
        Get page source and save it to variable. This action saves current source with all changes but not the initial
        returned by server.
        :return:
        """

    @abstractmethod
    async def type(self) -> BasFunction:
        """
        Type text inside element with focus.
        :return:
        """

    @abstractmethod
    async def resize(self) -> BasFunction:
        """
        Changes browser resolution. Standard value is 1024x600. If you want to get typical resolutions for different
        platforms, use service fingerprint switcher.
        :return:
        """

    # get_resolution_and_cursor_position
    async def get_resolution_and_cursor_position(self) -> BrowserResolutionCursorScroll:
        """
        Get current browser size, cursor and scroll position.
        :return:
        """

    @abstractmethod
    async def proxy(self) -> BasFunction:
        """
        By default, browser works without proxy, this action sets browser proxy.
        :return:
        """

    @abstractmethod
    async def javascript(self) -> BasFunction:
        """
        Execute Javascript code in browser.
        :return:
        """

    @abstractmethod
    async def execute_on_every_page_load_in_browser(self) -> BasFunction:
        """
        This action sets script which must be executed inside every page and every frame immediately after page is
        created. Unlike javascript action, script defined here is executed at the very beginning of page load,
        which gives possibility to change browser internals like window.navigator. Action should be called before
        page load.

        :return:
        """

    @abstractmethod
    async def reset(self) -> BasFunction:
        """
        Clear all browser data: proxy, user agent, headers, BAS cache filters, BAS cache data, cookies.

        :return:
        """

    #
    @abstractmethod
    async def open_file_result(self) -> BasFunction:
        """
        Uploading file is performed in two steps: setting next open file dialog result with this action and clicking
        on element which triggers file upload, like "Upload" button.

        :return:
        """

    @abstractmethod
    async def start_drag_file(self) -> BasFunction:
        """
        This action is alternative to "Open File Result" with only difference - it drag file into browser instead of
        opening dialog.

        :return:
        """

    @abstractmethod
    async def prompt_result(self) -> BasFunction:
        """
        Prompt window displays a dialog with an optional message prompting the user to input some text. It is
        outdated functionality and most sites don't use it anymore. BAS allows to input text into that window
        automatically, to do that you must call this action before prompt window will appear.

        :return:
        """

    @abstractmethod
    async def http_auth(self) -> BasFunction:
        """
        HTTP authentication provides method for user to input site login and password. It is rarely used nowadays,
        but some sites still rely on it. During authentication process browser shows window and user must input
        authentication data there. This process can be automated, all you need to do is to call this action before
        window is triggered.

        :return:
        """

    @abstractmethod
    async def scroll(self) -> BasFunction:
        """
        Scroll browser. The objective of this action is to make specified coordinates visible.

        :return:
        """

    @abstractmethod
    async def render(self) -> BasFunction:
        """
        This action makes screenshot of selected screen part and saves it to png image encoded as base64 string.

        :return:
        """

    @abstractmethod
    async def solve_captcha(self) -> BasFunction:
        """
        This action solves image captcha(not recaptcha) and works only if you have image data formatted as base64
        string.

        :return:
        """

    @abstractmethod
    async def recaptcha_v3(self) -> BasFunction:
        """
        This action solves google recaptcha 3.0

        :return:
        """

    @abstractmethod
    async def solve_captcha_with_clicks(self) -> BasFunction:
        """
        Solve any type of captcha that requires clicking on images.

        :return:
        """

    @abstractmethod
    async def captcha_failed(self) -> BasFunction:
        """
        Use this action if last captcha was solved wrong.

        :return:
        """

    @abstractmethod
    async def timeout(self) -> BasFunction:
        """
        BAS limits execution time for every action. No action can last forever except sleep and manual captcha
        solving, but you can tweak limits.

        :return:
        """

    @abstractmethod
    async def browser_settings(self) -> BasFunction:
        """
        Changes browser settings: network, canvas, webgl, etc. Use "Get Fingerprint" action to change browser
        fingerprint.

        :return:
        """

    @abstractmethod
    async def click_extension_button(self) -> BasFunction:
        """
        Click on extension button.

        :return:
        """

    @abstractmethod
    async def touch_screen_mode(self) -> BasFunction:
        """
        Enable touch screen.

        :return:
        """

    @abstractmethod
    async def mouse_settings(self) -> BasFunction:
        """
        This is mouse movement settings. You set it either globally(through this action) or for each action
        individually by clicking on settings icon near cancel button inside any action, that uses mouse.

        :return:
        """

    @abstractmethod
    async def notifications(self) -> BasFunction:
        """
        Allow or deny browser notifications.

        :return:
        """


class Browser(AbstractBrowser, ABC):
    __doc__ = inspect.getdoc(AbstractBrowser)

    _tr: Union[AbstractTransport]
    _options: BrowserOptions

    def __init__(self, tr: Union[AbstractTransport], options: BrowserOptions, *args, **kwargs):
        self._tr = tr
        self._options = options
        super().__init__(tr=self._tr, *args, **kwargs)

    def options_get(self):
        return self._options

    async def options_set(self):
        """
        Tells browser to use specified folder as a place to store cookies, cache, localstorage, etc.
        :return:
        """
        await self._tr.run_function_thread(
            "_basCreateOrSwitchToRegularProfile",
            {
                "profile_folder_path": self._options.profile_folder_path,
                "load_fingerprint_from_profile_folder": self._options.load_fingerprint_from_profile_folder,
                "load_proxy_from_profile_folder": self._options.load_proxy_from_profile_folder,
            },
        )

    def options_update(self) -> None:
        if self._options.worker_pid > 0:
            return

        process_name = "Worker.exe"
        pid: int = 0

        for proc in psutil.process_iter():
            if process_name not in proc.name():
                continue
            for cmd in proc.cmdline():
                if cmd == self._options.profile_folder_path:
                    pid = proc.pid
                    break
            if pid > 0:
                break

        if pid == 0:
            raise BrowserProcessNotFound("pid of running browser not found: %s" % self._options.profile_folder_path)

        self._options.worker_pid = pid

    async def set_visible(self, force: bool = False) -> None:
        if self._options.show_browser is not True and force is not True:
            return

        await self.open()
        self.options_update()
        window_set_visible(self._options.worker_pid)

    async def open(self) -> BasFunction:
        return await self._tr.run_function_thread("_basOpenBrowser")

    async def close(self, force=False) -> BasFunction:
        if self._options.worker_pid == 0:
            raise Exception("worker pid is 0")

        result = await self._tr.run_function_thread("_basCloseBrowser")
        await asyncio.sleep(1)

        def _kill_proc(worker_pid: int):
            try:
                p = psutil.Process(worker_pid)
            except psutil.NoSuchProcess:
                return
            try:
                p.terminate()
            except psutil.NoSuchProcess:
                pass

        if force > 0:
            _kill_proc(self._options.worker_pid)

        # wait for browser closed
        for _ in range(0, 60):
            try:
                p = psutil.Process(self._options.worker_pid)
            except psutil.NoSuchProcess:
                break

            if not psutil.pid_exists(self._options.worker_pid):
                break

            if p.status() != psutil.STATUS_RUNNING:
                break

            await asyncio.sleep(1)

        self._options.worker_pid = 0

        return result

    async def load(self, url: str, referer: Optional[str] = None) -> BasFunction:
        return await self._tr.run_function_thread("_basBrowserLoad", {"url": url, referer: referer})

    async def current_url(self) -> BasFunction:
        return await self._tr.run_function_thread("_basBrowserCurrentUrl")

    async def previous_page(self) -> BasFunction:
        try:
            return await self._tr.run_function_thread("_basBrowserPreviousPage")
        except bas_remote.errors.FunctionError as exc:
            if exc.message == "Failed to wait of state complete":
                raise BrowserTimeout("Failed to wait of state complete")
            raise exc

    async def page_html(self) -> BasFunction:
        return await self._tr.run_function_thread("_basPageHtml")

    async def type(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def resize(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def get_resolution_and_cursor_position(self) -> BrowserResolutionCursorScroll:
        data = await self._tr.run_function_thread("_basGetResolutionAndCursorPosition")
        data_json = yaml.load(data, Loader=yaml.UnsafeLoader)
        obj_model = BrowserResolutionCursorScroll(**data_json)
        return obj_model

    async def proxy(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def javascript(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def execute_on_every_page_load_in_browser(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def reset(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def open_file_result(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def start_drag_file(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def prompt_result(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def http_auth(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def scroll(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def render(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def solve_captcha(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def recaptcha_v3(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def solve_captcha_with_clicks(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def captcha_failed(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def timeout(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def browser_settings(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def click_extension_button(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def touch_screen_mode(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def mouse_settings(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def notifications(self) -> BasFunction:
        raise NotImplementedError("function not implemented")
