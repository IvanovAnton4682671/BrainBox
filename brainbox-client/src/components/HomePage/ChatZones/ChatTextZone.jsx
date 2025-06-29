import React from "react";
import { generateAnswer, deleteTextMessages } from "../../../utils/api/text";
import { useChat } from "../../../utils/stateManager/chatContext";
import { FaRegTrashAlt } from "react-icons/fa";
import { MdClear } from "react-icons/md";
import { MdArrowUpward } from "react-icons/md";
import styles from "./ChatTextZone.module.css";

function ChatTextZone() {
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

  //косвенная работа с состоянием через родительский метод handleMessages
  const handleSendMessage = async () => {
    if (inputValue.trim()) {
      setIsUploading(true);
      try {
        const text = inputValue;
        sendMessage({
          text: text,
          type: "user",
          createdAt: new Date().toISOString(),
          service: "chatBot",
        });
        setInputValue("");
        const { task_id } = await generateAnswer(text);
        startGlobalTask(
          "chatBot",
          task_id,
          (result) => {
            sendMessage({
              text: result.message_text,
              type: "response",
              table: "text_chat",
              createdAt: new Date().toISOString(),
              service: "chatBot",
            });
          },
          (error) => {
            sendMessage({
              text: "Таймаут генерации",
              type: "response",
              createdAt: new Date().toISOString(),
              service: "chatBot",
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

  //удаление истории чата через состояние после подтверждения
  const handleDeleteChat = async () => {
    try {
      if (
        activeService &&
        window.confirm("Вы уверены, что хотите удалить текущий чат?")
      ) {
        await deleteTextMessages();
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

export default ChatTextZone;
