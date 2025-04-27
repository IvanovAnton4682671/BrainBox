import React from "react";
import { useChat } from "../../../utils/stateManager/chatContext";
import { recognizeAudio } from "../../../utils/api/neural";
import { FaRegTrashAlt } from "react-icons/fa";
import styles from "./ChatAudioZone.module.css";

function ChatAudioZone() {
  //получаем поле и метод из состояния
  const { activeService, deleteChat, sendMessage } = useChat();

  //обработка отправки аудио-сообщения через родительский метод взаимодействия с контекстом
  const handleAudioFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file || !activeService) {
      return;
    }
    sendMessage({
      text: file.name,
      isAudio: true,
      type: "user",
    });
    try {
      const result = await recognizeAudio(file);
      sendMessage({
        text: result.text,
        type: "response",
      });
    } catch (error) {
      alert(error);
      sendMessage({
        text: error,
        type: "response",
      });
    }
  };

  //удаление истории чата через состояние после подтверждения
  const handleDeleteChat = () => {
    if (
      activeService &&
      window.confirm("Вы уверены, что хотите удалить текущий чат?")
    ) {
      deleteChat(activeService);
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.buttonUpload}>
        <label htmlFor="audio-upload" className={styles.uploadButton}>
          Загрузить аудио-файл
        </label>
        <input
          id="audio-upload"
          type="file"
          accept="audio/*"
          style={{ display: "none" }}
          onChange={handleAudioFileUpload}
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
