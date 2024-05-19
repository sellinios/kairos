import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Footer.css';

const Footer: React.FC = () => {
    const { t } = useTranslation('Footer'); // Specify the namespace

    return (
        <footer className="footer bg-blue py-3">
            <Helmet>
                <title>{t('footerTitle')}</title>
                <meta name="description" content={t('footerDescription')} />
                <meta name="keywords" content={t('footerKeywords')} />
            </Helmet>
            <div className="container text-center">
                <p>&copy; {new Date().getFullYear()} {t('companyName')}</p>
            </div>
        </footer>
    );
}

export default Footer;
