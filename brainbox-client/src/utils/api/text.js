import axios from "axios";

const GATEWAY_URL_TEXT = window.appConfig.GATEWAY_URL_TEXT;

axios.defaults.withCredentials = true;

export const generateAnswer = async (text) => {
  try {
    const response = await axios.post(`${GATEWAY_URL_TEXT}/generate-answer`, {
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

export const checkTaskStatus = async (task_id) => {
  try {
    const response = await axios.get(`${GATEWAY_URL_TEXT}/tasks/${task_id}`);
    return response.data;
  } catch (error) {
    console.error("Check task status error: ", error);
    throw error;
  }
};

export const getTextMessages = async () => {
  try {
    const response = await axios.get(`${GATEWAY_URL_TEXT}/get-text-messages`, {
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
    const response = await axios.delete(
      `${GATEWAY_URL_TEXT}/delete-text-messages`,
      {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error(
      "Delete text message error: ",
      error.response?.data || error.message
    );
    throw error;
  }
};
