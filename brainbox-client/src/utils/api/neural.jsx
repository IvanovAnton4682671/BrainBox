import axios from "axios";

const GATEWAY_URL = "http://localhost:8000/neural";

export const recognizeAudio = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  try {
    const response = await axios.post(
      `${GATEWAY_URL}/recognize-audio`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Audio recognition error: ", error);
    throw error;
  }
};

export const getAudioMessages = async () => {
  try {
    const response = await axios.get(`${GATEWAY_URL}/get-audio-messages`, {
      withCredentials: true,
      headers: {
        "Content-Type": "application/json",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error getting audio messages: ", error);
    throw error;
  }
};
