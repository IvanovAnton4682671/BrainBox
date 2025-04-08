import React from "react";
import { useChat } from "../../../utils/stateManager/chatContext";
import { FaRegTrashAlt } from "react-icons/fa";
import { MdClear } from "react-icons/md";
import { MdArrowUpward } from "react-icons/md";
import styles from "./ChatInputZone.module.css";

function ChatInputZone({ handleMessages }) {
  //получаем поле и метод из состояния
  const { activeService, deleteChat } = useChat();
  //состояние для работы с textarea
  const [inputValue, setInputValue] = React.useState("");

  //удаление истории чата через состояние после подтверждения
  const handleDeleteChat = () => {
    if (
      activeService &&
      window.confirm("Вы уверены, что хотите удалить текущий чат?")
    ) {
      deleteChat(activeService);
    }
  };

  //очистка textarea
  const handleInputClear = () => {
    setInputValue("");
  };

  //косвенная работа с состоянием через родительский метод handleMessages
  const handleSendMessage = () => {
    if (inputValue.trim()) {
      handleMessages({ text: inputValue });
      setInputValue("");
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
            Отправить
            <MdArrowUpward className={styles.buttonSubmitImg} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChatInputZone;
