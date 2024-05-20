import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import './PrivacyPolicy.css';

const PrivacyPolicy: React.FC = () => {
    const { t } = useTranslation('PrivacyPolicy'); // Specify the namespace

    return (
        <div className="privacy-container my-5">
            <Helmet>
                <title>{t('privacyPolicyTitle')} - Kairos</title>
                <meta name="description" content={t('privacyPolicyDescription')} />
                <meta name="keywords" content={t('privacyPolicyKeywords')} />
            </Helmet>
            <h1>{t('privacyPolicyTitle')}</h1>
            <div className="privacy-content" dangerouslySetInnerHTML={{ __html: t('privacyPolicyContent') }} />
        </div>
    );
};

export default PrivacyPolicy;
