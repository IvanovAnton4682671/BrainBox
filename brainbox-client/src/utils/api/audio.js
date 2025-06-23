import axios from "axios";

const GATEWAY_URL_AUDIO = window.appConfig.GATEWAY_URL_AUDIO;

//автоматическая отправка кук
axios.defaults.withCredentials = true;

export const uploadAudio = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  try {
    const response = await axios.post(
      `${GATEWAY_URL_AUDIO}/upload-audio`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Upload audio error: ", error);
    throw error;
  }
};

export const recognizeSavedAudio = async (audio_uid) => {
  try {
    const response = await axios.post(
      `${GATEWAY_URL_AUDIO}/recognize-saved-audio`,
      {
        audio_uid: audio_uid,
      }
    );
    return response.data;
  } catch (error) {
    console.error(
      "Recognize saved audio error: ",
      error.response?.data || error.message
    );
    throw error;
  }
};

export const checkTaskStatus = async (task_id) => {
  try {
    const response = await axios.get(`${GATEWAY_URL_AUDIO}/tasks/${task_id}`);
    return response.data;
  } catch (error) {
    console.error("Check task status error: ", error);
    throw error;
  }
};

export const getAudioMessages = async () => {
  try {
    console.log("Отправляем запрос на аудио-сообщения");
    const response = await axios.get(
      `${GATEWAY_URL_AUDIO}/get-audio-messages`,
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
        table: "audio_chat",
      })),
    };
  } catch (error) {
    console.error("Get audio messages error: ", error);
    throw error;
  }
};

export const downloadAudio = async (audio_uid) => {
  try {
    const response = await axios.get(
      `${GATEWAY_URL_AUDIO}/download-audio/${audio_uid}`,
      {
        responseType: "blob",
        withCredentials: true,
      }
    );
    //создание временной ссылки на скачивание
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `audio_${audio_uid}.mp3`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Download audio error: ", error);
    throw error;
  }
};

export const deleteAudioMessages = async () => {
  try {
    const response = await axios.delete(
      `${GATEWAY_URL_AUDIO}/delete-audio-messages`,
      {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Delete audio messages error: ", error);
    throw error;
  }
};
