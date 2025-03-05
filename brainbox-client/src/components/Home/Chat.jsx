import React from "react";
import styles from "./Chat.module.css";
import ChatMessageZone from "./ChatMessageZone";
import ChatInputZone from "./ChatInputZone";

function Chat() {
  const [messages, setMessages] = React.useState([]);

  const handleMessages = (message) => {
    setMessages([...messages, message]);
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.chatWindow}>
        <ChatMessageZone messages={messages} />
      </div>
      <div className={styles.chatInputZone}>
        <ChatInputZone handleMessages={handleMessages} />
      </div>
    </div>
  );
}

export default Chat;
