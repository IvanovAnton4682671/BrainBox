import React from "react";
import ChatMessageZone from "../ChatZones/ChatMessageZone";
import ChatAudioZone from "../ChatZones/ChatAudioZone";
import ChatInputZone from "../ChatZones/ChatInputZone";
import { useChat } from "../../../utils/StateManager/ChatContext";
import styles from "./Chat.module.css";

function Chat() {
  //получаем состояние и метод из контекста
  const { activeService, chats, sendMessage } = useChat();
  //фильтруем сообщения для текущего активного сервиса
  const messages = activeService ? chats[activeService] : [];

  //автоматический ответ
  const generateResponse = () => {
    return "Это автоматический ответ от системы. Ваше сообщение получено!";
  };

  //обработка отправляемого сообщения от пользователя из всех чатов
  const handleMessages = (message) => {
    if (!activeService) {
      return;
    }

    //отправка сообщения пользователя
    sendMessage({ ...message, type: "user" });

    //заглушка для ответа
    setTimeout(() => {
      sendMessage({
        text: generateResponse(),
        type: "response",
      });
    }, 500);
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.chatWindow}>
        <ChatMessageZone messages={messages} />
      </div>
      <div
        className={
          activeService === "speechToText"
            ? styles.chatAudioZone
            : styles.chatInputZone
        }
      >
        {activeService === "speechToText" ? (
          <ChatAudioZone handleMessages={handleMessages} />
        ) : (
          <ChatInputZone handleMessages={handleMessages} />
        )}
      </div>
    </div>
  );
}

export default Chat;
