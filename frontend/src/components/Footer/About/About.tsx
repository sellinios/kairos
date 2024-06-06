// src/components/About.tsx
import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import './About.css';

const About: React.FC = () => {
    const { t } = useTranslation('About'); // Specify the namespace

    return (
        <div className="about-container">
            <Helmet>
                <title>{t('aboutTitle')} - Kairos</title>
                <meta name="description" content={t('aboutDescription')} />
                <meta name="keywords" content={t('aboutKeywords')} />
            </Helmet>
            <h1>{t('aboutUs')}</h1>
            <div className="about-content">
                <p>{t('aboutWelcomeMessage')}</p>
                <p>{t('aboutMoreInfo')}</p>
            </div>
        </div>
    );
}

export default About;
