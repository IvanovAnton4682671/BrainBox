import React from "react";
import { useChat } from "../../../utils/stateManager/chatContext";
import { generateAnswer, deleteImageMessages } from "../../../utils/api/image";
import { FaRegTrashAlt } from "react-icons/fa";
import { MdClear } from "react-icons/md";
import { MdArrowUpward } from "react-icons/md";
import styles from "./ChatImageZone.module.css";

function ChatImageZone() {
  //получаем поле и метод из состояния
  const { activeService, deleteChat, sendMessage, startGlobalTask } = useChat();
  //состояние для работы с textarea
  const [inputValue, setInputValue] = React.useState("");
  //состояние для определения статуса загрузки сообщения
  const [isUploading, setIsUploading] = React.useState(false);

  //очистка textarea
  const handleInputClear = () => {
    setInputValue("");
  };

  const handleSendMessage = async () => {
    if (inputValue.trim()) {
      setIsUploading(true);
      try {
        const text = inputValue;
        sendMessage({
          text: text,
          type: "user",
          createdAt: new Date().toISOString(),
          service: "imageGeneration",
        });
        setInputValue("");
        const { task_id } = await generateAnswer(text);
        startGlobalTask(
          "imageGeneration",
          task_id,
          (result) => {
            sendMessage({
              image_uid: result.image_uid,
              type: "response",
              table: "image_chat",
              createdAt: new Date().toISOString(),
              service: "imageGeneration",
            });
          },
          (error) => {
            sendMessage({
              text: "Таймаут генерации",
              type: "response",
              createdAt: new Date().toISOString(),
              service: "imageGeneration",
            });
          }
        );
      } catch (error) {
        console.error("Handle send message error: ", error);
        throw error;
      } finally {
        setIsUploading(false);
      }
    }
  };

  const handleDeleteChat = async () => {
    try {
      if (
        activeService &&
        window.confirm("Вы уверены, что хотите удалить текущий чат?")
      ) {
        await deleteImageMessages();
        deleteChat(activeService);
        alert("Чат успешно удалён!");
      }
    } catch (error) {
      console.error("Handle delete chat error: ", error);
      throw error;
    }
  };

  return (
    <div className={styles.wrapper}>
      <textarea
        className={styles.textArea}
        placeholder="Напишите запрос здесь"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      ></textarea>
      <div className={styles.inputButtons}>
        <div className={styles.buttonDeleteChat} onClick={handleDeleteChat}>
          Удалить чат
          <FaRegTrashAlt className={styles.buttonDeleteChatImg} />
        </div>
        <div className={styles.rightButtons}>
          <div className={styles.buttonClear} onClick={handleInputClear}>
            Очистить
            <MdClear className={styles.buttonClearImg} />
          </div>
          <div className={styles.buttonSubmit} onClick={handleSendMessage}>
            {isUploading ? "Загрузка..." : "Отправить"}
            <MdArrowUpward className={styles.buttonSubmitImg} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChatImageZone;
