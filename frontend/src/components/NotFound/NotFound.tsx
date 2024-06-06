import React, { useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import './NotFound.css';

const NotFound: React.FC = () => {
  const { t, i18n } = useTranslation();

  useEffect(() => {
    // Force the language to Greek for testing
    i18n.changeLanguage('gr');
  }, [i18n]);

  return (
    <div className="not-found-container">
      <Helmet>
        <title>404 - {t('pageNotFoundTitle', 'Page Not Found')} - Kairos</title>
        <meta name="description" content={t('pageNotFoundDescription', 'The page you are looking for does not exist.')} />
        <meta name="keywords" content={t('pageNotFoundKeywords', '404, not found, error')} />
      </Helmet>
      <div className="not-found-content">
        <h1>404</h1>
        <p>{t('pageNotFoundMessage', 'The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.')}</p>
        <p className="motto">{t('pageNotFoundMotto', 'Disrupted by a thunderstorm or maybe the bad weather')}</p>
      </div>
    </div>
  );
};

export default NotFound;
