import React from 'react';
import { Helmet } from 'react-helmet';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Footer.css';

const Footer: React.FC = () => {
  return (
    <footer className="footer bg-blue py-3">
      <Helmet>
        <title>Kairos - Quality Services and Products</title>
        <meta name="description" content="Kairos provides high-quality services and products. Connect with us to learn more." />
        <meta name="keywords" content="Kairos, Services, Products, Quality, Customer Service" />
      </Helmet>
      <div className="container text-center">
        <p>&copy; {new Date().getFullYear()} Kairos</p>
      </div>
    </footer>
  );
}

export default Footer;
