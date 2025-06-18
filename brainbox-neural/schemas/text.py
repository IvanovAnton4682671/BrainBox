from pydantic import BaseModel, Field
from datetime import datetime

class ID(BaseModel):
    id: int = Field(
        ...,
        description="ID сообщения"
    )

class UserID(BaseModel):
    user_id: int = Field(
        ...,
        description="ID пользователя, которому принадлежит сообщение (его собственное или ответ на его сообщение)"
    )

class IsFromUser(BaseModel):
    is_from_user: bool = Field(
        ...,
        description="Флаг, обозначающий чьё сообщение"
    )

class MessageText(BaseModel):
    message_text: str = Field(
        ...,
        min_length=1,
        description="Текст сообщения"
    )

class CreatedAt(BaseModel):
    created_at: datetime = Field(
        ...,
        description="Дата и время создания сообщения (UTC)"
    )

class TextMessageInDB(ID, UserID, IsFromUser, MessageText, CreatedAt):
    pass

class TextMessageCreate(UserID, IsFromUser, MessageText):
    pass

class TextMessageResponse(IsFromUser, MessageText, CreatedAt):
    pass

    def to_dict(self):
        return {
            "is_from_user": self.is_from_user,
            "message_text": self.message_text,
            "created_at": self.created_at.isoformat()
        }