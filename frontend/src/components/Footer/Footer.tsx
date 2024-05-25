import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Footer.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebook } from '@fortawesome/free-brands-svg-icons';
import { faInfoCircle, faEnvelope, faCloud, faMapMarkedAlt, faShieldAlt, faGlobe, faMap } from '@fortawesome/free-solid-svg-icons';

const Footer: React.FC = () => {
    const { t } = useTranslation('Footer'); // Specify the namespace

    return (
        <footer className="footer bg-dark text-white py-4">
            <Helmet>
                <title>{t('footerTitle')}</title>
                <meta name="description" content={t('footerDescription')} />
                <meta name="keywords" content={t('footerKeywords')} />
            </Helmet>
            <div className="container">
                <div className="row">
                    <div className="col-md-3">
                        <nav className="footer-nav mb-3">
                            <ul className="list-unstyled">
                                <li><Link to="/about" className="text-white"><FontAwesomeIcon icon={faInfoCircle} /> {t('about')}</Link></li>
                                <li><Link to="/contact" className="text-white"><FontAwesomeIcon icon={faEnvelope} /> {t('contact')}</Link></li>
                                <li><Link to="/weather" className="text-white"><FontAwesomeIcon icon={faCloud} /> {t('weather')}</Link></li>
                                <li><Link to="/privacy-policy" className="text-white"><FontAwesomeIcon icon={faShieldAlt} /> {t('privacyPolicy')}</Link></li>
                                <li>
                                    <a href="https://www.facebook.com/Kairos.gr/" target="_blank" rel="noopener noreferrer" className="text-white">
                                        <FontAwesomeIcon icon={faFacebook} /> {t('facebook')}
                                    </a>
                                </li>
                            </ul>
                        </nav>
                    </div>
                    <div className="col-md-3">
                        <nav className="footer-nav mb-3">
                            <h5 className="text-white">{t('aethraEngines')}</h5>
                            <ul className="list-unstyled">
                                <li><Link to="/aethra-weather-engine" className="text-white"><FontAwesomeIcon icon={faCloud} /> {t('aethraWeatherEngine')}</Link></li>
                                <li><Link to="/aethra-geo-engine" className="text-white"><FontAwesomeIcon icon={faMapMarkedAlt} /> {t('aethraGeoEngine')}</Link></li>
                            </ul>
                        </nav>
                    </div>
                    <div className="col-md-3">
                        <nav className="footer-nav mb-3">
                            <h5 className="text-white">{t('continents')}</h5>
                            <ul className="list-unstyled">
                                <li><Link to="/geography/europe" className="text-white"><FontAwesomeIcon icon={faGlobe} /> {t('europe')}</Link></li>
                                <li><Link to="/geography/asia" className="text-white"><FontAwesomeIcon icon={faGlobe} /> {t('asia')}</Link></li>
                                <li><Link to="/geography/africa" className="text-white"><FontAwesomeIcon icon={faGlobe} /> {t('africa')}</Link></li>
                                <li><Link to="/geography/north-america" className="text-white"><FontAwesomeIcon icon={faGlobe} /> {t('northAmerica')}</Link></li>
                                <li><Link to="/geography/south-america" className="text-white"><FontAwesomeIcon icon={faGlobe} /> {t('southAmerica')}</Link></li>
                                <li><Link to="/geography/oceania" className="text-white"><FontAwesomeIcon icon={faGlobe} /> {t('Oceania')}</Link></li>
                                <li><Link to="/geography/antarctica" className="text-white"><FontAwesomeIcon icon={faGlobe} /> {t('antarctica')}</Link></li>
                            </ul>
                        </nav>
                    </div>
                    <div className="col-md-3">
                        <nav className="footer-nav mb-3">
                            <h5 className="text-white">{t('regionsOfGreece')}</h5>
                            <ul className="list-unstyled">
                                <li><Link to="/geography/europe/greece/attica" className="text-white"><FontAwesomeIcon icon={faMap} /> {t('attica')}</Link></li>
                                <li><Link to="/geography/europe/greece/macedonia" className="text-white"><FontAwesomeIcon icon={faMap} /> {t('macedonia')}</Link></li>
                                <li><Link to="/geography/europe/greece/crete" className="text-white"><FontAwesomeIcon icon={faMap} /> {t('crete')}</Link></li>
                                <li><Link to="/geography/europe/greece/thessaly" className="text-white"><FontAwesomeIcon icon={faMap} /> {t('thessaly')}</Link></li>
                                <li><Link to="/geography/europe/greece/epirus" className="text-white"><FontAwesomeIcon icon={faMap} /> {t('epirus')}</Link></li>
                                <li><Link to="/geography/europe/greece/peloponnese" className="text-white"><FontAwesomeIcon icon={faMap} /> {t('peloponnese')}</Link></li>
                                <li><Link to="/geography/europe/greece/aegean" className="text-white"><FontAwesomeIcon icon={faMap} /> {t('aegean')}</Link></li>
                            </ul>
                        </nav>
                    </div>
                </div>
                <p className="text-center">&copy; {new Date().getFullYear()} {t('companyName')}</p>
            </div>
        </footer>
    );
}

export default Footer;
