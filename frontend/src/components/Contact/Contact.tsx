import React from 'react';
import { Helmet } from 'react-helmet';
import './Contact.css'; // Ensure the CSS file is correctly linked

function Contact() {
    return (
        <div className="contact-container">
            <Helmet>
                <title>Contact Us - Kairos</title>
                <meta name="description" content="Get in touch with us via email or phone. We look forward to hearing from you!" />
                <meta name="keywords" content="Kairos, Contact, Email, Phone, Customer Service" />
            </Helmet>
            <h1 className="contact-title">Contact Us</h1>
            <p className="contact-text">Please reach out to us via email or phone. We look forward to hearing from you!</p>
        </div>
    );
}

export default Contact;
