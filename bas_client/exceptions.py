import functools
from abc import ABC


def docstring_message_exception(cls):
    """Decorates an exception to make its docstring its default message."""
    # Must use cls_init name, not cls.__init__ itself, in closure to avoid recursion
    cls_init = cls.__init__

    @functools.wraps(cls.__init__)
    def wrapped_init(self, msg=cls.__doc__, *args, **kwargs):
        cls_init(self, msg, *args, **kwargs)

    cls.__init__ = wrapped_init
    return cls


@docstring_message_exception
class AbstractException(Exception, ABC):
    pass
