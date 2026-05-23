from sqlalchemy import Boolean, Column, DateTime, Index, Integer, String, func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    # Возможные роли: user / admin
    role = Column(String(20), nullable=False, default="user", index=True)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Защита на уровне БД: только один пользователь с role="admin"
    __table_args__ = (
        Index(
            "ix_users_only_one_admin",
            "role",
            unique=True,
            sqlite_where=(role == "admin"),
        ),
    )