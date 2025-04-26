import axios from "axios";

const GATEWAY_URL = "http://localhost:8000/auth";

//настройка для автоматической отправки кук
axios.defaults.withCredentials = true;

const handleError = (error) => {
  console.error(error);
  if (error.response?.data?.detail?.error) {
    return {
      success: error.response.data.detail.success,
      error: error.response.data.detail.error,
    };
  }
  return {
    success: false,
    error: {
      code: error.code || "network_error",
      message: error.message || "Ошибка сети!",
    },
  };
};

export const userRegister = async (email, name, password) => {
  try {
    const response = await axios.post(`${GATEWAY_URL}/register`, {
      email: email,
      name: name,
      password: password,
    });
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

export const userLogin = async (email, password) => {
  try {
    const response = await axios.post(`${GATEWAY_URL}/login`, {
      email: email,
      password: password,
    });
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

export const checkSession = async () => {
  try {
    const response = await axios.get(`${GATEWAY_URL}/check-session`);
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

export const userLogout = async () => {
  try {
    const response = await axios.post(`${GATEWAY_URL}/logout`);
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};
