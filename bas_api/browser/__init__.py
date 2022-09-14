from abc import ABC
from typing import Optional, Union

from bas_api.function import BasFunction
from bas_api.transport import AbstractTransport


class AbstractBrowser(ABC):
    _tr: Union[AbstractTransport]

    def __init__(self, tr: Union[AbstractTransport], *args, **kwargs):
        self._tr = tr

    async def load(self, url: str, referer: Optional[str]):
        """
        Loads specified url into browser. Examples: Load google.com, Load instagram.com.
        :param url:
        :param referer:
        :return:
        """
        pass

    async def current_url(self) -> BasFunction:
        """
        Get current url from browser address bar.
        :return:
        """
        pass

    async def previous_page(self) -> BasFunction:
        """
        Loads previous url from a history list.
        :return:
        """
        pass

    async def page_html(self) -> BasFunction:
        """
        Get page source and save it to variable. This action saves current source with all changes but not the initial
        returned by server.
        :return:
        """
        pass


class BrowserOptions:
    profile_dir: str
    fingerprint: Optional[str]
    pid: int

    def __init__(self):
        pass


class Browser(AbstractBrowser):
    _tr: Union[AbstractTransport]

    def __init__(self, tr: Union[AbstractTransport], *args, **kwargs):
        self._tr = tr
        super().__init__(tr=self._tr, *args, **kwargs)

    def _set_up(self):
        pass

    async def load(self, url: str, referer: Optional[str]) -> BasFunction:
        return await self._tr.run_function_thread("_basBrowserLoad", {"url": url, referer: referer})

    async def current_url(self) -> BasFunction:
        return await self._tr.run_function_thread("_basBrowserCurrentUrl")

    async def previous_page(self) -> BasFunction:
        return await self._tr.run_function_thread("_basBrowserPreviousPage")

    async def page_html(self) -> BasFunction:
        return await self._tr.run_function_thread("_basPageHtml")
