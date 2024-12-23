// import React, { useState, useEffect } from 'react';
// import axios from 'axios';
// import IncidentDetails from './InDetails';

// const Home = () => {
//   const [recentIncidents, setRecentIncidents] = useState([]);
//   const [stats, setStats] = useState({
//     totalIncidents: 0,
//     criticalIncidents: 0,
//     unsolvedIncidents: 0,
//   });
//   const [isLoading, setIsLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     const fetchData = async () => {
//       try {
//         setIsLoading(true);

//         // Fetch recent incidents
//         const incidentsResponse = await axios.get('http://localhost:5000/api/incidents', {
//           params: { limit: 3 },
//         });

//         // Fetch statistics
//         const statsResponse = await axios.get('http://localhost:5000/api/incidents/stats/overview');

//         setRecentIncidents(incidentsResponse.data.incidents || []);
//         setStats(statsResponse.data);
//         setError(null);
//       } catch (error) {
//         console.error('Error fetching data:', error);
//         setError(error.message);
//         setRecentIncidents([]);
//       } finally {
//         setIsLoading(false);
//       }
//     };

//     fetchData();
//   }, []);

//   if (isLoading) {
//     return (
//       <div className="flex justify-center items-center min-h-screen">
//         <div className="spinner-border" role="status">
//           Loading...
//         </div>
//       </div>
//     );
//   }

//   if (error) {
//     return (
//       <div className="text-center text-red-500 p-8">
//         <h2>Error Loading Data</h2>
//         <p>{error}</p>
//       </div>
//     );
//   }

//   return (
//     <div className="container mx-auto px-4 py-8">
//       {/* Hero Section */}
//       <section className="text-center mb-8">
//         <h1 className="text-4xl font-bold text-blue-600 mb-4">
//           Stay Ahead of Cyber Threats in Indian Cyberspace
//         </h1>
//         <p className="text-gray-600 mb-6">
//           A platform for monitoring and reporting cyber threats in India.
//         </p>
//         <div>
//           <button className="bg-blue-600 text-white px-4 py-2 rounded mr-4">
//             View Dashboard
//           </button>
//           <button className="bg-gray-600 text-white px-4 py-2 rounded">
//             Report an Incident
//           </button>
//         </div>
//       </section>

//       {/* Statistics Section */}
//       <section className="mb-8">
//         <h2 className="text-2xl font-bold mb-4">Key Statistics</h2>
//         <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
//           <div className="bg-white shadow-md p-4 rounded">
//             <h3 className="text-xl font-bold">Total Incidents</h3>
//             <p className="text-gray-600 text-lg">{stats.totalIncidents}</p>
//           </div>
//           <div className="bg-white shadow-md p-4 rounded">
//             <h3 className="text-xl font-bold">Critical Incidents</h3>
//             <p className="text-gray-600 text-lg">{stats.criticalIncidents}</p>
//           </div>
//           <div className="bg-white shadow-md p-4 rounded">
//             <h3 className="text-xl font-bold">Unresolved Incidents</h3>
//             <p className="text-gray-600 text-lg">{stats.unsolvedIncidents}</p>
//           </div>
//         </div>
//       </section>

//       {/* Recent Incidents Section */}
//       <section>
//         <h2 className="text-2xl font-bold mb-6">Recent Cyber Incidents</h2>
//         {recentIncidents.length === 0 ? (
//           <p className="text-center text-gray-500">No recent incidents found</p>
//         ) : (
//           <div className="grid md:grid-cols-3 gap-6">
//             {recentIncidents.map((incident) => (
//               <IncidentDetails key={incident._id} incident={incident} />
//             ))}
//           </div>
//         )}
//       </section>
//     </div>
//   );
// };

// export default Home;




import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchRecentIncidents, fetchIncidentStats } from '../APIservice';
import IncidentCard from './IncidentCard';

function HomePage() {
  const [recentIncidents, setRecentIncidents] = useState([]);
  const [stats, setStats] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      const incidents = await fetchRecentIncidents(5);
      const incidentStats = await fetchIncidentStats();
      setRecentIncidents(incidents);
      setStats(incidentStats);
    };
    fetchData();
  }, []);

  return (
    <div className="space-y-8">
      <div className="bg-white shadow-md rounded-lg p-6">
        <h1 className="text-3xl font-bold text-cyber-blue mb-4">
          Cyber Incident Dashboard
        </h1>
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-blue-100 p-4 rounded-lg">
            <h3 className="font-semibold">Total Incidents</h3>
            <p className="text-2xl font-bold">{stats.totalIncidents || 0}</p>
          </div>
          <div className="bg-red-100 p-4 rounded-lg">
            <h3 className="font-semibold">Critical Incidents</h3>
            <p className="text-2xl font-bold">{stats.criticalIncidents || 0}</p>
          </div>
          <div className="bg-yellow-100 p-4 rounded-lg">
            <h3 className="font-semibold">Unsolved Incidents</h3>
            <p className="text-2xl font-bold">{stats.unsolvedIncidents || 0}</p>
          </div>
        </div>
      </div>

      <div className="bg-white shadow-md rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">Recent Incidents</h2>
          <Link 
            to="/incidents" 
            className="bg-cyber-blue text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            View All Incidents
          </Link>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {recentIncidents.map(incident => (
            <IncidentCard key={incident._id} incident={incident} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default HomePage;