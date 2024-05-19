import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import './About.css';

const About: React.FC = () => {
    const { t } = useTranslation('About'); // Specify the namespace

    return (
        <div className="container mt-5">
            <Helmet>
                <title>{t('aboutTitle')} - Kairos</title>
                <meta name="description" content={t('aboutDescription')} />
                <meta name="keywords" content={t('aboutKeywords')} />
            </Helmet>
            <h1>{t('aboutUs')}</h1>
            <p>{t('aboutWelcomeMessage')}</p>
            <p>{t('aboutMoreInfo')}</p>
        </div>
    );
}

export default About;
