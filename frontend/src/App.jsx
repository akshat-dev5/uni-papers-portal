import React, { useState, useCallback, useEffect } from 'react';
import { BookOpen } from 'lucide-react';
import { io } from 'socket.io-client';
import FilterSection from './components/FilterSection';
import PapersTable from './components/PapersTable';
import AiProgressModal from './components/AiProgressModal';
import { getPapers } from './services/api';

// Initialize socket outside component to prevent multiple instances
const socket = io('http://localhost:5000', { autoConnect: false });

function App() {
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);

  // Modal & AI States
  const [isAiModalOpen, setIsAiModalOpen] = useState(false);
  const [aiLogs, setAiLogs] = useState([]);
  const [aiStep, setAiStep] = useState('');

  // Connect socket when app loads
  useEffect(() => {
    socket.connect();
    return () => {
      socket.disconnect();
    };
  }, []);

  const handleFilterChange = useCallback(async (filters) => {
    setLoading(true);
    try {
      const response = await getPapers(filters);
      setPapers(response.data);
    } catch (error) {
      console.error("Error fetching papers:", error);
      setPapers([]); 
    } finally {
      setLoading(false);
    }
  }, []);

  const handleGenerateSolution = async (pdfUrl) => {
    setIsAiModalOpen(true);
    setAiLogs(["Initiating connection to AI server..."]);
    setAiStep("Starting Pipeline");

    try {
      // 1. Call Backend to start generation
      const response = await fetch('http://localhost:5000/api/solution/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pdfUrl })
      });
      const data = await response.json();
      const solutionId = data.solutionId;

      // 2. Join the specific Socket Room for this task
      socket.emit('join-solution-room', solutionId);

      // 3. Listen for Real-Time Logs
      socket.on('pipeline-log', (data) => {
        setAiLogs(prev => [...prev, data.log]);
        // Update bottom step text (truncate if too long)
        setAiStep(data.log.length > 40 ? data.log.substring(0, 40) + "..." : data.log);
      });

      // 4. Listen for Success
      socket.on('pipeline-complete', (data) => {
        setAiLogs(prev => [
          ...prev, 
          "✅ Verification Complete!", 
          "Triggering document download..."
        ]);
        setAiStep("Download Complete!");

        // Trigger file download
        window.location.href = `http://localhost:5000/api/solution/download/${solutionId}`;

        // Cleanup and close modal after 3 seconds
        setTimeout(() => {
          setIsAiModalOpen(false);
          setAiLogs([]);
          socket.off('pipeline-log');
          socket.off('pipeline-complete');
          socket.off('pipeline-error');
        }, 3000);
      });

      // 5. Listen for Errors
      socket.on('pipeline-error', (data) => {
        setAiLogs(prev => [...prev, `❌ ERROR: Process failed with code ${data.code}`]);
        setAiStep("Failed");
      });

    } catch (error) {
      setAiLogs(prev => [...prev, "ERROR: Failed to connect to AI server."]);
      setAiStep("Failed");
    }
  };

  const handleCloseModal = () => {
    setIsAiModalOpen(false);
    setAiLogs([]);
    // Remove listeners if user forces close
    socket.off('pipeline-log');
    socket.off('pipeline-complete');
    socket.off('pipeline-error');
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 font-sans">
      <header className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center gap-3">
          <BookOpen className="text-blue-600 w-6 h-6" />
          <h1 className="text-xl font-semibold text-slate-900 tracking-tight">
            ABVV Question Papers Database
          </h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-6">
          <p className="text-slate-500 mb-6">
            Complete master index of Atal Bihari Vajpayee Vishwavidyalaya (ABVV), Bilaspur, Chhattisgarh previous year question papers. Use filters below to refine your search.
          </p>
          
          <FilterSection 
            onFilterChange={handleFilterChange} 
            totalCount={papers.length} 
            loading={loading}
          />

          <div className="mt-6">
            <PapersTable 
              papers={papers} 
              loading={loading} 
              onGenerateSolution={handleGenerateSolution} 
            />
          </div>
        </div>
      </main>

      <AiProgressModal 
        isOpen={isAiModalOpen} 
        onClose={handleCloseModal} 
        logs={aiLogs} 
        currentStep={aiStep} 
      />
    </div>
  );
}

export default App;