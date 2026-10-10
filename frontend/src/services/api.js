import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export const documentService = {
  uploadFile: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  extractData: (documentId) => {
    return api.post(`/documents/${documentId}/extract`);
  }
};

export const chatService = {
  askQuestion: (documentId, query) => {
    return api.post('/chat/query', { document_id: documentId, query });
  }
};

export const storyboardService = {
  generate: (documentId, mode) => {
    return api.post('/storyboards/generate', { document_id: documentId, mode });
  }
};

export default api;