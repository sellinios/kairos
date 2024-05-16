import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Footer.css';

const Footer: React.FC = () => {
  return (
    <footer className="footer bg-dark text-white py-3">
      <div className="container text-center">
        <p>&copy; {new Date().getFullYear()} Kairos</p>
      </div>
    </footer>
  );
}

export default Footer;
