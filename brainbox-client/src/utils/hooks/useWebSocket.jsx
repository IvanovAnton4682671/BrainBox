import { useEffect, useRef } from "react";
import { useWebSocketContext } from "../stateManager/wsContext";

export function useWebSocket() {
  const { addMessageHandler } = useWebSocketContext();
  const wsRef = useRef(null);

  useEffect(() => {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/ws`;

    const connectWebSocket = () => {
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        console.log("WebSocket connected");
        // Отправляем периодические пинги
        const pingInterval = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send("ping");
          } else {
            clearInterval(pingInterval);
          }
        }, 30000);
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          //вызываем все обработчики
          handlers.current.forEach((handler) => handler(message));
        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
        }
      };

      ws.onclose = (event) => {
        console.log(`WebSocket closed: ${event.code} ${event.reason}`);
        // Переподключение с экспоненциальной задержкой
        setTimeout(connectWebSocket, 3000);
      };

      ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        ws.close();
      };

      wsRef.current = ws;
    };

    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return { addMessageHandler };
}
