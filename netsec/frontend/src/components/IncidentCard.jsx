import React from 'react';
import { Link } from 'react-router-dom';

function IncidentCard({ incident, linkToDetails = false }) {
  const getThreatLevelColor = (level) => {
    switch (level) {
      case 'Critical': return 'bg-red-500 text-white';
      case 'High': return 'bg-yellow-500 text-white';
      case 'Medium': return 'bg-orange-500 text-white';
      default: return 'bg-green-500 text-white';
    }
  };

  const cardContent = (
    <div className="bg-white shadow-md rounded-lg p-4 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-lg font-semibold text-cyber-blue">
          {incident.Incident_ID}
        </h3>
        <span 
          className={`px-2 py-1 rounded text-xs ${getThreatLevelColor(incident.Threat_Level)}`}
        >
          {incident.Threat_Level}
        </span>
      </div>
      <div className="space-y-1">
        <p className="text-sm">
          <strong>Sector:</strong> {incident.Sector}
        </p>
        <p className="text-sm">
          <strong>Type:</strong> {incident.Incident_Type}
        </p>
        <p className="text-sm">
          <strong>Date:</strong> {new Date(incident.Date).toLocaleDateString()}
        </p>
        <p className="text-sm truncate">
          <strong>Description:</strong> {incident.Description}
        </p>
      </div>
      {linkToDetails && (
        <Link 
          to={`/incident/${incident._id}`} 
          className="mt-2 block text-center bg-cyber-blue text-black py-2 rounded hover:text-blue-800 transition-colors"
        >
          View Details
        </Link>
      )}
    </div>
  );

  return linkToDetails 
    ? cardContent 
    : (
      <Link to={`/incident/${incident._id}`}>
        {cardContent}
      </Link>
    );
}

export default IncidentCard;