from abc import ABC, abstractmethod
from typing import Union

from bas_api.function import BasFunction
from bas_api.transport import AbstractTransport


class AbstractWaiters(ABC):
    _tr: Union[AbstractTransport]

    @abstractmethod
    def __init__(self, tr: Union[AbstractTransport], *args, **kwargs):
        self._tr = tr

    @abstractmethod
    async def wait_full_page_load(self) -> BasFunction:
        """
        Wait until page is fully loaded.
        :return:
        """
        pass


class Waiters(AbstractWaiters):
    _tr: Union[AbstractTransport]

    def __init__(self, tr: Union[AbstractTransport], *args, **kwargs):
        self._tr = tr
        super().__init__(tr=self._tr, *args, **kwargs)

    async def wait_full_page_load(self) -> BasFunction:
        return await self._tr.run_function_thread("_basWaitersWaitFullPageLoad")
