from typing import List

from pydantic import BaseModel


class NetworkCacheEntry(BaseModel):
    body: str
    error: str
    is_error: int
    is_finished: int
    post_data: str
    request_headers: List[List[str]]
    response_headers: List[List[str]]
    status: int
    url: str
