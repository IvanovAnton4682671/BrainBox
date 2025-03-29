import React from "react";
import styles from "./ChatAudioZone.module.css";
import { FaRegTrashAlt } from "react-icons/fa";

function ChatAudioZone({ handleMessages }) {
  const handleAudioFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const fileName = file.name;
      handleMessages({ text: fileName, isAudio: true });
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
      <div className={styles.buttonDeleteChat}>
        Удалить чат
        <FaRegTrashAlt className={styles.buttonDeleteChatImg} />
      </div>
    </div>
  );
}

export default ChatAudioZone;
