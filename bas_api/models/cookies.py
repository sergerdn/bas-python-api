"""
JSON to Pydantic Converter: https://jsontopydantic.com/
"""

from typing import List

from pydantic import BaseModel


class Cookie(BaseModel):
    domain: str
    expires: float
    httpOnly: bool
    name: str
    path: str
    priority: str
    sameParty: bool
    sameSite: str
    secure: bool
    session: bool
    size: int
    sourcePort: int
    sourceScheme: str
    value: str


class Cookies(BaseModel):
    cookies: List[Cookie]
