import React from "react";
import { useChat } from "../../../utils/stateManager/chatContext";
import { FaRegTrashAlt } from "react-icons/fa";
import styles from "./ChatAudioZone.module.css";

function ChatAudioZone({ handleMessages }) {
  //получаем поле и метод из состояния
  const { activeService, deleteChat } = useChat();

  //обработка отправки аудиосообщения через родительский метод взаимодействия с контекстом
  const handleAudioFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      handleMessages({
        text: file.name,
        isAudio: true,
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
          Загрузить аудиофайл
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
