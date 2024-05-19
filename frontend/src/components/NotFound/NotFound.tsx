import React from 'react';
import { Helmet } from 'react-helmet';

const NotFound = () => {
    return (
        <div>
            <Helmet>
                <title>404 - Page Not Found - Kairos</title>
                <meta name="description" content="The page you are looking for does not exist. Please check the URL or return to the homepage." />
                <meta name="keywords" content="404, Page Not Found, Kairos, error" />
            </Helmet>
            <h1>404</h1>
            <p>Page Not Found</p>
        </div>
    );
};

export default NotFound;
