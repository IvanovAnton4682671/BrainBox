import React from "react";
import {
  generateAnswer,
  deleteTextMessages,
  checkTaskStatus,
} from "../../../utils/api/text";
import { useChat } from "../../../utils/stateManager/chatContext";
import { FaRegTrashAlt } from "react-icons/fa";
import { MdClear } from "react-icons/md";
import { MdArrowUpward } from "react-icons/md";
import styles from "./ChatTextZone.module.css";

function ChatTextZone() {
  //получаем поле и метод из состояния
  const {
    activeService,
    deleteChat,
    sendMessage,
    addTypingIndicator,
    removeTypingIndicator,
  } = useChat();
  //состояние для работы с textarea
  const [inputValue, setInputValue] = React.useState("");
  //состояние для определения статуса загрузки сообщения
  const [isUploading, setIsUploading] = React.useState(false);
  //интервал опроса по task_id
  const intervalsRef = React.useRef({});

  React.useEffect(() => {
    return () => {
      Object.values(intervalsRef.current).forEach((interval) => {
        clearInterval(interval);
      });
      intervalsRef.current = {};
    };
  }, []);

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
        //сразу начинаем опрос по task_id
        setInputValue("");
        addTypingIndicator("chatBot");
        const { task_id } = await generateAnswer(text);
        let attempts = 0;
        const maxAttempts = 120;
        intervalsRef.current[task_id] = setInterval(async () => {
          attempts++;
          try {
            const statusResponse = await checkTaskStatus(task_id);
            if (statusResponse.status === "completed") {
              clearInterval(intervalsRef.current[task_id]);
              delete intervalsRef.current[task_id];
              removeTypingIndicator("chatBot");
              sendMessage({
                text: statusResponse.result.message_text,
                type: "response",
                table: "text_chat",
                createdAt: new Date().toISOString(),
                service: "chatBot",
              });
            } else if (attempts >= maxAttempts) {
              clearInterval(intervalsRef.current[task_id]);
              delete intervalsRef.current[task_id];
              removeTypingIndicator("chatBot");
              sendMessage({
                text: "Таймаут генерации",
                type: "response",
                createdAt: new Date().toISOString(),
                service: "chatBot",
              });
            }
          } catch (error) {
            clearInterval(intervalsRef.current[task_id]);
            delete intervalsRef.current[task_id];
            removeTypingIndicator("chatBot");
            console.error("Handle send message error: ", error);
            throw error;
          }
        }, 1000);
      } catch (error) {
        removeTypingIndicator("chatBot");
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
