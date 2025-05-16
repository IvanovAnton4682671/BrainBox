from databases.postgresql import Base
from sqlalchemy import Column, Integer, Boolean, String, DateTime
from sqlalchemy.sql import func

class TextMessage(Base):
    """
    Модель записи таблицы text_chat для SQLAlchemy
    """
    __tablename__ = "text_chat"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="ID сообщения"
    )
    user_id = Column(
        Integer,
        nullable=False,
        comment="ID пользователя, которому принадлежит сообщение (его собственное или ответ на его сообщение)"
    )
    is_from_user = Column(
        Boolean,
        nullable=False,
        comment="Флаг, обозначающий чьё сообщение"
    )
    message_text = Column(
        String,
        nullable=False,
        comment="Текст сообщения"
    )
    created_at = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
        comment="Дата и время создания сообщения (UTC)"
    )

    def __repr__(self) -> str:
        return f"<Message(id={self.id};user_id={self.user_id};system_answer={self.is_from_user});text={self.message_text};created_at={self.created_at}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "is_from_user": self.is_from_user,
            "message_text": self.message_text,
            "created_at": self.created_at
        }