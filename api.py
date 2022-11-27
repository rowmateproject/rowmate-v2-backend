from fastapi import APIRouter
from routers import boats, config, adverts, users

from models.users import UserCreate, UserRead, UserUpdate, User
from users import auth_backend, fastapi_users

router = APIRouter()
router.include_router(boats.router)
router.include_router(config.router)
router.include_router(adverts.router)
router.include_router(users.router)


router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True), prefix="/auth/jwt", tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(User, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True),
    prefix="/users",
    tags=["users"],
)



