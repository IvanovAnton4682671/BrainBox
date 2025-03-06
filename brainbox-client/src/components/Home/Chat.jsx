import React from "react";
import styles from "./Chat.module.css";
import ChatMessageZone from "./ChatMessageZone";
import ChatInputZone from "./ChatInputZone";

function Chat() {
  const [messages, setMessages] = React.useState([]);

  const generateResponse = () => {
    return "Это автоматический ответ от системы. Ваше сообщение получено!";
  };

  const handleMessages = (message) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: message, type: "user" },
    ]);
    const response = generateResponse();
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: response, type: "response" },
    ]);
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
