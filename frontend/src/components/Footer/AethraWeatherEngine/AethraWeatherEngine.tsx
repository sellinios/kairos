import React, { useState, useEffect, useTransition } from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import './AethraWeatherEngine.css';

const AethraWeatherEngine: React.FC = () => {
    const { t, i18n } = useTranslation('AethraWeatherEngine'); // Specify the namespace
    const [isPending, startTransition] = useTransition();
    const [translationsLoaded, setTranslationsLoaded] = useState(false);

    useEffect(() => {
        startTransition(() => {
            i18n.loadNamespaces('AethraWeatherEngine').then(() => {
                setTranslationsLoaded(true);
            });
        });
    }, [i18n]);

    if (!translationsLoaded) {
        return <div>Loading...</div>; // Show a loading indicator while translations are loading
    }

    return (
        <div className="aethra-weather-engine-container">
            <Helmet>
                <title>{t('pageTitle')} - Kairos</title>
                <meta name="description" content={t('pageDescription')} />
                <meta name="keywords" content={t('pageKeywords')} />
            </Helmet>
            <h1>{t('pageTitle')}</h1>
            <div className="aethra-weather-engine-content">
                <p>{t('pageDescription')}</p>
                <div className="article">
                    <h2>{t('introducingWeatherEngine')}</h2>
                    <p>{t('weatherImportance')}</p>
                    <h3>{t('whatIsWeatherEngine')}</h3>
                    <p>{t('weatherEngineDescription')}</p>
                    <h3>{t('keyFeatures')}</h3>
                    <ul>
                        <li>{t('comprehensiveData')}</li>
                        <li>{t('accurateForecasts')}</li>
                        <li>{t('userFriendlyInterface')}</li>
                        <li>{t('realTimeUpdates')}</li>
                        <li>{t('customizableAlerts')}</li>
                    </ul>
                    <h3>{t('howItWorks')}</h3>
                    <ul>
                        <li>{t('dataCollection')}</li>
                        <li>{t('dataProcessing')}</li>
                        <li>{t('dataPresentation')}</li>
                    </ul>
                    <h3>{t('exampleUseCase')}</h3>
                    <p>{t('useCaseDescription')}</p>
                    <h3>{t('gettingStarted')}</h3>
                    <ol>
                        <li>{t('visitWebsite')}</li>
                        <li>{t('createAccount')}</li>
                        <li>{t('exploreData')}</li>
                        <li>{t('setUpAlerts')}</li>
                    </ol>
                    <h3>{t('conclusion')}</h3>
                    <p>{t('conclusionMessage')}</p>
                </div>
            </div>
        </div>
    );
};

export default AethraWeatherEngine;
