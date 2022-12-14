import asyncio
import logging
import os.path
import random
from typing import Dict, Optional, Union

from bas_remote.runners import BasFunction

from bas_client.browser import Browser, BrowserOptions
from bas_client.browser.exceptions import BrowserProcessIsZero
from bas_client.network import Network
from bas_client.settings import BasClientSettings
from bas_client.transport import AbstractTransportOptions, RemoteTransport, RemoteTransportOptions
from bas_client.typing import LoggerLike
from bas_client.waiters import Waiters


class BasClient:
    _transport_options: AbstractTransportOptions
    _settings: BasClientSettings
    _tr: Union[RemoteTransport]
    _loop: Optional[asyncio.AbstractEventLoop]
    browser: Browser
    browser_options: BrowserOptions
    waiters = Waiters
    network = Network
    logger: LoggerLike

    def __init__(
        self,
        transport_options: AbstractTransportOptions,
        bas_client_settings: Optional[BasClientSettings] = None,
        browser_options: Optional[BrowserOptions] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        self._transport_options = transport_options

        self.logger = logging.getLogger("[bas-client]")

        if bas_client_settings is not None:
            self._settings = bas_client_settings
        else:
            self._settings = BasClientSettings(working_dir=self._transport_options.working_dir)

        self._transport_options.working_dir = self._settings.working_dir

        self._loop = loop
        self._tr = RemoteTransport(options=self._transport_options, loop=self._loop)

        if browser_options is None:
            profile_dir = os.path.join(self._settings.working_profile_dir, "profile_%s" % random.randint(10000, 99999))
            self.browser_options = BrowserOptions(profile_folder_path=profile_dir)
        else:
            self.browser_options = browser_options

        self.browser = Browser(tr=self._tr, options=self.browser_options)
        self.waiters = Waiters(tr=self._tr)
        self.network = Network(tr=self._tr)

    async def set_up(self):
        await self._tr.connect()
        await self.browser.options_set()
        await self.browser.set_visible()
        return self

    async def clean_up(self):
        try:
            await self.browser.close()
        except BrowserProcessIsZero:
            pass

        return await self._tr.close()

    async def run_function(self, function_name: str, function_params: Optional[Dict] = None) -> BasFunction:
        return await self._tr.run_function(function_name=function_name, function_params=function_params)

    async def run_function_thread(self, function_name: str, function_params: Optional[Dict] = None) -> BasFunction:
        return await self._tr.run_function_thread(function_name=function_name, function_params=function_params)
