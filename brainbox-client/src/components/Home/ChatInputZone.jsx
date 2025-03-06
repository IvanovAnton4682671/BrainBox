import React from "react";
import styles from "./ChatInputZone.module.css";
import { FaRegTrashAlt } from "react-icons/fa";
import { FaArrowAltCircleUp } from "react-icons/fa";

function ChatInputZone({ handleMessages }) {
  const [inputValue, setInputValue] = React.useState("");

  const handleInputClear = () => {
    setInputValue("");
  };

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
        <FaRegTrashAlt
          className={styles.buttonTrash}
          onClick={handleInputClear}
        />
        <FaArrowAltCircleUp
          className={styles.buttonSubmit}
          onClick={handleSendMessage}
        />
      </div>
    </div>
  );
}

export default ChatInputZone;
