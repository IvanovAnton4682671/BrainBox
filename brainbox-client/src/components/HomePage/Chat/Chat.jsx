import React from "react";
import ChatMessageZone from "../ChatZones/ChatMessageZone";
import ChatAudioZone from "../ChatZones/ChatAudioZone";
import ChatInputZone from "../ChatZones/ChatInputZone";
import { useChat } from "../../../utils/stateManager/chatContext";
import styles from "./Chat.module.css";

function Chat() {
  //получаем состояние и метод из контекста
  const { activeService, chats } = useChat();
  //фильтруем сообщения для текущего активного сервиса
  const messages = activeService ? chats[activeService] : [];

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
          <ChatAudioZone />
        ) : (
          <ChatInputZone />
        )}
      </div>
    </div>
  );
}

export default Chat;
