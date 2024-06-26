import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Header.css';
import SearchEngine from './Search/SearchEngine';

const Header: React.FC = () => {
    const { t } = useTranslation('Header'); // Specify the namespace

    return (
        <>
            <Helmet>
                <title>{t('appTitle')} - {t('home')}</title>
                <meta name="description" content={t('welcomeMessage')} />
                <meta name="keywords" content="Kairos, Search" />
            </Helmet>
            <header className="header py-2">
                <div className="container d-flex justify-content-between align-items-center">
                    <div className="header__logo d-flex align-items-center">
                        <span className="header__title">{t('appTitle')}</span>
                    </div>
                    <div className="header__search">
                        <SearchEngine />
                    </div>
                </div>
            </header>
        </>
    );
};

export default Header;
