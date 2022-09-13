from abc import ABC

from bas_remote.runners import BasFunction as _BasFunction


class AbstractBasFunction(ABC):
    pass


class BasFunction(ABC, _BasFunction):
    pass


class RemoteBasFunction(ABC, _BasFunction):
    pass
