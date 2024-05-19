import React from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';

const NotFound: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div>
      <Helmet>
        <title>404 - {t('pageNotFoundTitle')} - Kairos</title>
        <meta name="description" content={t('pageNotFoundDescription')} />
        <meta name="keywords" content={t('pageNotFoundKeywords')} />
      </Helmet>
      <h1>404</h1>
      <p>{t('pageNotFoundMessage')}</p>
    </div>
  );
};

export default NotFound;
