import React from 'react';
import { useTranslation } from 'react-i18next';
import './PrivacyPolicy.css';

const PrivacyPolicy: React.FC = () => {
    const { t } = useTranslation('PrivacyPolicy'); // Specify the namespace

    return (
        <div className="privacy-container my-5">
            <h1>{t('privacyPolicyTitle')}</h1>
            <div className="privacy-content" dangerouslySetInnerHTML={{ __html: t('privacyPolicyContent') }} />
        </div>
    );
};

export default PrivacyPolicy;
