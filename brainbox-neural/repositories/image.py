from sqlalchemy.ext.asyncio import AsyncSession
from schemas.image import UserID, ImageUID, ImageMessageInDB, ImageMessageRequest, ImageMessageResponse
from typing import Optional, List
from models.image import ImageMessage
from sqlalchemy import select, desc

class ImageRepository:
    """
    Репозиторий для CRUD-операций для сообщений-картинок
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user_message(self, message: ImageMessageRequest) -> Optional[ImageMessageInDB]:
        try:
            query = ImageMessage(
                user_id=message.user_id,
                is_from_user=True,
                message_text=message.message_text
            )
            self.session.add(query)
            await self.session.commit()
            await self.session.refresh(query)
            return ImageMessageInDB.model_validate(query.to_dict()) if query else None
        except Exception as e:
            await self.session.rollback()
            raise

    async def create_system_message(self, message: ImageMessageResponse) -> Optional[ImageMessageInDB]:
        try:
            query = ImageMessage(
                user_id=message.user_id,
                is_from_user=False,
                image_uid=message.image_uid
            )
            self.session.add(query)
            await self.session.commit()
            await self.session.refresh(query)
            return ImageMessageInDB.model_validate(query.to_dict()) if query else None
        except Exception as e:
            await self.session.rollback()
            raise

    async def get_user_messages(self, user_id: UserID) -> Optional[List[ImageMessageInDB]]:
        try:
            query = select(ImageMessage).where(ImageMessage.user_id == user_id).order_by(desc(ImageMessage.created_at))
            result = await self.session.execute(query)
            messages = result.scalars().all()
            return [ImageMessageInDB.model_validate(msg.to_dict()) for msg in messages] if messages else None
        except Exception as e:
            raise

    async def get_message_by_uid(self, image_uid: ImageUID) -> Optional[ImageMessageInDB]:
        try:
            query = select(ImageMessage).where(ImageMessage.image_uid == str(image_uid))
            result = await self.session.execute(query)
            message = result.scalars().first()
            return ImageMessageInDB.model_validate(message.to_dict()) if message else None
        except Exception as e:
            raise

    async def delete_user_messages(self, user_id: UserID) -> None:
        try:
            messages = await self.get_user_messages(user_id)
            if not messages:
                return
            query = ImageMessage.__table__.delete().where(ImageMessage.user_id == user_id)
            await self.session.execute(query)
            await self.session.commit()
            return
        except Exception as e:
            await self.session.rollback()
            raise