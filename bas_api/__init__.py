from typing import Union, Optional, Dict

from bas_remote.runners import BasFunction

from bas_api.browser import Browser
from bas_api.transport import RemoteTransport, RemoteTransportOptions


class BasApi:
    _options: RemoteTransportOptions
    _tr: Union[RemoteTransport]
    browser: Browser

    def __init__(self, options: RemoteTransportOptions):
        self._options = options
        self._tr = RemoteTransport(options=self._options)
        self.browser = Browser(tr=self._tr)

    async def connect(self):
        await self._tr.connect()

    async def close_transport(self):
        await self._tr.close()

    def run_function(self, function_name: str, function_params: Optional[Dict] = None) -> BasFunction:
        return self._tr.run_function(function_name=function_name, function_params=function_params)
