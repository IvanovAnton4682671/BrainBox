from database.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

class User(Base):
    """
    Модель пользователя для SQLAlchemy
    """
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="ID пользователя"
    )
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        comment="Уникальная почта пользователя"
    )
    name = Column(
        String(20),
        unique=True,
        nullable=False,
        comment="Уникальное имя пользователя"
    )
    password_hash = Column(
        String(255),
        nullable=False,
        comment="Хэш пароля пользователя (bcrypt)"
    )
    created_at = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
        comment="Дата и время создания записи (UTC)"
    )
    last_login = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
        comment="Дата и время последнего входа в запись (UTC)"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, name={self.name}, password_hash={self.password_hash}, created_at={self.created_at}), last_login={self.last_login}>"