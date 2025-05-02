from databases.postgres import Base
from sqlalchemy import Column, Integer, Boolean, String, DateTime
from sqlalchemy.sql import func

class AudioMessage(Base):
    """
    Модель сообщения распознавания аудио для SQLAlchemy
    """
    __tablename__ = "audio_chat"

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
    audio_uid = Column(
        String(36),
        nullable=True,
        comment="Специальный ID аудио-файла"
    )
    created_at = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
        comment="Дата и время создания сообщения (UTC)"
    )

    def __repr__(self) -> str:
        return f"<Message(id={self.id};user_id={self.user_id};system_answer={self.is_from_user});text={self.message_text};audio_path={self.audio_uid if self.audio_uid else "None"};created_at={self.created_at}>"