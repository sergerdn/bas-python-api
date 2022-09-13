import asyncio
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


async def main():
    options = RemoteTransportOptions(
        remote_script_name="remote_script_name",
        remote_script_user="remote_script_user",
        remote_script_password="remote_script_password",
    )
    api = BasApi(options=options)
    await api.connect()

    await api.browser.load(url="https://www.google.com/", referer="https://www.google.com/")
    current_url = api.browser.current_url()
    print(current_url)

    await api.close_transport()


if __name__ == "__main__":
    asyncio.run(main())
