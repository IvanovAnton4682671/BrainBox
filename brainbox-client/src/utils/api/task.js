import axios from "axios";

export const checkTaskStatus = async (task_id, taskType) => {
  const baseUrl =
    taskType === "speechToText"
      ? "http://localhost:8000/audio"
      : taskType === "imageGeneration"
      ? "http://localhost:8000/image"
      : "http://localhost:8000/text";

  try {
    const response = await axios.get(`${baseUrl}/tasks/${task_id}`);
    return response.data;
  } catch (error) {
    console.error("Check task status error: ", error);
    throw error;
  }
};
