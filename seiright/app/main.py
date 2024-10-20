import logging
from datetime import timedelta
from typing import Annotated, Dict

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt

from ..core._types import LLMProvider
from ..core.assemble import ComplianceChecker
from .api_models import CheckComplianceResponse, Token, TokenData, User, get_user
from .security import (
    access_token_expire_time,
    algorithm,
    authenticate_user,
    create_access_token,
    oauth2_scheme,
    secret_key,
)
from .utils import read_db

app = FastAPI()
logging.basicConfig(level=logging.INFO)
compliance_checker = ComplianceChecker(llm_provider=LLMProvider.OPENAI, model="gpt4o")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme())]) -> User:
    """checks if the current user is a valid user or not. If not raises an exception

    Args:
        token: token to authenticate user

    Returns:
        User, if it is a valid user otherwise exception
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key(), algorithms=[algorithm()])
        username: str | None = payload.get("sub")  # type: ignore
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db = read_db()
    user = get_user(db, username=token_data.username)  # type: ignore
    if user is None:
        raise credentials_exception
    return user


@app.get("/check-compliance")
async def check_compliance(
    current_user: Annotated[User, Depends(get_current_user)], url: str
) -> CheckComplianceResponse:
    """Checks whether the given page is compliant or not

    Args:
        current_user: user information required for authentication
        url: url to read and check compliance for

    Returns:
        A Dictionary with user information and compliance information
    """
    compliance_check = compliance_checker.chat(url)
    return CheckComplianceResponse(
        is_compliant=compliance_check.is_compliant,
        confidence_score=compliance_check.confidence_score,
        reason=compliance_check.reasoning,
        user=current_user.username,
        url=url,
        llm_provider=compliance_check.llm_provider.value,
    )


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Dict:
    """authenticates the user and returns a token

    Args:
        form_data: form data with username and password

    Raises:
        HTTPException: Raises an exception if the user is not a valid user

    Returns:
        token and token type
    """
    db = read_db()
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=access_token_expire_time())
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
