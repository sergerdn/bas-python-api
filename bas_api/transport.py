import os
from abc import ABC, abstractmethod
from typing import Union, Optional, Dict

from bas_remote import BasRemoteClient, Options
from bas_remote.runners import BasThread

from bas_api.function import BasFunction


class AbstractTransport(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def run_function_thread(self, function_name: str, function_params: Optional[Dict] = None) -> BasFunction:
        pass

    @abstractmethod
    def run_function(self, function_name: str, function_params: Optional[Dict] = None) -> BasFunction:
        pass


class RemoteTransportOptions:
    remote_script_name: str = "BasPythonApi"
    remote_script_user: Union[str, None] = None
    remote_script_password: Union[str, None] = None
    working_dir: Union[str, None] = None

    def __init__(
        self,
        remote_script_name: Union[str, None] = None,
        remote_script_user: Union[str, None] = None,
        remote_script_password: Union[str, None] = None,
    ):
        if remote_script_name is not None:
            self.remote_script_name = remote_script_name

        if remote_script_user is not None:
            self.remote_script_user = remote_script_user
        if remote_script_password is not None:
            self.remote_script_password = remote_script_password

        self.working_dir = os.path.normpath(os.path.join(os.getcwd(), ".data"))


class RemoteTransport(AbstractTransport):
    _options: RemoteTransportOptions
    _client: BasRemoteClient
    _thread: BasThread

    def __init__(self, options: RemoteTransportOptions):
        self._client = BasRemoteClient(
            options=Options(
                script_name=options.remote_script_name,
                login=options.remote_script_user,
                password=options.remote_script_password,
                working_dir=options.working_dir,
            )
        )

    async def connect(self):
        await self._client.start()
        self._thread = self._client.create_thread()

    async def close(self):
        await self._thread.stop()
        await self._client.close()

    async def run_function_thread(self, function_name: str, function_params: Optional[Dict] = None) -> BasFunction:
        return await self._thread.run_function(name=function_name, params=function_params)

    async def run_function(self, function_name: str, function_params: Optional[Dict] = None) -> BasFunction:
        return await self._client.run_function(function_name=function_name, function_params=function_params)
