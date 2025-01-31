from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import HTTPException, Request, status
from fastapi.param_functions import Depends
from fastapi.security import HTTPBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext

from task_management import config
from task_management.db.repositories.users import UsersRepository
from task_management.db.utils import AsyncSession, get_async_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(email: str, password: str, session: AsyncSession):
    user_repo = UsersRepository(session)
    user = await user_repo.get(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + config.JWT_EXPIRATION
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             config.SECRET_KEY,
                             algorithm=config.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + config.REFRESH_TOKEN_SECRET_EXPIRATION
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             config.REFRESH_TOKEN_SECRET,
                             algorithm=config.JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(HTTPBearer)],
                           session: Annotated[AsyncSession, Depends(get_async_session)]):
    try:
        payload = jwt.decode(token,
                             config.SECRET_KEY,
                             algorithms=[config.JWT_ALGORITHM]) # type: ignore
        email: str = payload.get('email')
        if email is None:
            raise credentials_exception
        expiration_time = payload.get('exp')
        if expiration_time > datetime.now():
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user_repo = UsersRepository(session)
    user = await user_repo.get(email)
    if user is None:
        raise credentials_exception
    return user


async def get_refresh_token_user(token: str, session: AsyncSession):
    payload = jwt.decode(token,
                         config.REFRESH_TOKEN_SECRET,
                         algorithms=[config.JWT_ALGORITHM]) # type: ignore
    email: str = payload.get('email')
    if email is None:
        raise InvalidTokenError
    user_repo = UsersRepository(session)
    user = await user_repo.get(email)
    if user is None:
        raise InvalidTokenError
    return user


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self,
                       request: Request,
                       session: Annotated[AsyncSession, Depends(get_async_session)]):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request) # type: ignore
        if not credentials:
            raise credentials_exception
        if not credentials.scheme == "Bearer":
            raise credentials_exception
        token = credentials.credentials
        try:
            payload = jwt.decode(token,
                                 config.SECRET_KEY,
                                 algorithms=[config.JWT_ALGORITHM]) # type: ignore
            email: str = payload.get('email')
            if email is None:
                raise credentials_exception
        except (InvalidTokenError, ExpiredSignatureError):
            raise credentials_exception
        user_repo = UsersRepository(session)
        user = await user_repo.get(email)
        if user is None:
            raise credentials_exception
        return user

