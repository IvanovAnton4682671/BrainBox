import React from "react";

const WebSocketContext = React.createContext({
  addMessageHandler: () => {},
  isConnected: false,
});

export const WebSocketProvider = ({ children }) => {
  const wsRef = React.useRef(null);
  const handlers = React.useRef([]);
  const [isConnected, setIsConnected] = React.useState(false);
  const reconnectAttempts = React.useRef(0);
  const reconnectTimer = React.useRef(null);
  const isMounted = React.useRef(false);

  const connect = React.useCallback(() => {
    if (wsRef.current) {
      try {
        wsRef.current.close();
      } catch (e) {
        console.error("Error closing previous socket:", e);
      }
      wsRef.current = null;
    }

    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsURL = `${protocol}//localhost:8000/ws`;
    const socket = new WebSocket(wsURL);

    socket.onopen = () => {
      console.log("WebSocket connected!");
      setIsConnected(true);
      reconnectAttempts.current = 0;
    };

    socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        handlers.current.forEach((handler) => handler(message));
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    socket.onclose = (event) => {
      console.log(`WebSocket closed: ${event.code} ${event.reason}`);
      setIsConnected(false);
      const delay = Math.min(
        1000 * Math.pow(2, reconnectAttempts.current),
        30000
      );
      reconnectAttempts.current += 1;
      reconnectTimer.current = setTimeout(() => {
        console.log("Attempting to reconnect WebSocket...");
        connect();
      }, delay);
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    wsRef.current = socket;
  }, []);

  React.useEffect(() => {
    if (!isMounted.current) {
      connect();
      isMounted.current = true;
      return () => {
        if (wsRef.current) {
          wsRef.current.close();
        }
        if (reconnectTimer.current) {
          clearTimeout(reconnectTimer.current);
        }
      };
    }
  }, [connect]);

  const addMessageHandler = (handler) => {
    handlers.current.push(handler);
    return () => {
      handlers.current = handlers.current.filter((h) => h !== handler);
    };
  };

  return (
    <WebSocketContext.Provider
      value={{
        addMessageHandler,
        isConnected,
      }}
    >
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocketContext = () => React.useContext(WebSocketContext);
