from beanie import Document
from pydantic import BaseModel


class User(Document):
    username: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
