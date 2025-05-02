from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.audio import AudioRepository
import io
from pydub import AudioSegment
import speech_recognition as sr
from schemas.audio import AudioUploadResponse, AudioMessageCreate
from core.storage import audio_storage
import os

logger = setup_logger("services/audio.py")

class AudioService:
    def __init__(self, session: AsyncSession):
        self.repo = AudioRepository(session)

    def _recognize_audio(self, audio_data: bytes, file_extension: str) -> dict:
        """
        Распознаёт речь из аудио-файла с очисткой ресурсов
        """
        logger.info("Пришёл запрос на распознавание речи!")
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

    async def process_audio_message(self, user_id: int, file_data: bytes, file_name: str) -> AudioUploadResponse:
        try:
            #сохраняем аудио-файл в MinIO
            audio_uid = await audio_storage.upload_audio(file_data)
            #распознаём текст
            file_extension = os.path.splitext(file_name)[1][1:]
            recognition_result = self._recognize_audio(file_data, file_extension)
            recognition_text = recognition_result["text"]
            #сохраняем запись пользователя
            await self.repo.create_message(AudioMessageCreate(
                user_id=user_id,
                is_from_user=True,
                message_text=file_name,
                audio_uid=audio_uid
            ))
            #сохраняем системный ответ
            await self._save_system_response(user_id, recognition_text)
            return AudioUploadResponse(
                message="Аудио-файл успешно распознан!",
                text=recognition_text,
                audio_uid=audio_uid
            )
        except Exception as e:
            logger.error(f"При распознавании произошла ошибка: {str(e)}", exc_info=True)