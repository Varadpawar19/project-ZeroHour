import React, { useState } from 'react';

function SearchFilter({ onFilterChange }) {
  const [filters, setFilters] = useState({
    sector: '',
    threat_level: '',
    incident_type: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    const newFilters = { ...filters, [name]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4">Search & Filter Incidents</h2>
      <div className="grid md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Sector</label>
          <select
            name="sector"
            value={filters.sector}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200"
          >
            <option value="">All Sectors</option>
            <option value="Finance">Finance</option>
            <option value="Healthcare">Healthcare</option>
            <option value="Government">Government</option>
            <option value="Technology">Technology</option>
            <option value="Education">Education</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Threat Level</label>
          <select
            name="threat_level"
            value={filters.threat_level}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200"
          >
            <option value="">All Threat Levels</option>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Incident Type</label>
          <select
            name="incident_type"
            value={filters.incident_type}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200"
          >
            <option value="">All Incident Types</option>
            <option value="Malware">Malware</option>
            <option value="Phishing">Phishing</option>
            <option value="Data Breach">Data Breach</option>
            <option value="Network Intrusion">Network Intrusion</option>
            <option value="Social Engineering">Social Engineering</option>
            <option value="Ransomware">Ransomware</option>
            <option value="DDoS Attack">DDoS Attack</option>
          </select>
        </div>
      </div>
    </div>
  );
}

export default SearchFilter;