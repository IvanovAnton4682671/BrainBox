import React from "react";
import styles from "./ChatAudioZone.module.css";

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
  );
}

export default ChatAudioZone;
