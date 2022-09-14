import os.path
import random
from typing import Union, Optional, Dict

from bas_remote.runners import BasFunction

from bas_api.browser import Browser, BrowserOptions
from bas_api.settings import BasApiSettings
from bas_api.transport import RemoteTransport, RemoteTransportOptions


class BasApi:
    _transport_options: RemoteTransportOptions
    _settings: BasApiSettings
    _tr: Union[RemoteTransport]
    browser: Browser
    browser_options: BrowserOptions

    def __init__(
        self,
        transport_options: RemoteTransportOptions,
        bas_api_settings: Optional[BasApiSettings] = None,
        browser_options: Optional[BrowserOptions] = None,
    ):

        if bas_api_settings is not None:
            self._settings = bas_api_settings
        else:
            self._settings = BasApiSettings()

        self._transport_options = transport_options
        self._transport_options.working_dir = self._settings.working_dir

        self._tr = RemoteTransport(options=self._transport_options)

        if browser_options is None:
            profile_dir = os.path.join(self._settings.working_profile_dir, "%s" % random.randint(10000, 99999))
            self.browser_options = BrowserOptions(profile_folder_path=profile_dir)

        self.browser = Browser(tr=self._tr, options=self.browser_options)

    async def set_up(self):
        await self._tr.connect()
        await self.browser.options_set()
        await self.browser.set_visible()

    async def close_transport(self):
        await self._tr.close()

    async def run_function_thread(self, function_name: str, function_params: Optional[Dict] = None) -> BasFunction:
        return await self._tr.run_function_thread(function_name=function_name, function_params=function_params)
