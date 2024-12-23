


import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import SearchFilter from '../components/SearchFilter';
import IncidentCard from '../components/IncidentCard';

function IncidentsPage() {
  const [incidents, setIncidents] = useState([]);
  const [pagination, setPagination] = useState({
    currentPage: 1,
    totalPages: 0,
    totalDocuments: 0
  });
  const [filters, setFilters] = useState({
    sector: '',
    threat_level: '',
    incident_type: ''
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchIncidents();
  }, [pagination.currentPage, filters]);

  const fetchIncidents = async () => {
    setLoading(true);
    try {
      const queryParams = new URLSearchParams({
        page: pagination.currentPage,
        limit: 10,
        ...filters
      }).toString();

      const response = await axios.get(`http://localhost:5000/api/incidents?${queryParams}`);
      
      setIncidents(response.data.incidents);
      setPagination(prev => ({
        ...prev,
        totalPages: response.data.totalPages,
        totalDocuments: response.data.totalDocuments
      }));
    } catch (error) {
      console.error('Error fetching incidents:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (pageNumber) => {
    setPagination(prev => ({ ...prev, currentPage: pageNumber }));
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    setPagination(prev => ({ ...prev, currentPage: 1 }));
  };

  return (
    <div className="container mx-auto px-4">
      <SearchFilter onFilterChange={handleFilterChange} />

      {loading ? (
        <div className="text-center py-8">Loading...</div>
      ) : (
        <>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            {incidents.map(incident => (
              <IncidentCard 
                key={incident._id} 
                incident={incident} 
                linkToDetails={true} 
              />
            ))}
          </div>

          <div className="flex justify-center items-center space-x-2 py-4">
            {Array.from({ length: pagination.totalPages }, (_, i) => i + 1).map(pageNumber => (
              <button
                key={pageNumber}
                onClick={() => handlePageChange(pageNumber)}
                className={`px-4 py-2 rounded ${
                  pageNumber === pagination.currentPage 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-200 text-gray-800'
                }`}
              >
                {pageNumber}
              </button>
            ))}
          </div>

          <div className="text-center text-gray-600 mt-2">
            Total Incidents: {pagination.totalDocuments}
          </div>
        </>
      )}
    </div>
  );
}

export default IncidentsPage;