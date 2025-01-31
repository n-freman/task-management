from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from task_management.api.schemas import (
    LoginRequest,
    LoginResponse,
    RegistrationRequest,
    UpdateAccessTokenRequest,
    UserDataResponse,
)
from task_management.db.repositories.users import UsersRepository
from task_management.db.utils import get_async_session
from task_management.domain import User

from .utils import (
    JWTBearer,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    get_refresh_token_user,
)

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post('/register')
async def register_user(
    request: RegistrationRequest,
    session: AsyncSession = Depends(get_async_session)
) -> UserDataResponse:
    user_repo = UsersRepository(session)
    password_hash = get_password_hash(request.password)
    user = await user_repo.add(request.email, password_hash)
    return UserDataResponse(id=user.id,
                            email=user.email)


@router.post('/login')
async def login_user(
    request: LoginRequest,
    session: AsyncSession = Depends(get_async_session)
) -> LoginResponse:
    try:
        if not await authenticate_user(request.email, request.password, session):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                'Invalid credentials')
        token_data = {'email': request.email}
        access_token = str(create_access_token(token_data))
        refresh_token = str(create_refresh_token(token_data))
        return LoginResponse(access_token=access_token,
                             refresh_token=refresh_token)
    except NoResultFound:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            'Invalid credentials')


@router.post('/login/refresh')
async def update_access_token(
    request: UpdateAccessTokenRequest,
    session: AsyncSession = Depends(get_async_session)
) -> LoginResponse:
    try:
        user = await get_refresh_token_user(request.refresh_token, session)
        token_data = {'email': user.email}
        access_token = str(create_access_token(token_data))
        return LoginResponse(access_token=access_token,
                             refresh_token=request.refresh_token)
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            'Refresh token is not valid')


@router.get('/me')
async def get_current_user(user: Annotated[User, Depends(JWTBearer())]) -> UserDataResponse:
    return UserDataResponse(id=str(user.id),
                            email=user.email)

