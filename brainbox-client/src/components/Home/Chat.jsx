import styles from "./Chat.module.css";
import ChatInputArea from "./ChatInputArea";

function Chat() {
  return (
    <div className={styles.wrapper}>
      <div className={styles.chatWindow}>
        <p>chatWindow</p>
      </div>
      <div className={styles.chatInputZone}>
        <ChatInputArea />
      </div>
    </div>
  );
}

export default Chat;
