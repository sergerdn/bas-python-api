from abc import ABC, abstractmethod
from typing import Union

import yaml

from bas_api.function import BasFunction
from bas_api.models import Cookies
from bas_api.transport import AbstractTransport


class AbstractNetwork(ABC):
    """
    All actions to interact with browser network requests. Deny request to certain urls, set user agent and other
    headers, access to cache.
    """

    _tr: Union[AbstractTransport]

    @abstractmethod
    def __init__(self, tr: Union[AbstractTransport], *args, **kwargs):
        pass

    @abstractmethod
    async def set_header(self) -> BasFunction:
        """
        Wait for the end of the current download.

        :return:
        """

    @abstractmethod
    async def save_cookies(self) -> Cookies:
        """
        Save all browser cookies into variable.

        :return:
        """

    @abstractmethod
    async def restore_cookies(self) -> BasFunction:
        """
        Restore cookies for browser.

        :return:
        """

    @abstractmethod
    async def load_cookies_from_http_client(self) -> BasFunction:
        """
        Load cookies from http client to browser.

        :return:
        """

    @abstractmethod
    async def cache_mask_allow(self) -> BasFunction:
        """
        Add page content to cache if Url matches specified mask. Works only on pages which will be loaded next after
        this action call.

        :return:
        """

    @abstractmethod
    async def cache_mask_deny(self) -> BasFunction:
        """
        Do not add page content to cache if Url matches specified mask. Works only on pages which will be loaded next
        after this action call.

        :return:
        """

    @abstractmethod
    async def request_mask_allow(self) -> BasFunction:
        """
        Allow Url loading if Url matches specified mask. By default, every Url is loaded.

        :return:
        """

    @abstractmethod
    async def request_mask_deny(self) -> BasFunction:
        """
        Deny Url loading if Url matches specified mask. By default, every Url is loaded.

        :return:
        """

    @abstractmethod
    async def clear_cached_data(self) -> BasFunction:
        """
        Delete information about all loaded Urls from the cache.

        :return:
        """

    @abstractmethod
    async def clear_cache_masks(self) -> BasFunction:
        """
        Clear all previously added cache masks.

        :return:
        """

    @abstractmethod
    async def get_status(self) -> BasFunction:
        """
        Get request status for the specified Url.

        :return:
        """

    @abstractmethod
    async def is_loaded(self) -> BasFunction:
        """
        Check if the specified Url has been loaded.

        :return:
        """

    @abstractmethod
    async def get_last_item_from_cache(self) -> BasFunction:
        """
        Get last cache item for specified Url and save it to variable.

        :return:
        """

    @abstractmethod
    async def restrict_popups(self) -> BasFunction:
        """
        Restrict all popups. You can restrict specific popup with Request Mask Deny action.

        :return:
        """

    @abstractmethod
    async def allow_popups(self) -> BasFunction:
        """
        Allow all popups. Revokes Restrict popups action.

        :return:
        """

    @abstractmethod
    async def restrict_downloads(self) -> BasFunction:
        """
        Restrict all file downloads. You can restrict specific download with Request Mask Deny action.

        :return:
        """

    @abstractmethod
    async def allow_downloads(self) -> BasFunction:
        """
        Allow all file downloads. Revokes Restrict downloads action.

        :return:
        """


class Network(AbstractNetwork, ABC):
    _tr: Union[AbstractTransport]

    def __init__(self, tr: Union[AbstractTransport], *args, **kwargs):
        self._tr = tr
        super().__init__(tr=self._tr, *args, **kwargs)

    async def save_cookies(self) -> Cookies:
        data = await self._tr.run_function_thread("_basNetworkSaveCookies")
        data_json = yaml.load(data, Loader=yaml.UnsafeLoader)
        obj_model = Cookies(**data_json)
        return obj_model

    async def restore_cookies(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def load_cookies_from_http_client(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def cache_mask_allow(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def cache_mask_deny(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def request_mask_allow(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def request_mask_deny(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def clear_cached_data(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def clear_cache_masks(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def get_status(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def is_loaded(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def get_last_item_from_cache(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def restrict_popups(self) -> BasFunction:
        pass

    async def allow_popups(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def restrict_downloads(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def allow_downloads(self) -> BasFunction:
        raise NotImplementedError("function not implemented")

    async def set_header(self) -> BasFunction:
        raise NotImplementedError("function not implemented")
