import axios from "axios";

const GATEWAY_URL_AUTH = window.appConfig.GATEWAY_URL_AUTH;

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
    const response = await axios.post(`${GATEWAY_URL_AUTH}/register`, {
      email: email,
      name: name,
      password: password,
    });
    console.log(
      `Выполнился запрос с данными ${email}, ${name}, ${password} на адрес ${GATEWAY_URL_AUTH}/register`
    );
    return response.data;
  } catch (error) {
    console.log(`Ошибка при регистрации: ${error}`);
    return handleError(error);
  }
};

export const userLogin = async (email, password) => {
  try {
    const response = await axios.post(`${GATEWAY_URL_AUTH}/login`, {
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
    const response = await axios.get(`${GATEWAY_URL_AUTH}/check-session`);
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};

export const userLogout = async () => {
  try {
    const response = await axios.post(`${GATEWAY_URL_AUTH}/logout`);
    return response.data;
  } catch (error) {
    return handleError(error);
  }
};
