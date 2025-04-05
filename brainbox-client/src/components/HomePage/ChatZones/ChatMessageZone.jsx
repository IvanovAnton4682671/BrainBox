import React from "react";
import { FaFileAudio } from "react-icons/fa";
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
          </div>
        ))}
      </div>
    </div>
  );
}

export default ChatMessageZone;
