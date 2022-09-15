"""
JSON to Pydantic Converter: https://jsontopydantic.com/
"""

from typing import List, Optional

from pydantic import BaseModel


class Cookie(BaseModel):
    domain: str
    expires: float
    httpOnly: bool
    name: str
    path: str
    priority: str
    sameParty: bool
    sameSite: Optional[str]
    secure: bool
    session: bool
    size: int
    sourcePort: int
    sourceScheme: str
    value: str


class Cookies(BaseModel):
    cookies: List[Cookie]
