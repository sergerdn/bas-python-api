"""
All actions to work with browser, which do not require a specific element for use. For example, load the url,
set proxy, make a screenshot, etc. To click on an element or enter text in a specific field, click on this item and
select an action from the menu.

"""
from bas_api.browser.api import Browser, BrowserOptions

__all__ = ["BrowserOptions", "Browser"]
