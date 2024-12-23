import React from 'react';

function Footer() {
  return (
    <footer className="bg-gray-800 text-white py-6">
      <div className="container mx-auto px-4 flex justify-between items-center">
        <div>
          <h3 className="text-lg font-bold">Cyber Incident Tracker</h3>
          <p className="text-sm text-gray-400">
            © {new Date().getFullYear()} Cyber Security Management System
          </p>
        </div>
        <div className="space-x-4">
          <a 
            href="#" 
            className="hover:text-cyber-blue transition-colors"
          >
            Privacy Policy
          </a>
          <a 
            href="#" 
            className="hover:text-cyber-blue transition-colors"
          >
            Terms of Service
          </a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;