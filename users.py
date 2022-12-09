from pathlib import Path
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
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from fastapi_mail.schemas import MessageType
import os
from dotenv import load_dotenv
from fastapi_users import exceptions, models
import jwt
from fastapi_users.jwt import decode_jwt
from logger import logger
load_dotenv()

SECRET = os.getenv('JWTSECRET')
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=os.getenv('MAIL_PORT'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_STARTTLS=os.getenv('MAIL_STARTTLS'),
    MAIL_SSL_TLS=os.getenv('MAIL_SSL_TLS'),
    USE_CREDENTIALS=os.getenv('USE_CREDENTIALS'),
    VALIDATE_CERTS=os.getenv('VALIDATE_CERTS'),
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
    SUPPRESS_SEND=os.getenv('SUPPRESS_SEND')
)


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def verify(self, token: str, request: Optional[Request] = None) -> models.UP:
        """
        Validate a verification request.

        Changes the is_verified flag of the user to True.

        Triggers the on_after_verify handler on success.

        :param token: The verification token generated by request_verify.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises InvalidVerifyToken: The token is invalid or expired.
        :raises UserAlreadyVerified: The user is already verified.
        :return: The verified user.
        """
        logger.debug("VERIFY")
        try:
            data = decode_jwt(
                token,
                self.verification_token_secret,
                [self.verification_token_audience],
            )
        except jwt.PyJWTError:
            raise exceptions.InvalidVerifyToken()

        try:
            user_id = data["user_id"]
            email = data["email"]
        except KeyError:
            raise exceptions.InvalidVerifyToken()

        try:
            user = await self.get_by_email(email)
        except exceptions.UserNotExists:
            raise exceptions.InvalidVerifyToken()

        try:
            parsed_id = self.parse_id(user_id)
        except exceptions.InvalidID:
            raise exceptions.InvalidVerifyToken()

        if parsed_id != user.id:
            raise exceptions.InvalidVerifyToken()

        if user.is_verified:
            raise exceptions.UserAlreadyVerified()

        verified_user = await self._update(user, {"is_verified": True})

        await self.on_after_verify(verified_user, request)
        return verified_user

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        await self.request_verify(user)
        print(f"User {user} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None):

        template_body = {
            "firstname": user.firstname,
            "lastname": user.lastname,
            "token": token
        }
        message = MessageSchema(
            subject="Rowmate Registration",
            recipients=[user.email],
            template_body=template_body,
            subtype=MessageType.html)

        fm = FastMail(conf)
        await fm.send_message(message, template_name="register.{}.html".format(user.lang))

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
