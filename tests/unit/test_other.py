from bas_client.browser.exceptions import BrowserTimeout


def test_docstring_message_exception():
    exc = BrowserTimeout()
    assert str(exc) == BrowserTimeout.__doc__

    exc = BrowserTimeout("some message")
    assert str(exc) == "some message"

    exc = BrowserTimeout()
    assert str(exc) == BrowserTimeout.__doc__
