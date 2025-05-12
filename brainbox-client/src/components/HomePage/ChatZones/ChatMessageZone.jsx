import React from "react";
import { FaFileAudio } from "react-icons/fa";
import { downloadAudio } from "../../../utils/api/audio";
import styles from "./ChatMessageZone.module.css";

function ChatMessageZone({ messages }) {
  //ссылка на скроллбар для автоматической прокрутки сообщений вниз
  const messageBoxRef = React.useRef(null);

  //реализация автоматической прокрутки при получении нового сообщения
  React.useEffect(() => {
    if (messageBoxRef.current) {
      messageBoxRef.current.scrollTop = messageBoxRef.current.scrollHeight;
    }
  }, [messages]);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString("ru-RU", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const handleDownload = async (audio_uid, filename) => {
    try {
      await downloadAudio(audio_uid, filename);
    } catch (error) {
      console.error("Handle download error: ", error);
      throw error;
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.messageBox} ref={messageBoxRef}>
        {messages.map((message, index) => (
          <div
            key={index}
            className={
              message.type === "user"
                ? styles.userMessage
                : styles.responseMessage
            }
          >
            {message.isAudio && <FaFileAudio className={styles.audioImg} />}
            {message.text}
            {message.audio_uid && (
              <button
                onClick={() => handleDownload(message.audio_uid, message.text)}
                className={styles.downloadButton}
              >
                Скачать
              </button>
            )}
            <span className={styles.messageDate}>
              {message.createdAt && formatDate(message.createdAt)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ChatMessageZone;
