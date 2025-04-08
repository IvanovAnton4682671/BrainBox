import React from "react";
import axios from "axios";
import { userRegister, userLogin } from "../api/auth";
import { useAuthContext } from "../stateManager/authContext";

const AUTH_URL = "http://localhost:8001/auth";

export const useAuth = () => {
  const { isAuthenticated, setIsAuthenticated, userName, setUserName } =
    useAuthContext();

  const [isSessionChecked, setIsSessionChecked] = React.useState(false);

  const checkSession = React.useCallback(async () => {
    console.log("Проверка сессии...");
    try {
      const response = await axios.get(`${AUTH_URL}/check-session`, {
        withCredentials: true,
        timeout: 5000,
      });
      console.log("Результат проверки сессии: ", response.data);
      setIsAuthenticated(response.data.success);
      if (response.data.user_name) {
        setUserName(response.data.user_name);
      }
    } catch (error) {
      console.error("Ошибка при проверки сессии: ", error);
      setIsAuthenticated(false);
      setUserName("");
    } finally {
      setIsSessionChecked(true);
    }
  }, [setIsAuthenticated, setUserName]);

  //проверка сессии при монтировании
  React.useEffect(() => {
    checkSession();
  }, [checkSession]);

  const register = async (email, name, password) => {
    const result = await userRegister(email, name, password);
    if (result.success) {
      await checkSession(); //проверяем сессию после успешной регистрации
    }
    return result;
  };

  const login = async (email, password) => {
    const result = await userLogin(email, password);
    if (result.success) {
      await checkSession(); //проверяем сессию после успешной авторизации
    }
    return result;
  };

  const logout = async () => {
    try {
      const response = await axios.post(
        `${AUTH_URL}/logout`,
        {},
        {
          withCredentials: true,
        }
      );
      if (response.data.success) {
        setIsAuthenticated(false);
        setUserName("");
        document.cookie =
          "sessionid=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
        return true;
      }
      return false;
    } catch (error) {
      console.error("Ошибка при выходе из системы: ", error);
      return false;
    }
  };

  return {
    isAuthenticated,
    userName,
    isSessionChecked,
    register,
    login,
    logout,
  };
};
