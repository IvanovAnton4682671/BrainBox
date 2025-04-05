import axios from "axios";
const AUTH_URL = "http://localhost:8001/auth";

export const userRegister = async (email, name, password) => {
  try {
    const response = await axios.post(`${AUTH_URL}/register`, {
      email: email,
      name: name,
      password: password,
    });
    return response.data;
  } catch (error) {
    if (error.response?.data?.detail) {
      return error.response.data.detail;
    }
    return {
      success: false,
      error: {
        code: "network_error",
        message: "Ошибка сети!",
      },
    };
  }
};

export const userLogin = async (email, password) => {
  try {
    const response = await axios.post(`${AUTH_URL}/login`, {
      email: email,
      password: password,
    });
    return response.data;
  } catch (error) {
    if (error.response?.data?.detail) {
      return error.response.data.detail;
    }
    return {
      success: false,
      error: {
        code: "network_error",
        message: "Ошибка сети!",
      },
    };
  }
};
