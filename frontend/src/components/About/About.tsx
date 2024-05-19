import React from 'react';
import { Helmet } from 'react-helmet';
import './About.css'; // Ensure your CSS file is correctly linked

const About: React.FC = () => {
    return (
        <div className="container mt-5">
            <Helmet>
                <title>About Us - Kairos</title>
                <meta name="description" content="Learn more about Kairos. We specialize in providing high-quality services and products. Our team is dedicated to ensuring the best experience for our clients." />
                <meta name="keywords" content="Kairos, About Us, Services, Products, Mission, Vision, Values" />
            </Helmet>
            <h1>About Us</h1>
            <p>Welcome to our company. We specialize in providing high-quality services and products. Our team is dedicated to ensuring the best experience for our clients.</p>
            <p>Learn more about our mission, vision, and values on this page.</p>
        </div>
    );
}

export default About;
