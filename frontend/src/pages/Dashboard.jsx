import React, { useState } from 'react';
import { UploadCloud, CheckCircle, AlertCircle, MessageSquare, Database, LayoutTemplate } from 'lucide-react';
import { documentService } from '../services/api';
import ChatTab from '../components/ChatTab';
import ExtractionTab from '../components/ExtractionTab';
import StoryboardTab from '../components/StoryboardTab';

export default function Dashboard() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('chat'); // chat, extract, storyboard

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0]);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    
    try {
      const response = await documentService.uploadFile(file);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error uploading document');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      {!result ? (
        <div className="bg-white p-12 rounded-lg shadow-sm border border-gray-200 text-center max-w-2xl mx-auto mt-10">
          <UploadCloud className="mx-auto h-16 w-16 text-blue-500 mb-6" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Upload a Document to Begin</h2>
          <p className="text-gray-500 mb-8">DocuMind AI will index your file for semantic search, structured extraction, and automated planning.</p>
          
          <input 
            type="file" 
            accept=".pdf,.txt,.md"
            onChange={handleFileChange}
            className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 mb-6 cursor-pointer"
          />
          
          <button 
            onClick={handleUpload}
            disabled={!file || loading}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors w-full"
          >
            {loading ? 'Processing & Indexing...' : 'Upload & Process Workspace'}
          </button>
          
          {error && <div className="mt-4 text-red-500 flex items-center justify-center gap-2"><AlertCircle size={16} /> {error}</div>}
        </div>
      ) : (
        <div className="space-y-6 mt-4">
          {/* Success Banner */}
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="bg-green-100 p-2 rounded-full text-green-600"><CheckCircle size={20} /></div>
              <div>
                <h3 className="font-semibold text-gray-800">{result.filename}</h3>
                <p className="text-xs text-gray-500">Indexed {result.chunks_indexed} chunks • ID: {result.document_id.slice(0,8)}...</p>
              </div>
            </div>
            <button onClick={() => {setResult(null); setFile(null);}} className="text-sm text-blue-600 hover:underline">
              Upload New File
            </button>
          </div>

          {/* Navigation Tabs */}
          <div className="flex border-b border-gray-200">
            <button 
              onClick={() => setActiveTab('chat')}
              className={`px-6 py-3 font-medium text-sm flex items-center gap-2 border-b-2 transition-colors ${activeTab === 'chat' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'}`}
            >
              <MessageSquare size={16} /> RAG Chat
            </button>
            <button 
              onClick={() => setActiveTab('extract')}
              className={`px-6 py-3 font-medium text-sm flex items-center gap-2 border-b-2 transition-colors ${activeTab === 'extract' ? 'border-purple-600 text-purple-600' : 'border-transparent text-gray-500 hover:text-gray-700'}`}
            >
              <Database size={16} /> Structured Extraction
            </button>
            <button 
              onClick={() => setActiveTab('storyboard')}
              className={`px-6 py-3 font-medium text-sm flex items-center gap-2 border-b-2 transition-colors ${activeTab === 'storyboard' ? 'border-emerald-600 text-emerald-600' : 'border-transparent text-gray-500 hover:text-gray-700'}`}
            >
              <LayoutTemplate size={16} /> Workflow Storyboard
            </button>
          </div>

          {/* Tab Content */}
          <div className="mt-6">
            {activeTab === 'chat' && <ChatTab documentId={result.document_id} />}
            {activeTab === 'extract' && <ExtractionTab documentId={result.document_id} />}
            {activeTab === 'storyboard' && <StoryboardTab documentId={result.document_id} />}
          </div>
        </div>
      )}
    </div>
  );
}