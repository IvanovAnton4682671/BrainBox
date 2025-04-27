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
