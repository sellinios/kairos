import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import './Contact.css';

const Contact: React.FC = () => {
    const { t } = useTranslation('Contact'); // Specify the namespace

    return (
        <div className="contact-container">
            <Helmet>
                <title>{t('contactTitle')} - Kairos</title>
                <meta name="description" content={t('contactDescription')} />
                <meta name="keywords" content={t('contactKeywords')} />
            </Helmet>
            <h1 className="contact-title">{t('contactUs')}</h1>
            <p className="contact-text">{t('contactMessage')}</p>
        </div>
    );
}

export default Contact;
