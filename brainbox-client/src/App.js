import React from "react";
import Login from "./components/LoginPage/Login/Login";
import Home from "./components/HomePage/Home/Home";
import { ChatProvider } from "./utils/stateManager/chatContext";
import { useAuth } from "./utils/hooks/useAuth";
import { AuthProvider } from "./utils/stateManager/authContext";

function AppContent() {
  const { isAuthenticated, isSessionChecked, logout } = useAuth();

  if (!isSessionChecked) {
    return <div>Проверка сессии...</div>;
  }

  return (
    <div>
      {isAuthenticated ? (
        /*обёртка ChatProvider для авторизованных пользователей*/
        <ChatProvider>
          {/*
             ChatProvider делает состояние чатов доступным для всех компонентов внутри
             handleLogout передаётся для реализации выхода из системы
          */}
          <Home handleLogout={logout}></Home>
        </ChatProvider>
      ) : (
        /*компонент авторизации для неавторизованных пользователей*/
        <Login />
      )}
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
