import logging
from abc import ABC, abstractmethod
from typing import Union

from bas_client.function import BasFunction
from bas_client.transport import AbstractTransport
from bas_client.typing import LoggerLike


class AbstractWaiters(ABC):
    _tr: Union[AbstractTransport]
    logger: LoggerLike

    @abstractmethod
    def __init__(self, tr: Union[AbstractTransport], *args, **kwargs):
        self._tr = tr
        self.logger = logging.getLogger("[bas-client:waiters]")

    @abstractmethod
    async def wait_full_page_load(self) -> BasFunction:
        """
        Wait until page is fully loaded.
        :return:
        """

    @abstractmethod
    async def wait_url_loaded(self) -> BasFunction:
        """
        Wait until browser loads specified URL.

        :return:
        """

    @abstractmethod
    async def wait_address_bar(self) -> BasFunction:
        """
        Wait until address bar contains specified URL.

        :return:
        """

    @abstractmethod
    async def wait_text(self) -> BasFunction:
        """
        Wait until specific text appears on the page.

        :return:
        """

    @abstractmethod
    async def wait_css(self) -> BasFunction:
        """
        Wait until specific CSS-selector returns a non-empty result.

        :return:
        """

    @abstractmethod
    async def wait_file_download(self) -> BasFunction:
        """
        Wait for the end of the current download.

        :return:
        """

    @abstractmethod
    async def sleep(self) -> BasFunction:
        """
        Pauses current thread for the specified number of milliseconds.

        :return:
        """


class Waiters(AbstractWaiters):
    def __init__(self, tr: Union[AbstractTransport], *args, **kwargs):
        super().__init__(tr=tr, *args, **kwargs)

    async def wait_full_page_load(self) -> BasFunction:
        return await self._tr.run_function_thread("_basWaitersWaitFullPageLoad")

    async def wait_url_loaded(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def wait_address_bar(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def wait_text(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def wait_css(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def wait_file_download(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def sleep(self) -> BasFunction:
        raise NotImplementedError("function not implemented")
