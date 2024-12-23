import React from 'react';
import { Link } from 'react-router-dom';
import { Shield } from 'lucide-react';

function Header() {
  return (
    <header className="bg-gradient-to-r from-cyber-blue to-blue-800 text-black font-semibold py-4 shadow-lg">
      <div className="container mx-auto px-4 flex justify-between items-center max-w-6xl">
        <Link 
          to="/" 
          className="text-2xl font-bold flex items-center group"
          aria-label="Cyber Incident Tracker Home"
        >
          <Shield 
            className="h-8 w-8 mr-3 text-black group-hover:rotate-6 transition-transform duration-300" 
            strokeWidth={2.5} 
          />
          <span className="tracking-tight group-hover:text-gray-200 transition-colors">
            Cyber Incident Tracker
          </span>
        </Link>
        <nav>
          <ul className="flex space-x-2">
            {[
              { to: '/', label: 'Home' },
              { to: '/incidents', label: 'Incidents' }
            ].map(({ to, label }) => (
              <li key={to}>
                <Link
                  to={to}
                  className="px-4 py-2 rounded-md transition-all duration-300 
                    hover:text-blue/20 
                    focus:outline-none 
                    focus:ring-2 
                    focus:ring-white/50
                    text-sm"
                >
                  {label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;