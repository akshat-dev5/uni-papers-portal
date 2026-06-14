import React, { useState, useCallback } from 'react';
import { BookOpen } from 'lucide-react';
import FilterSection from './components/FilterSection';
import PapersTable from './components/PapersTable';
import { getPapers } from './services/api';

function App() {
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);

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
          
          {/* Yahan humne count aur loading pass kar diya */}
          <FilterSection 
            onFilterChange={handleFilterChange} 
            totalCount={papers.length} 
            loading={loading}
          />

          <div className="mt-6">
            <PapersTable papers={papers} loading={loading} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;