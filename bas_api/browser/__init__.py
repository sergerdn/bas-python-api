import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Union

import psutil

from bas_api.browser.gui import window_set_visible
from bas_api.function import BasFunction
from bas_api.transport import AbstractTransport


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
    _tr: Union[AbstractTransport]
    _options: BrowserOptions

    def __init__(self, tr: Union[AbstractTransport], *args, **kwargs):
        self._tr = tr

    @abstractmethod
    async def open_browser(self):
        """
        Create a browser if it has not already been created. This action is not mandatory for use to work with browser.
        :return:
        """
        pass

    @abstractmethod
    async def load(self, url: str, referer: Optional[str]):
        """
        Loads specified url into browser. Examples: Load google.com, Load instagram.com.
        :param url:
        :param referer:
        :return:
        """
        pass

    @abstractmethod
    async def current_url(self) -> BasFunction:
        """
        Get current url from browser address bar.
        :return:
        """
        pass

    @abstractmethod
    async def previous_page(self) -> BasFunction:
        """
        Loads previous url from a history list.
        :return:
        """
        pass

    @abstractmethod
    async def page_html(self) -> BasFunction:
        """
        Get page source and save it to variable. This action saves current source with all changes but not the initial
        returned by server.
        :return:
        """
        pass


class Browser(AbstractBrowser):
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
            raise Exception("pid of running browser not found: %s" % self._options.profile_folder_path)

        self._options.worker_pid = pid

    async def set_visible(self, force: bool = False) -> None:
        if self._options.show_browser is not True and force is not True:
            return

        await self.open_browser()
        self.options_update()
        window_set_visible(self._options.worker_pid)

    async def open_browser(self) -> BasFunction:
        return await self._tr.run_function_thread("_basOpenBrowser")

    async def close_browser(self) -> BasFunction:
        result = await self._tr.run_function_thread("_basCloseBrowser")

        await asyncio.sleep(1)
        if self._options.worker_pid > 0:
            p = psutil.Process(self._options.worker_pid)
            p.terminate()
        return result

    async def load(self, url: str, referer: Optional[str]) -> BasFunction:
        return await self._tr.run_function_thread("_basBrowserLoad", {"url": url, referer: referer})

    async def current_url(self) -> BasFunction:
        return await self._tr.run_function_thread("_basBrowserCurrentUrl")

    async def previous_page(self) -> BasFunction:
        return await self._tr.run_function_thread("_basBrowserPreviousPage")

    async def page_html(self) -> BasFunction:
        return await self._tr.run_function_thread("_basPageHtml")
