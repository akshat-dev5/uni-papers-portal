import React, { useEffect, useRef } from 'react';
import { X, CheckCircle2, Loader2, Sparkles, BrainCircuit } from 'lucide-react';
import SoftAurora from './background/SoftAurora';

// NEW: Added modalType prop
const AiProgressModal = ({ isOpen, onClose, logs, modalType }) => {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  if (!isOpen) return null;

  // NEW: Clean logic for identifying flow
  const isWatermarkFlow = modalType === 'watermark';
  const modalTitle = isWatermarkFlow ? "AI Watermark Remover" : "AI Solution Generator";

  const translateLog = (rawLog) => {
    if (!rawLog) return null;
    
    if (rawLog.includes("Initiating connection")) return "Waking up AI agents & establishing secure connection...";
    if (rawLog.includes("Downloading PDF")) return "Fetching the document securely...";
    
    if (rawLog.includes("Watermark_Init")) return "Initializing Watermark Removal Engine...";
    if (rawLog.includes("Watermark_Detect")) return "AI Vision is scanning and isolating watermarks...";
    if (rawLog.includes("Watermark_Restore")) return "Restoring document clarity and removing artifacts...";
    if (rawLog.includes("Watermark_Complete")) return "Final clean document reconstructed successfully!";
    
    if (rawLog.includes("Converting PDF to images")) return "Preparing document for AI vision analysis...";
    if (rawLog.includes("Extracting page")) {
      const match = rawLog.match(/page (\d+)\/(\d+)/);
      return match ? `AI Vision is scanning page ${match[1]} of ${match[2]}...` : "Scanning pages...";
    }
    if (rawLog.includes("Starting 3-Agent")) return "Document scanned. Initiating Intelligence Pipeline...";
    if (rawLog.includes("Orchestrator selected model")) return "Selecting the most advanced AI brain for this subject...";
    if (rawLog.includes("Answering Sub-part") || rawLog.includes("Answering (")) return "Student Agent is actively researching and drafting an answer...";
    if (rawLog.includes("Professor Review")) {
      if (rawLog.includes("Approved: True")) return "Professor Agent verified the answer. Quality check passed! ✅";
      if (rawLog.includes("Approved: False")) return "Professor Agent found flaws. Sending back for revision... ⚠️";
      return "Professor Agent is rigorously verifying accuracy...";
    }
    if (rawLog.includes("Revision needed")) return "Student Agent is improving the answer based on feedback...";
    if (rawLog.includes("Answer generation complete")) return "All questions successfully answered and verified!";
    if (rawLog.includes("Converting Markdown to Word")) return "Formatting all verified answers into a Word document...";
    if (rawLog.includes("Word document saved")) return "Final document generated successfully!";
    
    if (rawLog.includes("Successfully finished")) return "Process complete! Preparing your download...";
    if (rawLog.includes("ERROR") || rawLog.includes("Traceback") || rawLog.includes("failed")) return "We encountered a slight issue. Retrying...";

    return null; 
  };

  const calculateProgress = () => {
    const text = logs.join(" ");
    
    if (isWatermarkFlow) {
      if (text.includes("Successfully finished")) return 100;
      if (text.includes("Watermark_Complete")) return 90;
      if (text.includes("Watermark_Restore")) return 70;
      if (text.includes("Watermark_Detect")) return 40;
      if (text.includes("Watermark_Init")) return 20;
      if (text.includes("Downloading PDF")) return 10;
      return 5;
    }

    if (text.includes("Successfully finished")) return 100;
    if (text.includes("Converting Markdown")) return 95;
    if (text.includes("Answer generation complete")) return 90;
    
    const approvedCount = (text.match(/Approved: True/g) || []).length;
    if (approvedCount > 0) return Math.min(40 + (approvedCount * 4), 85);
    
    if (text.includes("Starting 3-Agent")) return 35;
    if (text.includes("Extracting page")) return 20;
    if (text.includes("Downloading PDF")) return 10;
    return 5; 
  };

  const userFriendlyLogs = logs.map(translateLog).filter(log => log !== null);
  const currentProgress = calculateProgress();

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
      <div className="relative w-full max-w-2xl bg-white rounded-3xl shadow-2xl overflow-hidden flex flex-col h-[85vh] max-h-[750px]">
        
        <div className="absolute inset-0 z-0 opacity-40 pointer-events-none">
          <SoftAurora speed={0.4} scale={1.2} color1="#e0e7ff" color2="#fce7f3" />
        </div>

        <div className="relative z-10 flex flex-col h-full bg-white/60 backdrop-blur-md">
          <div className="px-8 py-6 border-b border-white/40 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl shadow-lg shadow-indigo-500/20">
                <Sparkles className="w-7 h-7 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-slate-800 tracking-tight">{modalTitle}</h2>
                <p className="text-sm font-medium text-indigo-600 flex items-center gap-2 mt-0.5">
                  <Loader2 className="w-4 h-4 animate-spin" /> Live Processing
                </p>
              </div>
            </div>
            <button onClick={onClose} className="text-slate-400 hover:text-slate-800 bg-white/50 hover:bg-white p-2 rounded-full transition-all">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="px-8 pt-4 pb-2">
            <div className="flex justify-between text-xs font-semibold text-slate-500 mb-2 uppercase tracking-wider">
              <span>Overall Progress</span>
              <span>{currentProgress}%</span>
            </div>
            <div className="h-2 w-full bg-indigo-100 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full transition-all duration-700 ease-out"
                style={{ width: `${currentProgress}%` }}
              ></div>
            </div>
          </div>

          <div ref={scrollRef} className="flex-1 p-6 sm:px-8 sm:pb-8 overflow-y-auto space-y-3 scroll-smooth">
            {userFriendlyLogs.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-slate-500 gap-3">
                <BrainCircuit className="w-10 h-10 animate-pulse text-indigo-400" />
                <p className="font-medium text-lg">Initializing AI Engines...</p>
              </div>
            ) : (
              userFriendlyLogs.map((log, index) => {
                const isLatest = index === userFriendlyLogs.length - 1;
                const isSuccessMsg = log.includes("✅") || log.includes("successfully") || log.includes("complete");
                const isWarningMsg = log.includes("⚠️") || log.includes("issue");

                return (
                  <div key={index} className={`flex items-start gap-4 p-4 rounded-2xl border transition-all duration-500 ${isLatest ? 'bg-white shadow-md border-indigo-200 translate-x-1 scale-[1.02]' : 'bg-white/50 border-transparent opacity-60 hover:opacity-100'}`}>
                    {isSuccessMsg ? <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" /> : isWarningMsg ? <BrainCircuit className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" /> : isLatest ? <Loader2 className="w-5 h-5 text-indigo-500 animate-spin shrink-0 mt-0.5" /> : <CheckCircle2 className="w-5 h-5 text-indigo-300 shrink-0 mt-0.5" />}
                    <p className={`text-[15px] leading-relaxed ${isLatest ? 'font-semibold text-slate-800' : 'font-medium text-slate-600'}`}>{log}</p>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AiProgressModal;