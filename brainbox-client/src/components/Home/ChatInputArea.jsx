import styles from "./ChatInputArea.module.css";

function ChatInputArea() {
  return (
    <div className={styles.wrapper}>
      <textarea
        className={styles.textArea}
        placeholder="Напишите запрос здесь"
      ></textarea>
    </div>
  );
}

export default ChatInputArea;
