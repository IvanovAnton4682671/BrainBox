import React from "react";

//создание контекста для управления состоянием чатов
const ChatContext = React.createContext();

//начальное состояние чатов для всех сервисов
const initialChats = {
  speechToText: [],
  imageGeneration: [],
  chatBot: [],
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
          [state.activeService]: [
            ...state.chats[state.activeService], //существующие сообщения
            action.payload, //новое сообщение
          ],
        },
      };
    case "DELETE_CHAT":
      //очистка чата: заменяем массив сообщений сервиса пустым
      return { ...state, chats: { ...state.chats, [action.payload]: [] } };
    case "LOAD_CHATS":
      //загрузка чатов: заменяем текущие чаты сохраненными данными
      return { ...state, chats: action.payload };
    default:
      return state;
  }
};

//провайдер контекста (основной компонент)
export const ChatProvider = ({ children }) => {
  //используем useReducer для управления сложным состоянием
  const [state, dispatch] = React.useReducer(chatReducer, {
    chats: initialChats, //начальное состояние чатов
    activeService: null, //изначально ни один сервис не выбран
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
