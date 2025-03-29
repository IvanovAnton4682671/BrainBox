import React from "react";
import Login from "./components/Login/Login";
import Home from "./components/Home/Home";
import { ChatProvider } from "./utils/ChatContext";

function App() {
  //состояние аутентификации: true = пользователь вошёл в систему
  const [isAuthenticated, setIsAuthenticated] = React.useState(false);

  //обработчик изменения статуса аутентификации
  const handleAuthentication = (isAuth) => {
    setIsAuthenticated(isAuth);
  };

  return (
    <div>
      {isAuthenticated ? (
        /*обёртка ChatProvider для авторизованных пользователей*/
        <ChatProvider>
          {/*
             ChatProvider делает состояние чатов доступным для всех компонентов внутри
             handleAuthentication передаётся для реализации выхода из системы
          */}
          <Home handleAuthentication={handleAuthentication} />
        </ChatProvider>
      ) : (
        /*компонент авторизации для неавторизованных пользователей*/
        <Login handleAuthentication={handleAuthentication} />
      )}
    </div>
  );
}

export default App;
