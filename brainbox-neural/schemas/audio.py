from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime

class AudioMessageBase(BaseModel):
    user_id: int = Field(..., description="ID пользователя, которому принадлежит сообщение (его собственное или ответ на его сообщение)")
    is_from_user: bool = Field(..., description="Флаг, обозначающий чьё сообщение")
    message_text: str = Field(..., min_length=1, description="Текст сообщения")

class AudioMessageCreate(AudioMessageBase):
    audio_uid: Optional[UUID4] = Field(None, description="Специальный ID аудио-файла")

class AudioMessageResponse(AudioMessageBase):
    id: int = Field(..., description="ID сообщения")
    audio_uid: Optional[UUID4] = Field(None, description="Специальный ID аудио-файла")
    created_at: datetime = Field(..., description="Дата и время создания сообщения (UTC)")

    class Config:
        from_attributes = True

class AudioUploadResponse(BaseModel):
    message: str = Field(..., description="Статус обработки")
    text: Optional[str] = Field(None, description="Распознанный текст")
    audio_uid: Optional[str] = Field(None, description="Специальный ID аудио-сообщения")