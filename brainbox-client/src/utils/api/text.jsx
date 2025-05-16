import axios from "axios";

const GATEWAY_URL = "http://localhost:8000/text";

axios.defaults.withCredentials = true;

export const generateAnswer = async (text) => {
  try {
    const response = await axios.post(`${GATEWAY_URL}/generate-answer`, {
      text: text,
    });
    return response.data;
  } catch (error) {
    console.error(
      "Generate answer error: ",
      error.response?.data || error.message
    );
    throw error;
  }
};

export const getTextMessages = async () => {
  try {
    const response = await axios.get(`${GATEWAY_URL}/get-text-messages`, {
      withCredentials: true,
      headers: {
        "Content-Type": "application/json",
      },
    });
    return {
      messages: response.data.messages.map((msg) => ({
        ...msg,
        table: "text_chat",
      })),
    };
  } catch (error) {
    console.error(
      "Get text messages error: ",
      error.response?.data || error.message
    );
    throw error;
  }
};

export const deleteTextMessages = async () => {
  try {
    const response = await axios.delete(`${GATEWAY_URL}/delete-text-messages`, {
      withCredentials: true,
      headers: {
        "Content-Type": "application/json",
      },
    });
    return response.data;
  } catch (error) {
    console.error(
      "Delete text message error: ",
      error.response?.data || error.message
    );
    throw error;
  }
};
