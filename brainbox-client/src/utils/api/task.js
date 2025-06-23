import axios from "axios";

const SPEECH_TO_TEXT = window.appConfig.GATEWAY_URL_AUDIO;
const IMAGE_GENERATION = window.appConfig.GATEWAY_URL_IMAGE;
const CHAT_BOT = window.appConfig.GATEWAY_URL_TEXT;

export const checkTaskStatus = async (task_id, taskType) => {
  const baseUrl =
    taskType === "speechToText"
      ? SPEECH_TO_TEXT
      : taskType === "imageGeneration"
      ? IMAGE_GENERATION
      : CHAT_BOT;

  try {
    const response = await axios.get(`${baseUrl}/tasks/${task_id}`);
    return response.data;
  } catch (error) {
    console.error("Check task status error: ", error);
    throw error;
  }
};
