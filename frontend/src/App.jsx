import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        {/* Simple Navbar */}
        <nav className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between shadow-sm">
          <div className="text-xl font-bold text-blue-600 flex items-center gap-2">
            <span className="bg-blue-600 text-white px-2 py-1 rounded">D</span>
            DocuMind AI
          </div>
        </nav>
        
        {/* Main Content */}
        <main className="p-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;