import React from 'react';
import { Download, BrainCircuit, FileText, Sparkles } from 'lucide-react';

const PapersTable = ({ papers, loading, onGenerateSolution, onCleanWatermark }) => {
  if (loading) {
    return (
      <div className="h-64 flex items-center justify-center text-slate-500 bg-white border border-slate-200 rounded-lg shadow-sm">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="font-medium">Loading papers...</p>
        </div>
      </div>
    );
  }

  if (!papers || papers.length === 0) {
    return (
      <div className="h-64 flex flex-col items-center justify-center text-slate-500 bg-white border border-slate-200 rounded-lg shadow-sm">
        <FileText className="w-10 h-10 mb-3 text-slate-300" />
        <p className="font-medium">No papers found.</p>
        <p className="text-sm">Try adjusting your search or filters.</p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-lg shadow-sm overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-600 whitespace-nowrap">
          <thead className="bg-slate-50 border-b border-slate-200 text-slate-700">
            <tr>
              <th className="px-5 py-3.5 font-semibold">Degree</th>
              <th className="px-5 py-3.5 font-semibold">Branch</th>
              <th className="px-5 py-3.5 font-semibold text-center">Sem</th>
              <th className="px-5 py-3.5 font-semibold">Subject</th>
              <th className="px-5 py-3.5 font-semibold">Code</th>
              <th className="px-5 py-3.5 font-semibold text-center">Year</th>
              <th className="px-5 py-3.5 font-semibold text-center">Month</th>
              <th className="px-5 py-3.5 font-semibold text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {papers.map((paper, index) => (
              <tr key={index} className="hover:bg-slate-50 transition-colors">
                <td className="px-5 py-3.5 uppercase font-medium text-slate-700">{paper.degree}</td>
                <td className="px-5 py-3.5 uppercase max-w-[150px] truncate" title={paper.branch}>{paper.branch}</td>
                <td className="px-5 py-3.5 text-center">{paper.semester}</td>
                <td className="px-5 py-3.5 font-medium text-blue-600 max-w-[250px] truncate" title={paper.subject_name}>{paper.subject_name}</td>
                <td className="px-5 py-3.5">{paper.subject_code}</td>
                <td className="px-5 py-3.5 text-center">{paper.year}</td>
                <td className="px-5 py-3.5 text-center uppercase">{paper.exam_month}</td>
                <td className="px-5 py-3.5 flex items-center justify-end gap-5">
                  
                  {/* Download Original */}
                  <a 
                    href={paper.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-slate-500 hover:text-blue-600 font-medium flex items-center gap-1.5 transition-colors"
                    title="Download Original"
                  >
                    <Download className="w-4 h-4" />
                  </a>
                  
                  {/* NEW: Watermark Removal Button */}
                  <button 
                    onClick={() => onCleanWatermark(paper.url)}
                    className="text-emerald-600 hover:text-emerald-800 font-medium flex items-center gap-1.5 transition-colors"
                    title="Remove Watermark"
                  >
                    <Sparkles className="w-4 h-4" /> Clean PDF
                  </button>

                  {/* AI Solution Button */}
                  <button 
                    onClick={() => onGenerateSolution(paper.url)}
                    className="text-indigo-600 hover:text-indigo-800 font-medium flex items-center gap-1.5 transition-colors"
                    title="Generate Solution using AI"
                  >
                    <BrainCircuit className="w-4 h-4" /> Solution
                  </button>

                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PapersTable;