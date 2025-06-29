from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.audio import AudioRepository
import io
from pydub import AudioSegment
import speech_recognition as sr
from schemas.audio import AudioUploadResponse, AudioMessageCreate
from core.storage import audio_storage
import os

logger = setup_logger("services.audio")

class AudioService:
    def __init__(self, session: AsyncSession):
        self.repo = AudioRepository(session)

    def _recognize_audio(self, audio_data: bytes, file_extension: str) -> dict:
        """
        Распознаёт речь из аудио-файла с очисткой ресурсов
        """
        logger.info("Пришёл запрос на распознавание речи")
        try:
            with io.BytesIO() as wav_buffer:
                if file_extension.lower() != "wav":
                    audio = AudioSegment.from_file(io.BytesIO(audio_data), format=file_extension)
                    audio = audio.set_channels(1).set_frame_rate(16000)
                    audio.export(wav_buffer, format="wav")
                else:
                    wav_buffer.write(audio_data)
                    wav_buffer.seek(0)
                recognizer = sr.Recognizer()
                with sr.AudioFile(wav_buffer) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language="ru-RU")
                    logger.info("Речь распознана, возвращаем ответ")
                    return { "text": text, "status": "success" }
        except Exception as e:
            logger.error(f"При распознавании произошла ошибка: {str(e)}", exc_info=True)
            raise

    async def _save_system_response(self, user_id: int, text: str) -> None:
        """
        Сохранение распознанного текста
        """
        try:
            system_message = AudioMessageCreate(
                user_id=user_id,
                is_from_user=False,
                message_text=text,
                audio_uid=None
            )
            await self.repo.create_message(system_message)
        except Exception as e:
            logger.error(f"Ошибка при сохранении системного ответа: {str(e)}", exc_info=True)
            raise

    async def recognize_saved_audio(self, user_id: int, audio_uid: str) -> AudioUploadResponse:
        """
        Распознаёт уже сохранённый файл
        """
        try:
            logger.info("Начинаем процесс распознавания аудио-файла...")
            #получение информации о сообщении из БД
            message = await self.repo.get_message_by_uid(audio_uid)
            if not message or message.user_id != user_id:
                raise ValueError("Audio message not found or access denied")
            #скачивание файла из MinIO
            audio_data = await audio_storage.download_audio(audio_uid)
            #определение расширения файла
            file_extension = os.path.splitext(message.message_text)[1][1:] if "." in message.message_text else ".mp3"
            #распознаём текст
            recognition_result = self._recognize_audio(audio_data, file_extension)
            recognition_text = recognition_result["text"]
            #сохраняем системный ответ
            await self._save_system_response(user_id, recognition_text)
            logger.info("Аудио-файл успешно распознан, возвращаем ответ")
            return AudioUploadResponse(
                message="Аудио-файл успешно распознан!",
                text=recognition_text,
                audio_uid=audio_uid
            )
        except Exception as e:
            logger.error(f"При распознавании аудио-файла произошла ошибка: {str(e)}", exc_info=True)
            raise

    async def delete_user_messages(self, user_id: int) -> dict:
        """
        Удаляет всю историю чата
        """
        try:
            logger.info("Удаляем все сообщения и аудио-файлы")
            messages = await self.repo.get_user_messages(user_id)
            if not messages:
                return { "success": True }
            for msg in messages:
                if msg.audio_uid:
                    audio_storage.client.remove_object(
                        audio_storage.bucket,
                        str(msg.audio_uid)
                    )
            await self.repo.delete_user_messages(user_id)
            return { "success": True }
        except Exception as e:
            logger.error(f"Ошибка при удалении истории чата: {str(e)}", exc_info=True)
            raise