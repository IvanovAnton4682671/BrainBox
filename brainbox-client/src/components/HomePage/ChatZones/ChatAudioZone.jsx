import React from "react";
import { useChat } from "../../../utils/stateManager/chatContext";
import {
  uploadAudio,
  recognizeSavedAudio,
  deleteAudioMessages,
} from "../../../utils/api/neural";
import { FaRegTrashAlt } from "react-icons/fa";
import styles from "./ChatAudioZone.module.css";

function ChatAudioZone() {
  //получаем поле и метод из состояния
  const { activeService, deleteChat, sendMessage } = useChat();
  //статус обработки отправленного аудио-файла
  const [isUploading, setIsUploading] = React.useState(false);

  //обработка отправки аудио-сообщения через родительский метод взаимодействия с контекстом
  const handleAudioUpload = async (e) => {
    const file = e.target.files[0];
    if (!file || !activeService) {
      return;
    }
    setIsUploading(true);
    try {
      //загрузка файла
      const uploadResult = await uploadAudio(file);
      if (!uploadResult.audio_uid) {
        throw Error(
          "Incorrect uploadResult.audio_uid = ",
          uploadResult.audio_uid
        );
      }
      //рендер пользовательского сообщения после успешной загрузки
      sendMessage({
        text: uploadResult.filename,
        isAudio: true,
        type: "user",
        audio_uid: uploadResult.audio_uid,
        createdAt: new Date().toISOString(),
      });
      //сразу запрос на распознавание отправленного файла
      const recognitionResult = await recognizeSavedAudio(
        uploadResult.audio_uid
      );
      sendMessage({
        text: recognitionResult.text,
        type: "response",
        createdAt: new Date().toISOString(),
      });
    } catch (error) {
      console.error("Handle audio upload error: ", error);
      throw error;
    } finally {
      setIsUploading(false);
    }
  };

  //удаление истории чата через состояние после подтверждения
  const handleDeleteChat = async () => {
    try {
      if (
        activeService &&
        window.confirm("Вы уверены, что хотите удалить текущий чат?")
      ) {
        await deleteAudioMessages();
        deleteChat(activeService);
        alert("Чат успешно удалён!");
      }
    } catch (error) {
      console.error("Handle delete chat error: ", error);
      throw error;
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.buttonUpload}>
        <label htmlFor="audio-upload" className={styles.uploadButton}>
          {isUploading ? "Загрузка..." : "Отправить аудио-файл"}
        </label>
        <input
          id="audio-upload"
          type="file"
          accept="audio/*"
          onChange={handleAudioUpload}
          disabled={isUploading}
          style={{ display: "none" }}
        />
      </div>
      <div className={styles.buttonDeleteChat} onClick={handleDeleteChat}>
        Удалить чат
        <FaRegTrashAlt className={styles.buttonDeleteChatImg} />
      </div>
    </div>
  );
}

export default ChatAudioZone;
