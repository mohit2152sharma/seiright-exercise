"""
This module has util functions for handling authentication and security

"""

from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from .api_models import get_user
from .utils import get_env_var


def secret_key() -> str:
    """fetches security key from the environment

    Returns:
        security key
    """
    return get_env_var("SECRET_KEY", raise_error=True)


def algorithm() -> str:
    """fetches hashing algorithm from environment

    Returns:
        algorithm
    """
    return get_env_var("ALGORITHM", raise_error=True)


def access_token_expire_time() -> int:
    """fetches token expire time from the environment

    Returns:
        token expiry time, if not present in environment returns the default value of 30 minutes
    """
    time = get_env_var("ACCESS_TOKEN_EXPIRE_TIME", default_value=30, raise_error=False)
    return int(time)


def pwd_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def oauth2_scheme() -> OAuth2PasswordBearer:
    return OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context().verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context().hash(password)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key(), algorithm=algorithm())
    return encoded_jwt
