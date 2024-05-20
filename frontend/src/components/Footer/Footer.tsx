import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Footer.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebook } from '@fortawesome/free-brands-svg-icons';

const Footer: React.FC = () => {
    const { t } = useTranslation('Footer'); // Specify the namespace

    return (
        <footer className="footer bg-dark text-white py-4">
            <Helmet>
                <title>{t('footerTitle')}</title>
                <meta name="description" content={t('footerDescription')} />
                <meta name="keywords" content={t('footerKeywords')} />
            </Helmet>
            <div className="container text-center">
                <nav className="footer-nav mb-3">
                    <ul className="list-inline">
                        <li className="list-inline-item"><a href="/about" className="text-white">{t('about')}</a></li>
                        <li className="list-inline-item"><a href="/contact" className="text-white">{t('contact')}</a></li>
                        <li className="list-inline-item"><a href="/weather" className="text-white">{t('weather')}</a></li>
                        <li className="list-inline-item"><a href="/aethra-weather-engine" className="text-white">{t('aethraWeatherEngine')}</a></li>
                        <li className="list-inline-item"><a href="/aethra-geo-engine" className="text-white">{t('aethraGeoEngine')}</a></li>
                        <li className="list-inline-item"><a href="/privacy-policy" className="text-white">{t('privacyPolicy')}</a></li>
                        <li className="list-inline-item">
                            <a href="https://www.facebook.com/Kairos.gr/" target="_blank" rel="noopener noreferrer" className="text-white">
                                <FontAwesomeIcon icon={faFacebook} /> {t('facebook')}
                            </a>
                        </li>
                    </ul>
                </nav>
                <p>&copy; {new Date().getFullYear()} {t('companyName')}</p>
            </div>
        </footer>
    );
}

export default Footer;
