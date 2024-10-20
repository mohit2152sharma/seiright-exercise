from pydantic import BaseModel

from ..core._types import LLMProvider


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    display_name: str | None = None
    email: str | None = None


class UserInDB(User):
    hashed_password: str


class CheckComplianceResponse(BaseModel):
    is_compliant: bool
    llm_provider: str
    confidence_score: float
    reason: str
    user: str
    url: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
