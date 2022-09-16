from pydantic import BaseModel


class BrowserResolutionCursorScroll(BaseModel):
    cursor_x: int
    cursor_y: int
    scroll_x: int
    scroll_y: int
    browser_width: int
    browser_height: int
