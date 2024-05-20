import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars, faTimes } from '@fortawesome/free-solid-svg-icons';
import 'bootstrap/dist/css/bootstrap.min.css';
import './NavigationMenu.css';

const NavigationMenu: React.FC = () => {
    const { t, i18n } = useTranslation('NavigationMenu'); // Specify the namespace
    const [isOpen, setIsOpen] = useState(false);

    const toggleMenu = () => {
        setIsOpen(!isOpen);
    };

    const changeLanguage = (lng: string) => {
        i18n.changeLanguage(lng);
        setIsOpen(false); // Close menu after language change
    };

    return (
        <div className="navigation-menu">
            <div className="menu-icon" onClick={toggleMenu}>
                <FontAwesomeIcon icon={isOpen ? faTimes : faBars} size="2x" />
            </div>
            {isOpen && (
                <div className="menu-content">
                    <div className="menu-header">
                        <div className="menu-close-icon" onClick={toggleMenu}>
                            <FontAwesomeIcon icon={faTimes} size="2x" />
                        </div>
                    </div>
                    <ul className="list-unstyled">
                        <li><Link to="/" onClick={toggleMenu}>{t('home')}</Link></li>
                        <li><Link to="/about" onClick={toggleMenu}>{t('about')}</Link></li>
                        <li><Link to="/contact" onClick={toggleMenu}>{t('contact')}</Link></li>
                        <li><Link to="/weather" onClick={toggleMenu}>{t('weather')}</Link></li>
                        <li><Link to="/aethra-weather-engine" onClick={toggleMenu}>{t('aethraWeatherEngine')}</Link></li>
                        <li><Link to="/aethra-geo-engine" onClick={toggleMenu}>{t('aethraGeoEngine')}</Link></li>
                        <li><a href="/privacy-policy" target="_blank" rel="noopener noreferrer">{t('privacyPolicy')}</a></li>
                    </ul>
                    <div className="language-selector">
                        <button onClick={() => changeLanguage('en')}>English</button>
                        <button onClick={() => changeLanguage('gr')}>Ελληνικά</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default NavigationMenu;
