import React, { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { 
  getDegrees, 
  getBranches, 
  getSemesters, 
  getYearsAndMonths 
} from '../services/api';

const FilterSection = ({ onFilterChange, totalCount, loading }) => {
  const university = 'abvv';

  const [degrees, setDegrees] = useState([]);
  const [branches, setBranches] = useState([]);
  const [semesters, setSemesters] = useState([]);
  const [years, setYears] = useState([]);
  const [months, setMonths] = useState([]);

  const [selectedDegree, setSelectedDegree] = useState('');
  const [selectedBranch, setSelectedBranch] = useState('');
  const [selectedSemester, setSelectedSemester] = useState('');
  const [selectedYear, setSelectedYear] = useState('');
  const [selectedMonth, setSelectedMonth] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    if (onFilterChange) {
      onFilterChange({
        university,
        degree: selectedDegree,
        branch: selectedBranch,
        semester: selectedSemester,
        year: selectedYear,
        month: selectedMonth,
        search: searchQuery
      });
    }
  }, [selectedDegree, selectedBranch, selectedSemester, selectedYear, selectedMonth, searchQuery, onFilterChange]);

  useEffect(() => {
    const fetchInitial = async () => {
      try {
        const [degRes, branchRes, semRes, ymRes] = await Promise.all([
          getDegrees(university),
          getBranches(university, ''),
          getSemesters(university, '', ''),
          getYearsAndMonths(university)
        ]);
        setDegrees(degRes.data);
        setBranches(branchRes.data);
        setSemesters(semRes.data);
        setYears(ymRes.data.years);
        setMonths(ymRes.data.months);
      } catch (error) {
        console.error("Initial fetch error:", error);
      }
    };
    fetchInitial();
  }, []);

  useEffect(() => {
    getBranches(university, selectedDegree).then(res => setBranches(res.data));
  }, [selectedDegree]);

  useEffect(() => {
    getSemesters(university, selectedDegree, selectedBranch).then(res => setSemesters(res.data));
  }, [selectedDegree, selectedBranch]);

  return (
    <div className="space-y-5 mb-8">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
        <input 
          type="text" 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search by subject, code, year..." 
          className="w-full pl-10 pr-4 py-2.5 text-slate-700 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow bg-white shadow-sm"
        />
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        <select 
          value={selectedDegree} 
          onChange={(e) => setSelectedDegree(e.target.value)}
          className="w-full border border-slate-200 text-slate-700 rounded-md px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm cursor-pointer uppercase"
        >
          <option value="">All Degrees</option>
          {degrees.map((deg, i) => <option key={i} value={deg}>{deg}</option>)}
        </select>
        
        <select 
          value={selectedBranch}
          onChange={(e) => setSelectedBranch(e.target.value)}
          className="w-full border border-slate-200 text-slate-700 rounded-md px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm cursor-pointer uppercase truncate"
        >
          <option value="">All Branches</option>
          {branches.map((br, i) => <option key={i} value={br}>{br}</option>)}
        </select>
        
        <select 
          value={selectedSemester}
          onChange={(e) => setSelectedSemester(e.target.value)}
          className="w-full border border-slate-200 text-slate-700 rounded-md px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm cursor-pointer"
        >
          <option value="">All Semesters</option>
          {semesters.map((sem, i) => <option key={i} value={sem}>Semester {sem}</option>)}
        </select>
        
        <select 
          value={selectedYear}
          onChange={(e) => setSelectedYear(e.target.value)}
          className="w-full border border-slate-200 text-slate-700 rounded-md px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm cursor-pointer"
        >
          <option value="">All Years</option>
          {years.map((yr, i) => <option key={i} value={yr}>{yr}</option>)}
        </select>
        
        <select 
          value={selectedMonth}
          onChange={(e) => setSelectedMonth(e.target.value)}
          className="w-full border border-slate-200 text-slate-700 rounded-md px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm cursor-pointer uppercase"
        >
          <option value="">All Months</option>
          {months.map((m, i) => <option key={i} value={m}>{m}</option>)}
        </select>
      </div>

      <div className="text-sm text-slate-500">
        Showing <span className="font-semibold text-slate-700">{loading ? '...' : totalCount}</span> papers
      </div>
    </div>
  );
};

export default FilterSection;