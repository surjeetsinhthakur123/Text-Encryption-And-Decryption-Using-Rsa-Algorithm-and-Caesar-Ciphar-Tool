import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service functions
export const pycryptAPI = {
  // Health check
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/health');
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  // Encrypt text
  encryptText: async (text, password, hint = '') => {
    try {
      const response = await apiClient.post('/encrypt/text', {
        text,
        password,
        hint: hint || undefined
      });
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage = error.response?.data?.error || error.message;
      return { success: false, error: errorMessage };
    }
  },

  // Decrypt text
  decryptText: async (encryptedContent, password) => {
    try {
      const response = await apiClient.post('/decrypt/text', {
        encrypted_content: encryptedContent,
        password
      });
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage = error.response?.data?.error || error.message;
      return { success: false, error: errorMessage };
    }
  }
};

export default pycryptAPI; 