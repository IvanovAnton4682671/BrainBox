from core.logger import setup_logger
from pathlib import Path
from pydub import AudioSegment
import speech_recognition as sr
import os

logger = setup_logger("services/audio.py")

def recognize_audio(audio_file_path: str) -> dict:
    logger.info("Пришёл запрос на распознавание речи!")
    temp_wav_path = None
    try:
        file_extension = Path(audio_file_path).suffix[1:].lower()
        if file_extension != "wav":
            audio = AudioSegment.from_file(audio_file_path, format=file_extension)
            audio = audio.set_channels(1).set_frame_rate(16000)
            temp_wav_path = "temp.wav"
            audio.export(temp_wav_path, format="wav")
        else:
            temp_wav_path = audio_file_path
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_wav_path) as source:
            audio_data = recognizer.record(source)
            try:
                text_from_audio = recognizer.recognize_google(audio_data, language="ru-RU")
                logger.info("Речь успешно сгенерирована!")
                return {"text": text_from_audio}
            except Exception as e:
                return {"text": str(e)}
    except Exception as e:
        return {"text": str(e)}
    finally:
        if temp_wav_path and temp_wav_path != audio_file_path and os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)