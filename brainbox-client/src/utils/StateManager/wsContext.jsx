import React from "react";

const WebSocketContext = React.createContext({
  addMessageHandler: () => {},
  connectWebSocket: () => {},
  isConnected: false,
});

export const WebSocketProvider = ({ children }) => {
  const wsRef = React.useRef(null); // Используем ref вместо state
  const handlers = React.useRef([]);
  const reconnectAttempts = React.useRef(0);
  const reconnectTimer = React.useRef(null);
  const [isConnected, setIsConnected] = React.useState(false); // Добавляем состояние подключения

  const addMessageHandler = (handler) => {
    handlers.current.push(handler);
    return () => {
      handlers.current = handlers.current.filter((h) => h !== handler);
    };
  };

  const connectWebSocket = React.useCallback(() => {
    // Используем useCallback
    // Закрываем существующее соединение если есть
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.close();
    }

    // Устанавливаем URL для WebSocket
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsURL = `${protocol}//localhost:8000/ws`;
    const socket = new WebSocket(wsURL);

    socket.onopen = () => {
      console.log("WebSocket connected!");
      setIsConnected(true);
      reconnectAttempts.current = 0;
    };

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      try {
        handlers.current.forEach((handler) => handler(message));
      } catch (error) {
        console.error(`Error parsing WebSocket message = ${message}: ${error}`);
      }
    };

    socket.onclose = (event) => {
      console.log(`WebSocket closed: ${event.code} ${event.reason}`);
      setIsConnected(false);

      // Экспоненциальная задержка для переподключения
      const delay = Math.min(
        1000 * Math.pow(2, reconnectAttempts.current),
        30000
      );
      reconnectAttempts.current += 1;

      reconnectTimer.current = setTimeout(() => {
        console.log("Attempt to reconnect WebSocket...");
        connectWebSocket();
      }, delay);
    };

    socket.onerror = (error) => {
      console.error(`WebSocket error: ${error}`);
    };

    wsRef.current = socket;
  }, []);

  // Инициализация соединения при монтировании
  React.useEffect(() => {
    connectWebSocket();

    // Очистка при размонтировании
    return () => {
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.close();
      }
      if (reconnectTimer.current) {
        clearTimeout(reconnectTimer.current);
      }
    };
  }, [connectWebSocket]);

  return (
    <WebSocketContext.Provider
      value={{
        addMessageHandler,
        connectWebSocket,
        isConnected,
      }}
    >
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocketContext = () => React.useContext(WebSocketContext);
