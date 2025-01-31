from datetime import datetime

from pydantic import BaseModel


class RegistrationRequest(BaseModel):
    email: str
    password: str


class LoginRequest(RegistrationRequest):
    pass


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class UpdateAccessTokenRequest(BaseModel):
    refresh_token: str


class UserDataResponse(BaseModel):
    id: str
    email: str

