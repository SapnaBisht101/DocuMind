import React, { useState } from 'react';
import { LayoutTemplate, Loader, ArrowRight, CheckCircle2, Lightbulb } from 'lucide-react';
import { storyboardService } from '../services/api';

export default function StoryboardTab({ documentId }) {
  const [mode, setMode] = useState('software');
  const [storyboard, setStoryboard] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await storyboardService.generate(documentId, mode);
      setStoryboard(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
      <div className="flex flex-wrap justify-between items-center mb-6 gap-4">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <LayoutTemplate size={20} className="text-emerald-500" /> AI Storyboard Generator
        </h3>
        <div className="flex items-center gap-2">
          <select 
            value={mode} 
            onChange={(e) => setMode(e.target.value)}
            className="border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-emerald-500"
          >
            <option value="software">Software Workflow</option>
            <option value="business">Business Process</option>
            <option value="research">Research Plan</option>
            <option value="presentation">Presentation Slides</option>
          </select>
          <button 
            onClick={handleGenerate} 
            disabled={loading}
            className="bg-emerald-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-emerald-700 disabled:opacity-50 flex items-center gap-2"
          >
            {loading ? <Loader className="animate-spin" size={16} /> : 'Generate Plan'}
          </button>
        </div>
      </div>

      {storyboard && (
        <div className="space-y-6">
          <div className="bg-emerald-50 p-4 rounded-lg border border-emerald-100">
            <h4 className="text-xl font-bold text-emerald-900">{storyboard.title}</h4>
            <p className="text-sm text-emerald-700 mt-2">{storyboard.project_overview}</p>
          </div>

          <div className="relative border-l-2 border-emerald-200 ml-3 space-y-8 pb-4">
            {storyboard.steps?.map((step, idx) => (
              <div key={idx} className="relative pl-6">
                <span className="absolute -left-[17px] top-1 bg-white border-2 border-emerald-500 text-emerald-600 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold">
                  {step.step_number}
                </span>
                <div className="bg-white border border-gray-200 p-4 rounded-lg shadow-sm">
                  <div className="flex justify-between items-start">
                    <h5 className="font-bold text-gray-800 text-lg">{step.title}</h5>
                    {step.is_explicit_requirement ? (
                      <span className="flex items-center gap-1 text-xs text-blue-600 bg-blue-50 px-2 py-1 rounded border border-blue-100"><CheckCircle2 size={12}/> In Document</span>
                    ) : (
                      <span className="flex items-center gap-1 text-xs text-amber-600 bg-amber-50 px-2 py-1 rounded border border-amber-100"><Lightbulb size={12}/> AI Suggestion</span>
                    )}
                  </div>
                  <p className="text-sm text-gray-600 mt-1 mb-3">{step.purpose}</p>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm bg-gray-50 p-3 rounded">
                    <div><span className="font-semibold text-gray-700">Actor/Role:</span> {step.actor_or_role}</div>
                    <div><span className="font-semibold text-gray-700">Inputs:</span> {step.inputs.join(', ')}</div>
                    <div className="col-span-2"><span className="font-semibold text-gray-700">Logic:</span> {step.processing_logic}</div>
                    <div className="col-span-2 flex items-center gap-2 text-emerald-700 font-medium"><ArrowRight size={14}/> {step.expected_output}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      {!storyboard && !loading && <p className="text-gray-500 text-sm text-center py-8">Select a mode and generate a structured step-by-step plan based on your document.</p>}
    </div>
  );
}