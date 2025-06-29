import React from "react";
import { useCallback, useEffect } from "react";
import { checkTaskStatus } from "../api/task";

//создание контекста для управления состоянием чатов
const ChatContext = React.createContext();

//начальное состояние чатов для всех сервисов
const initialChats = {
  speechToText: [],
  imageGeneration: [],
  chatBot: [],
};

const getTableByService = (serviceId) => {
  if (serviceId === "speechToText") {
    return "audio_chat";
  } else if (serviceId === "imageGeneration") {
    return "image_chat";
  } else {
    return "text_chat";
  }
};

//редьюсер для управления изменениями состояния
const chatReducer = (state, action) => {
  switch (action.type) {
    case "SELECT_SERVICE":
      //выбор активного сервиса: обновляем activeService в состоянии
      return { ...state, activeService: action.payload };
    case "SEND_MESSAGE":
      //добавление нового сообщения: добавляем в массив активного сервиса
      return {
        ...state,
        chats: {
          ...state.chats,
          [action.payload.service || state.activeService]: [
            ...state.chats[action.payload.service || state.activeService],
            {
              ...action.payload,
              table:
                action.payload.table ||
                getTableByService(
                  action.payload.service || state.activeService
                ),
            },
          ],
        },
      };
    case "ADD_TYPING_INDICATOR":
      return {
        ...state,
        chats: {
          ...state.chats,
          [action.payload.service]: [
            ...state.chats[action.payload.service],
            {
              id: `typing-indicator-${action.payload.taskId}`,
              type: "typing",
              service: action.payload.service,
              taskId: action.payload.taskId,
            },
          ],
        },
      };
    case "REMOVE_TYPING_INDICATOR":
      return {
        ...state,
        chats: {
          ...state.chats,
          [action.payload.service]: state.chats[action.payload.service].filter(
            (msg) => msg.id !== `typing-indicator-${action.payload.taskId}`
          ),
        },
      };
    case "START_TASK":
      return {
        ...state,
        tasks: new Map(state.tasks).set(action.payload.taskId, {
          service: action.payload.service,
          intervalId: action.payload.intervalId,
        }),
      };
    case "STOP_TASK":
      const newTasks = new Map(state.tasks);
      newTasks.delete(action.payload.taskId);
      return { ...state, tasks: newTasks };
    case "DELETE_CHAT":
      //очистка чата: заменяем массив сообщений сервиса пустым
      return { ...state, chats: { ...state.chats, [action.payload]: [] } };
    case "LOAD_CHATS":
      //загрузка чатов: заменяем текущие чаты сохраненными данными
      return { ...state, chats: action.payload };
    case "LOAD_SERVER_CHATS":
      const newState = { ...state };
      if (action.payload.audioMessages) {
        newState.chats.speechToText = (action.payload.audioMessages || [])
          .filter((msg) => msg.table === "audio_chat") //только аудио-сообщения
          .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
          .map((msg) => ({
            table: msg.table,
            text: msg.message_text,
            isAudio: Boolean(msg.audio_uid),
            type: msg.is_from_user ? "user" : "response",
            audio_uid: msg.audio_uid,
            createdAt: msg.created_at,
          }));
      }
      if (action.payload.imageMessages) {
        newState.chats.imageGeneration = (action.payload.imageMessages || [])
          .filter((msg) => msg.table === "image_chat") //только картинки-сообщения
          .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
          .map((msg) => ({
            table: msg.table,
            text: msg.message_text,
            type: msg.is_from_user ? "user" : "response",
            image_uid: msg.image_uid,
            createdAt: msg.created_at,
          }));
      }
      if (action.payload.textMessages) {
        newState.chats.chatBot = (action.payload.textMessages || [])
          .filter((msg) => msg.table === "text_chat") //только текстовые сообщения
          .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
          .map((msg) => ({
            table: msg.table,
            text: msg.message_text,
            type: msg.is_from_user ? "user" : "response",
            createdAt: msg.created_at,
          }));
      }
      return newState;
    default:
      return state;
  }
};

//провайдер контекста (основной компонент)
export const ChatProvider = ({ children }) => {
  //используем useReducer для управления сложным состоянием
  const [state, dispatch] = React.useReducer(chatReducer, {
    chats: initialChats, //начальное состояние чатов
    activeService: null, //изначально ни один сервис не выбран,
    tasks: new Map(), //для хранения активных задач
  });

  //эффект для загрузки сохраненных чатов из Local Storage при монтировании
  React.useEffect(() => {
    const savedChats = JSON.parse(localStorage.getItem("chats"));
    if (savedChats) {
      dispatch({ type: "LOAD_CHATS", payload: savedChats });
    }
  }, []); //пустой массив зависимостей = выполнить только при монтировании

  //эффект для автоматического сохранения чатов в Local Storage при изменениях
  React.useEffect(() => {
    localStorage.setItem("chats", JSON.stringify(state.chats));
  }, [state.chats]); //срабатывает при любом изменении state.chats

  const startGlobalTask = useCallback(
    (serviceType, taskId, resultHandler, errorHandler) => {
      dispatch({
        type: "ADD_TYPING_INDICATOR",
        payload: { service: serviceType, taskId },
      });

      let attempts = 0;
      const maxAttempts = 120;

      const intervalId = setInterval(async () => {
        attempts++;
        try {
          const statusResponse = await checkTaskStatus(taskId, serviceType);
          if (statusResponse.status === "completed") {
            clearInterval(intervalId);
            dispatch({ type: "STOP_TASK", payload: { taskId } });
            dispatch({
              type: "REMOVE_TYPING_INDICATOR",
              payload: { service: serviceType, taskId },
            });
            resultHandler(statusResponse.result);
          } else if (attempts >= maxAttempts) {
            clearInterval(intervalId);
            dispatch({ type: "STOP_TASK", payload: { taskId } });
            dispatch({
              type: "REMOVE_TYPING_INDICATOR",
              payload: { service: serviceType, taskId },
            });
            errorHandler("Таймаут операции");
          }
        } catch (error) {
          clearInterval(intervalId);
          dispatch({ type: "STOP_TASK", payload: { taskId } });
          dispatch({
            type: "REMOVE_TYPING_INDICATOR",
            payload: { service: serviceType, taskId },
          });
          errorHandler(`Ошибка: ${error.message}`);
        }
      }, 1000);

      dispatch({
        type: "START_TASK",
        payload: { taskId, service: serviceType, intervalId },
      });
    },
    []
  );

  // Очистка при размонтировании приложения
  useEffect(() => {
    return () => {
      state.tasks.forEach((task, taskId) => {
        clearInterval(task.intervalId);
      });
    };
  }, []);

  //формируем объект значения контекста
  const value = {
    ...state, //распространяем текущее состояние
    //методы для изменения состояния
    selectService: (serviceId) =>
      dispatch({ type: "SELECT_SERVICE", payload: serviceId }),
    sendMessage: (message) =>
      dispatch({ type: "SEND_MESSAGE", payload: message }),
    deleteChat: (serviceId) =>
      dispatch({ type: "DELETE_CHAT", payload: serviceId }),
    loadServerChats: (serverData) =>
      dispatch({ type: "LOAD_SERVER_CHATS", payload: serverData }),
    startGlobalTask,
  };

  //возвращаем провайдер с передачей контекста
  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

//свой собственный хук для доступа к контексту
export const useChat = () => {
  const context = React.useContext(ChatContext);
  //защита от использования вне провайдера
  if (!context) {
    throw new Error("useChat must be used within ChatProvider!");
  }
  return context;
};

//Основные концепции:
//1. Context API - механизм React для глобального управления состоянием
//2. Reducer - функция для централизованного управления изменениями состояния
//3. Actions - объекты {type, payload} для описания изменений
//4. Provider - компонент-обертка для доступа к контексту
//5. useEffect - хуки для работы с сайд-эффектами (localStorage)
//6. Структура состояния:
//    chats - объект с историей сообщений для каждого сервиса
//    activeService - идентификатор текущего выбранного сервиса

//Принцип работы:
//1. Все компоненты получают доступ к состоянию через useChat()
//2. Изменения состояния происходят только через dispatch(action)
//3. При любом изменении chats автоматически сохраняется в localStorage
//4. Состояние сохраняется между перезагрузками страницы благодаря localStorage
