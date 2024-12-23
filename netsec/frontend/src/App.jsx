


// import React from 'react';
// import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import Home from './components/Home.jsx';
// import Dashboard from './components/Dashboard';
// import ReportsInsights from './components/Reports&insights.jsx';
// import Tools from './components/Tools';
// import InDetails from './components/InDetails';
// import About from './components/About';
// import InDetailsPage from './components/InDetailsPage.jsx';


// const App = () => {
//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={<Home />} />
//         <Route path="/dashboard" element={<Dashboard />} />
//         <Route path="/reports-insights" element={<ReportsInsights />} />
//         <Route path="/tools" element={<Tools />} />
//         <Route path="/incident/:id" element={<InDetails />} />
//         <Route path="/about" element={<About />} />
//         <Route path="/incident/:id" element={<InDetailsPage />} />
//       </Routes>
//     </Router>
//   );
// };

// export default App;


import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './components/Home';
import IncidentsPage from './components/IncidentsPage';
import IncidentDetailsPage from './components/IncidentDetailspage';

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen bg-gray-100">
        <Header />
        <main className="flex-grow container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/incidents" element={<IncidentsPage />} />
            <Route path="/incident/:id" element={<IncidentDetailsPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;