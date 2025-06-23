import axios from "axios";

const GATEWAY_URL_IMAGE = window.appConfig.GATEWAY_URL_IMAGE;

axios.defaults.withCredentials = true;

export const generateAnswer = async (text) => {
  try {
    const response = await axios.post(`${GATEWAY_URL_IMAGE}/generate-answer`, {
      text: text,
    });
    return response.data;
  } catch (error) {
    console.error("Generate answer error: ", error);
    throw error;
  }
};

export const checkTaskStatus = async (task_id) => {
  try {
    const response = await axios.get(`${GATEWAY_URL_IMAGE}/tasks/${task_id}`);
    return response.data;
  } catch (error) {
    console.error("Check task status error: ", error);
    throw error;
  }
};

export const viewImage = async (image_uid) => {
  try {
    const response = await axios.get(`${GATEWAY_URL_IMAGE}/view/${image_uid}`, {
      responseType: "blob",
      withCredentials: true,
    });
    return URL.createObjectURL(response.data);
  } catch (error) {
    console.error("View image error: ", error);
  }
};

export const downloadImage = async (image_uid) => {
  try {
    const response = await axios.get(
      `${GATEWAY_URL_IMAGE}/download/${image_uid}`,
      {
        responseType: "blob",
        withCredentials: true,
      }
    );
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `image_${image_uid}.jpg`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Download image error: ", error);
    throw error;
  }
};

export const getImageMessages = async () => {
  try {
    const response = await axios.get(
      `${GATEWAY_URL_IMAGE}/get-image-messages`,
      {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return {
      messages: response.data.messages.map((msg) => ({
        ...msg,
        table: "image_chat",
      })),
    };
  } catch (error) {
    console.error("Get image messages error: ", error);
    throw error;
  }
};

export const deleteImageMessages = async () => {
  try {
    const response = await axios.delete(
      `${GATEWAY_URL_IMAGE}/delete-image-messages`,
      {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Delete image messages error: ", error);
  }
};
