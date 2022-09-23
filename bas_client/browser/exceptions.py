from bas_client.exceptions import AbstractException, docstring_message_exception


@docstring_message_exception
class BrowserTimeout(AbstractException):
    """Failed to wait of state complete"""


@docstring_message_exception
class BrowserNotRunning(AbstractException):
    """Browser not running"""


@docstring_message_exception
class BrowserProcessNotFound(AbstractException):
    """Pid of running browser not found"""


@docstring_message_exception
class BrowserProcessIsZero(AbstractException):
    """Worker pid is 0"""
