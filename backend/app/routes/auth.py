from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.core.auth import create_access_token
from app.core.config import settings
from app.core.dependencies import get_current_user
from app.database import get_db
from app.db_models import User
from app.models import UserLogin, UserOut, UserRegister
from app.services.users import authenticate_user, create_user


router = APIRouter(prefix="/auth", tags=["auth"])


FAILED_LOGINS: dict[str, list[datetime]] = {}
MAX_FAILED_ATTEMPTS = 5
LOGIN_WINDOW = timedelta(minutes=10)


def _client_ip(request: Request) -> str:
    if request.client:
        return request.client.host
    return "unknown"


def _check_login_limit(ip: str) -> None:
    now = datetime.now(timezone.utc)

    attempts = FAILED_LOGINS.get(ip, [])
    attempts = [item for item in attempts if now - item < LOGIN_WINDOW]
    FAILED_LOGINS[ip] = attempts

    if len(attempts) >= MAX_FAILED_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Слишком много попыток входа. Попробуйте позже",
        )


def _register_failed_login(ip: str) -> None:
    now = datetime.now(timezone.utc)
    FAILED_LOGINS.setdefault(ip, []).append(now)


def _clear_failed_logins(ip: str) -> None:
    FAILED_LOGINS.pop(ip, None)


def _set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
        path="/",
    )


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(
    data: UserRegister,
    db: Session = Depends(get_db),
):
    try:
        # ВАЖНО: роль всегда user.
        # Пользователь не может сам выбрать себе admin.
        return create_user(
            db=db,
            username=data.username,
            email=data.email,
            password=data.password,
            role="user",
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.post("/login")
def login(
    data: UserLogin,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    ip = _client_ip(request)

    _check_login_limit(ip)

    user = authenticate_user(
        db=db,
        login=data.login,
        password=data.password,
    )

    if not user:
        _register_failed_login(ip)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )

    _clear_failed_logins(ip)

    token = create_access_token(
        user_id=user.id,
        username=user.username,
        role=user.role,
    )

    _set_auth_cookie(response, token)

    return {
        "status": "ok",
        "user": UserOut.model_validate(user).model_dump(),
    }


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
    )

    return {"status": "ok"}


@router.get("/me", response_model=UserOut)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user