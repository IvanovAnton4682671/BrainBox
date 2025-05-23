from pydantic import BaseModel, Field, UUID4
from typing import Optional
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
    message_text: Optional[str] = Field(
        None,
        description="Текст сообщения"
    )

class ImageUID(BaseModel):
    image_uid: Optional[UUID4] = Field(
        None,
        description="Специальный ID картинки"
    )

class CreatedAt(BaseModel):
    created_at: datetime = Field(
        ...,
        description="Дата и время создания сообщения (UTC)"
    )

class ImageMessageInDB(ID, UserID, IsFromUser, MessageText, ImageUID, CreatedAt):
    pass

class ImageMessageRequest(UserID, MessageText):
    pass

class ImageMessageResponse(UserID, ImageUID):
    pass