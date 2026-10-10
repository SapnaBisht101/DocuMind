import React, { useState } from 'react';
import { Database, Loader } from 'lucide-react';
import { documentService } from '../services/api';

export default function ExtractionTab({ documentId }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleExtract = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await documentService.extractData(documentId);
      setData(response.data);
    } catch (err) {
        const serverError = err.response?.data?.detail || err.message;
        setError(`Failed to extract data: ${serverError}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <Database size={20} className="text-purple-500" /> Structured Extraction
        </h3>
        <button 
          onClick={handleExtract} 
          disabled={loading}
          className="bg-purple-100 text-purple-700 px-4 py-2 rounded text-sm font-medium hover:bg-purple-200 disabled:opacity-50 flex items-center gap-2"
        >
          {loading ? <Loader className="animate-spin" size={16} /> : 'Run Extraction'}
        </button>
      </div>

      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

      {data && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-50 p-3 rounded border border-gray-200">
              <span className="text-xs text-gray-500 uppercase font-semibold">Document Title</span>
              <p className="font-medium text-gray-800 mt-1">{data.title || "N/A"}</p>
            </div>
            <div className="bg-gray-50 p-3 rounded border border-gray-200">
              <span className="text-xs text-gray-500 uppercase font-semibold">Document Type</span>
              <p className="font-medium text-gray-800 mt-1">{data.document_type || "N/A"}</p>
            </div>
          </div>

          <div className="bg-gray-50 p-3 rounded border border-gray-200">
            <span className="text-xs text-gray-500 uppercase font-semibold">Executive Summary</span>
            <p className="text-sm text-gray-700 mt-1">{data.executive_summary || "No summary available."}</p>
          </div>

          <div className="bg-gray-50 p-3 rounded border border-gray-200">
            <span className="text-xs text-gray-500 uppercase font-semibold">Key Topics</span>
            <div className="flex gap-2 flex-wrap mt-2">
              {data.key_topics?.map((topic, i) => (
                <span key={i} className="bg-purple-100 text-purple-800 text-xs px-2.5 py-1 rounded border border-purple-200">
                  {topic}
                </span>
              ))}
            </div>
          </div>

          <div className="bg-gray-50 p-3 rounded border border-gray-200">
            <span className="text-xs text-gray-500 uppercase font-semibold">Key Entities</span>
            <div className="flex gap-2 flex-wrap mt-2">
              {data.entities?.map((ent, i) => (
                <span key={i} className="bg-blue-100 text-blue-800 text-xs px-2.5 py-1 rounded border border-blue-200">
                  <strong>{ent.name}</strong> ({ent.type})
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {!data && !loading && !error && (
        <p className="text-gray-500 text-sm text-center py-8">
          Click "Run Extraction" to pull structured metadata from this document.
        </p>
      )}
    </div>
  );
}