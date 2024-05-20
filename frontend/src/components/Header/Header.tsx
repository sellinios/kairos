import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Header.css';
import SearchEngine from '../Search/SearchEngine';
import NavigationMenu from '../NavigationMenu/NavigationMenu';

const Header: React.FC = () => {
    const { t } = useTranslation('Header'); // Specify the namespace

    return (
        <>
            <Helmet>
                <title>{t('appTitle')} - {t('home')}</title>
                <meta name="description" content={t('welcomeMessage')} />
                <meta name="keywords" content="Kairos, Search" />
            </Helmet>
            <header className="header py-3">
                <div className="container d-flex justify-content-between align-items-center">
                    <div className="header__logo d-flex align-items-center">
                        <span className="header__title">{t('appTitle')}</span>
                    </div>
                    <NavigationMenu />
                </div>
                <div className="container d-flex justify-content-center mt-3">
                    <SearchEngine />
                </div>
            </header>
        </>
    );
};

export default Header;
