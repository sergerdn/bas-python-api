from abc import ABC
from typing import Optional, Union

from bas_api.function import BasFunction
from bas_api.transport import AbstractTransport


class AbstractBrowser(ABC):
    _tr: Union[AbstractTransport]

    def __init__(self, tr: Union[AbstractTransport], *args, **kwargs):
        self._tr = tr

    def load(self, url: str, referer: Optional[str]):
        """
        Loads specified url into browser. Examples: Load google.com, Load instagram.com.
        :param url:
        :param referer:
        :return:
        """
        pass

    def current_url(self) -> BasFunction:
        """
        Get current url from browser address bar.
        :return:
        """
        pass

    def previous_page(self) -> BasFunction:
        """
        Loads previous url from a history list.
        :return:
        """
        pass

    def page_html(self) -> BasFunction:
        """
        Get page source and save it to variable. This action saves current source with all changes but not the initial
        returned by server.
        :return:
        """
        pass


class Browser(AbstractBrowser):
    _tr: Union[AbstractTransport]
    profile_dir: Optional[str]
    fingerprint: Optional[str]

    def __init__(self, tr: Union[AbstractTransport], *args, **kwargs):
        self._tr = tr
        super().__init__(tr=self._tr, *args, **kwargs)

    def _set_up(self):
        pass

    def load(self, url: str, referer: Optional[str]) -> BasFunction:
        return self._tr.run_function("_basBrowserLoad", {"url": url, referer: referer})

    def current_url(self) -> BasFunction:
        return self._tr.run_function("_basBrowserCurrentUrl")

    def previous_page(self) -> BasFunction:
        return self._tr.run_function("_basBrowserPreviousPage")

    def page_html(self) -> BasFunction:
        return self._tr.run_function("_basPageHtml")
