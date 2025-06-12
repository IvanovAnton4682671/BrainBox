import React from "react";
import { FaFileAudio } from "react-icons/fa";
import { downloadAudio } from "../../../utils/api/audio";
import { downloadImage } from "../../../utils/api/image";
import ReactMarkdown from "react-markdown";
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

  const handleDownloadAudio = async (audio_uid) => {
    try {
      await downloadAudio(audio_uid);
    } catch (error) {
      console.error("Handle download audio error: ", error);
      throw error;
    }
  };

  const handleDownloadImage = async (image_uid) => {
    try {
      await downloadImage(image_uid);
    } catch (error) {
      console.error("Handle download image error: ", error);
      throw error;
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.messageBox} ref={messageBoxRef}>
        {messages.map((message, index) => (
          <div
            key={message.id || index}
            className={
              message.type === "user"
                ? styles.userMessage
                : message.type === "typing"
                ? styles.typingMessage
                : styles.responseMessage
            }
          >
            {message.type === "typing" && (
              <img
                className={styles.typingIndicator}
                src="./ellipsis.gif"
                alt="Typing..."
              ></img>
            )}
            {message.isAudio && <FaFileAudio className={styles.audioImg} />}
            {message.table === "text_chat" && message.type === "response" ? (
              <ReactMarkdown>{message.text}</ReactMarkdown>
            ) : (
              message.text
            )}
            {message.image_uid && (
              <div className={styles.imageWrapper}>
                <img
                  src={`http://localhost:8000/image/view/${message.image_uid}`}
                  alt={"Generated картинка"}
                  className={styles.myImage}
                />
                <button
                  onClick={() => handleDownloadImage(message.image_uid)}
                  className={styles.downloadButton}
                >
                  Скачать
                </button>
              </div>
            )}
            {message.audio_uid && (
              <button
                onClick={() => handleDownloadAudio(message.audio_uid)}
                className={styles.downloadButton}
              >
                Скачать
              </button>
            )}
            {message.type !== "typing" && (
              <span className={styles.messageDate}>
                {message.createdAt && formatDate(message.createdAt)}
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ChatMessageZone;
