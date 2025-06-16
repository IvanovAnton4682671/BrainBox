import React from "react";
import { useChat } from "../../../utils/stateManager/chatContext";
import {
  uploadAudio,
  recognizeSavedAudio,
  checkTaskStatus,
  deleteAudioMessages,
} from "../../../utils/api/audio";
import { useWebSocketContext } from "../../../utils/stateManager/wsContext";
import { FaRegTrashAlt } from "react-icons/fa";
import styles from "./ChatAudioZone.module.css";

function ChatAudioZone() {
  //получаем поле и метод из состояния
  const {
    activeService,
    deleteChat,
    sendMessage,
    addTypingIndicator,
    removeTypingIndicator,
  } = useChat();
  //статус обработки отправленного аудио-файла
  const [isUploading, setIsUploading] = React.useState(false);
  const { addMessageHandler } = useWebSocketContext();
  //интервал опроса task_id
  //const intervalsRef = React.useRef({});

  React.useEffect(() => {
    const handler = (message) => {
      if (
        message.type === "task_completed" &&
        pendingTasks.current[message.task_id]
      ) {
        removeTypingIndicator("speechToText");
        console.log(`Полученное сообщение: ${message}`);
        sendMessage({
          text: message.result.text,
          type: "response",
          createdAt: new Date().toISOString(),
          service: "speechToText",
        });
        delete pendingTasks.current[message.task_id];
      }
    };
    const unsubscribe = addMessageHandler(handler);
    return unsubscribe;
  }, [removeTypingIndicator, sendMessage]);

  const pendingTasks = React.useRef({});

  /*React.useEffect(() => {
    return () => {
      Object.values(intervalsRef.current).forEach((interval) => {
        clearInterval(interval);
      });
      intervalsRef.current = {};
    };
  }, []);*/

  //обработка отправки аудио-сообщения через родительский метод взаимодействия с контекстом
  const handleAudioUpload = async (e) => {
    const file = e.target.files[0];
    if (!file || !activeService) {
      return;
    }
    setIsUploading(true);
    try {
      //загрузка файла
      const uploadResult = await uploadAudio(file);
      if (!uploadResult.audio_uid) {
        throw Error(
          "Incorrect uploadResult.audio_uid = ",
          uploadResult.audio_uid
        );
      }
      //рендер пользовательского сообщения после успешной загрузки
      sendMessage({
        text: uploadResult.filename,
        isAudio: true,
        type: "user",
        audio_uid: uploadResult.audio_uid,
        createdAt: new Date().toISOString(),
        service: "speechToText",
      });
      addTypingIndicator("speechToText");
      //сразу запрос на распознавание отправленного файла
      const { task_id } = await recognizeSavedAudio(uploadResult.audio_uid);
      pendingTasks.current[task_id] = true;
      /*let attempts = 0;
      const maxAttempts = 120;
      intervalsRef.current[task_id] = setInterval(async () => {
        attempts++;
        try {
          const statusResponse = await checkTaskStatus(task_id);
          if (statusResponse.status === "completed") {
            clearInterval(intervalsRef.current[task_id]);
            delete intervalsRef.current[task_id];
            removeTypingIndicator("speechToText");
            sendMessage({
              text: statusResponse.result.text,
              type: "response",
              createdAt: new Date().toISOString(),
              service: "speechToText",
            });
          } else if (attempts >= maxAttempts) {
            clearInterval(intervalsRef.current[task_id]);
            delete intervalsRef.current[task_id];
            removeTypingIndicator("speechToText");
            sendMessage({
              text: "Таймаут распознавания",
              type: "response",
              createdAt: new Date().toISOString(),
              service: "speechToText",
            });
          }
        } catch (error) {
          clearInterval(intervalsRef.current[task_id]);
          delete intervalsRef.current[task_id];
          removeTypingIndicator("speechToText");
          console.error("Handle audio upload error: ", error);
          throw error;
        }
      }, 1000);*/
    } catch (error) {
      removeTypingIndicator("speechToText");
      console.error("Handle audio upload error: ", error);
      throw error;
    } finally {
      setIsUploading(false);
    }
  };

  //удаление истории чата через состояние после подтверждения
  const handleDeleteChat = async () => {
    try {
      if (
        activeService &&
        window.confirm("Вы уверены, что хотите удалить текущий чат?")
      ) {
        await deleteAudioMessages();
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
      <div className={styles.buttonUpload}>
        <label htmlFor="audio-upload" className={styles.uploadButton}>
          {isUploading ? "Загрузка..." : "Отправить аудио-файл"}
        </label>
        <input
          id="audio-upload"
          type="file"
          accept="audio/*"
          onChange={handleAudioUpload}
          disabled={isUploading}
          style={{ display: "none" }}
        />
      </div>
      <div className={styles.buttonDeleteChat} onClick={handleDeleteChat}>
        Удалить чат
        <FaRegTrashAlt className={styles.buttonDeleteChatImg} />
      </div>
    </div>
  );
}

export default ChatAudioZone;
