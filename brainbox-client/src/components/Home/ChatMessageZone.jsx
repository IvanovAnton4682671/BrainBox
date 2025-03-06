import React from "react";
import styles from "./ChatMessageZone.module.css";

function ChatMessageZone({ messages }) {
  const messageBoxRef = React.useRef(null);

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
            {message.text}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ChatMessageZone;
