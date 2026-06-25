import React, { useState, useCallback, useEffect } from 'react';
import { BookOpen } from 'lucide-react';
import { io } from 'socket.io-client';
import FilterSection from './components/FilterSection';
import PapersTable from './components/PapersTable';
import AiProgressModal from './components/AiProgressModal';
import { getPapers } from './services/api';

const socket = io('http://localhost:5000', { autoConnect: false });

function App() {
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);

  // Modal & AI States
  const [isAiModalOpen, setIsAiModalOpen] = useState(false);
  const [aiLogs, setAiLogs] = useState([]);
  const [aiStep, setAiStep] = useState('');
  const [modalType, setModalType] = useState('solution'); // NEW: Tracks which flow is running

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

  // ----------------------------------------------------
  // FLOW 1: AI SOLUTION GENERATION
  // ----------------------------------------------------
  const handleGenerateSolution = async (pdfUrl) => {
    setModalType('solution'); // Set modal type
    setIsAiModalOpen(true);
    setAiLogs(["Initiating connection..."]);
    setAiStep("Starting Pipeline");

    try {
      const response = await fetch('http://localhost:5000/api/solution/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pdfUrl })
      });
      const data = await response.json();
      const solutionId = data.solutionId;

      socket.emit('join-solution-room', solutionId);

      socket.on('pipeline-log', (data) => {
        setAiLogs(prev => [...prev, data.log]);
        setAiStep(data.log.length > 40 ? data.log.substring(0, 40) + "..." : data.log);
      });

      socket.on('pipeline-complete', (data) => {
        setAiLogs(prev => [...prev, "✅ Verification Complete!", "Successfully finished"]);
        setAiStep("Download Complete!");
        
        // Force Download Hack
        window.location.href = `http://localhost:5000/api/solution/download/${solutionId}`;
        
        setTimeout(() => handleCloseModal(), 3000);
      });

      socket.on('pipeline-error', (data) => {
        setAiLogs(prev => [...prev, `❌ ERROR: Process failed with code ${data.code}`]);
        setAiStep("Failed");
      });

    } catch (error) {
      setAiLogs(prev => [...prev, "ERROR: Failed to connect to AI server."]);
      setAiStep("Failed");
    }
  };

  // ----------------------------------------------------
  // FLOW 2: WATERMARK REMOVAL 
  // ----------------------------------------------------
// FLOW 2: WATERMARK REMOVAL (BULLETPROOF DOWNLOAD)
  // ----------------------------------------------------
  const handleCleanWatermark = async (pdfUrl) => {
    setModalType('watermark');
    setIsAiModalOpen(true);
    setAiLogs([]);
    setAiStep("Starting Watermark Pipeline");

    // Simulated logs for UI engagement
    const simulatedLogs = [
      "Initiating connection...",
      "Downloading PDF...",
      "Watermark_Init",
      "Watermark_Detect",
      "Watermark_Restore"
    ];

    let currentLogIndex = 0;
    const logInterval = setInterval(() => {
      if (currentLogIndex < simulatedLogs.length) {
        setAiLogs(prev => [...prev, simulatedLogs[currentLogIndex]]);
        currentLogIndex++;
      }
    }, 8000); 

    try {
      const response = await fetch('http://localhost:5000/api/watermark/remove', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pdfUrl })
      });
      
      const data = await response.json();
      clearInterval(logInterval);
      
      if (data.status === "success" && data.downloadUrl) {
        setAiLogs(prev => [...prev, "Watermark_Complete", "Successfully finished"]);
        setAiStep("Download Complete!");
        
        // --- BULLETPROOF BLOB DOWNLOAD FIX ---
        const fileUrl = `http://localhost:5000${data.downloadUrl}`;
        const fileResponse = await fetch(fileUrl);
        const blob = await fileResponse.blob(); // Convert to binary data
        const blobUrl = window.URL.createObjectURL(blob); // Create browser-safe URL
        
        const a = document.createElement('a');
        a.href = blobUrl;
        a.download = 'Cleaned_Question_Paper.pdf'; // Name of file
        document.body.appendChild(a);
        a.click(); // Trigger click
        document.body.removeChild(a); // Cleanup
        window.URL.revokeObjectURL(blobUrl);
        // --------------------------------------
        
        setTimeout(() => handleCloseModal(), 2000);
      } else {
        setAiLogs(prev => [...prev, "❌ ERROR: Document cleanup failed."]);
        setAiStep("Failed");
      }
    } catch (error) {
      clearInterval(logInterval);
      setAiLogs(prev => [...prev, "❌ ERROR: Failed to connect to Server."]);
      setAiStep("Failed");
    }
  };

  const handleCloseModal = () => {
    setIsAiModalOpen(false);
    setAiLogs([]);
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
              onCleanWatermark={handleCleanWatermark} 
            />
          </div>
        </div>
      </main>

      <AiProgressModal 
        isOpen={isAiModalOpen} 
        onClose={handleCloseModal} 
        logs={aiLogs} 
        currentStep={aiStep}
        modalType={modalType} // Passing the type explicitly
      />
    </div>
  );
}

export default App;