import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchIncidentDetails } from '../APIservice';

function IncidentDetailspage() {
  const [incident, setIncident] = useState(null);
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDetails = async () => {
      const details = await fetchIncidentDetails(id);
      setIncident(details);
    };
    fetchDetails();
  }, [id]);

  if (!incident) return <div>Loading...</div>;

  return (
    <div className="bg-white shadow-md rounded-lg p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-cyber-blue">
          Incident Details
        </h1>
        <button 
          onClick={() => navigate(-1)}
          className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300"
        >
          Back to Incidents
        </button>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <h2 className="text-xl font-semibold mb-4">Incident Overview</h2>
          <div className="space-y-2">
            <p><strong>Incident ID:</strong> {incident.Incident_ID}</p>
            <p><strong>Date:</strong> {new Date(incident.Date).toLocaleDateString()}</p>
            <p><strong>Platform:</strong> {incident.Platform}</p>
            <p><strong>Sector:</strong> {incident.Sector}</p>
            <p><strong>Incident Type:</strong> {incident.Incident_Type}</p>
            <p><strong>Location:</strong> {incident.Location}</p>
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4">Threat Assessment</h2>
          <div className="space-y-2">
            <p><strong>Threat Level:</strong> 
              <span className={`ml-2 px-2 py-1 rounded ${
                incident.Threat_Level === 'Critical' 
                  ? 'bg-red-500 text-white' 
                  : incident.Threat_Level === 'High'
                  ? 'bg-yellow-500 text-white'
                  : 'bg-green-500 text-white'
              }`}>
                {incident.Threat_Level}
              </span>
            </p>
            <p><strong>Solved:</strong> 
              <span className={`ml-2 ${
                incident.Incident_Solved 
                  ? 'text-green-600' 
                  : 'text-red-600'
              }`}>
                {incident.Incident_Solved ? 'Yes' : 'No'}
              </span>
            </p>
            <p><strong>Source:</strong> {incident.Source || 'Not specified'}</p>
          </div>
        </div>
      </div>

      <div className="mt-6">
        <h2 className="text-xl font-semibold mb-4">Detailed Description</h2>
        <p>{incident.Description}</p>

        <h3 className="text-lg font-semibold mt-4 mb-2">Summary</h3>
        <p className="bg-gray-100 p-4 rounded">{incident.Summary}</p>
      </div>
    </div>
  );
}

export default IncidentDetailspage;