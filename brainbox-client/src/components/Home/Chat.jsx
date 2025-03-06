import React from "react";
import styles from "./Chat.module.css";
import ChatMessageZone from "./ChatMessageZone";
import ChatAudioZone from "./ChatAudioZone";
import ChatInputZone from "./ChatInputZone";

function Chat({ selectedService }) {
  const [messages, setMessages] = React.useState([]);

  const generateResponse = () => {
    return "Это автоматический ответ от системы. Ваше сообщение получено!";
  };

  const handleMessages = (message) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: message.text, type: "user", isAudio: message.isAudio || false },
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
        {selectedService === "Речь в текст" ? (
          <ChatAudioZone handleMessages={handleMessages} />
        ) : (
          <ChatInputZone handleMessages={handleMessages} />
        )}
      </div>
    </div>
  );
}

export default Chat;
