import styles from "./ChatMessageZone.module.css";

function ChatMessageZone({ messages }) {
  return (
    <div className={styles.wrapper}>
      <div className={styles.messageBox}>
        {messages.map((message, index) => (
          <div className={styles.userMessage} key={index}>
            {message}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ChatMessageZone;
