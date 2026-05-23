from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import get_password_hash, verify_password
from app.core.config import settings
from app.db_models import User


def _normalize(value: str) -> str:
    return value.strip().lower()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_login(db: Session, login: str) -> User | None:
    login = _normalize(login)

    return (
        db.query(User)
        .filter(or_(User.username == login, User.email == login))
        .first()
    )


def create_user(
    db: Session,
    username: str,
    email: str,
    password: str,
    role: str = "user",
) -> User:
    username = _normalize(username)
    email = _normalize(email)

    if role not in ("user", "admin"):
        role = "user"

    existing = (
        db.query(User)
        .filter(or_(User.username == username, User.email == email))
        .first()
    )

    if existing:
        raise ValueError("Пользователь с таким логином или email уже существует")

    if role == "admin":
        existing_admin = db.query(User).filter(User.role == "admin").first()
        if existing_admin:
            raise ValueError("Администратор уже существует")

    user = User(
        username=username,
        email=email,
        password_hash=get_password_hash(password),
        role=role,
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Не удалось создать пользователя. Возможно, данные уже заняты")

    db.refresh(user)
    return user


def authenticate_user(db: Session, login: str, password: str) -> User | None:
    user = get_user_by_login(db, login)

    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def ensure_default_admin(db: Session) -> None:
    existing_admin = db.query(User).filter(User.role == "admin").first()

    if existing_admin:
        return

    if not settings.admin_username or not settings.admin_email or not settings.admin_password:
        print(
            "Администратор не создан: задай ADMIN_USERNAME, "
            "ADMIN_EMAIL и ADMIN_PASSWORD перед первым запуском."
        )
        return

    create_user(
        db=db,
        username=settings.admin_username,
        email=settings.admin_email,
        password=settings.admin_password,
        role="admin",
    )

    print(f"Создан первый администратор: {settings.admin_username}")