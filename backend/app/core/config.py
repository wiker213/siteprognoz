import os
from pydantic import BaseModel


def _bool_env(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() in ("1", "true", "yes", "on")


def _list_env(name: str, default: list[str]) -> list[str]:
    value = os.getenv(name)
    if not value:
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings(BaseModel):
    api_title: str = os.getenv("API_TITLE", "Economic Forecast API")

    # Важно: при allow_credentials=True нельзя оставлять ["*"]
    allow_origins: list[str] = _list_env(
        "ALLOW_ORIGINS",
        [
            "http://127.0.0.1:5500",
            "http://localhost:5500",
        ],
    )

    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "DEV_ONLY_CHANGE_ME")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # На локалке False. На HTTPS-сайте обязательно True.
    cookie_secure: bool = _bool_env("COOKIE_SECURE", False)

    # Данные первого и единственного администратора.
    # Используются только если в БД ещё нет админа.
    admin_username: str | None = os.getenv("ADMIN_USERNAME")
    admin_email: str | None = os.getenv("ADMIN_EMAIL")
    admin_password: str | None = os.getenv("ADMIN_PASSWORD")


settings = Settings()