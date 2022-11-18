from typing import Optional, Literal

from beanie import PydanticObjectId
from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin
from models.users import roles
from db import User, get_user_db
import os
from dotenv import load_dotenv
load_dotenv()

SECRET = os.getenv('JWTSECRET')


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])

get_current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)


async def get_allowed_user(user: User = Depends(fastapi_users.current_user())):
    if isinstance(user, User):
        if not (user.is_accepted and user.is_active and user.is_verified):
            raise HTTPException(status_code=401)
        return user
    else:
        raise HTTPException(status_code=403)


class RequireRole:
    def __init__(self, required_role: Literal[roles]):
        self.role = required_role

    def __call__(self, user: User = Depends(get_allowed_user)):
        if self.role not in user.roles:
            raise HTTPException(status_code=403, detail="You don't have the role required to perform this action")
        else:
            return user
