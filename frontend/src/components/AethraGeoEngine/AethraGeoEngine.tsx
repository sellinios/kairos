import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import 'bootstrap/dist/css/bootstrap.min.css';
import './AethraGeoEngine.css';

interface SystemStats {
    countries: number;
    administrative_divisions: number;
    geographic_entities: number;
    places: number;
}

const AethraGeoEngine: React.FC = () => {
    const { t } = useTranslation('AethraGeoEngine'); // Specify the namespace
    const [stats, setStats] = useState<SystemStats | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [error, setError] = useState<string>('');

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await axios.get('/api/system-stats/');
                setStats(response.data);
            } catch (err) {
                console.error('Error fetching system stats:', err);
                setError(t('fetchError'));
            } finally {
                setIsLoading(false);
            }
        };

        fetchStats();
    }, [t]);

    if (isLoading) {
        return <div className="loading">{t('loading')}</div>;
    }

    if (error) {
        return <div className="error">{t('error')}: {error}</div>;
    }

    return (
        <div className="aethra-geo-engine-container">
            <Helmet>
                <title>{t('pageTitle')} - Kairos</title>
                <meta name="description" content={t('pageDescription')} />
                <meta name="keywords" content={t('pageKeywords')} />
            </Helmet>
            <div className="content text-center">
                <h1 className="title">{t('pageTitle')}</h1>
                <p className="description">
                    {t('pageDescription')}
                </p>
                <div className="stats row justify-content-center">
                    <div className="col-md-3">
                        <h3>{t('countries')}</h3>
                        <p>{stats?.countries}</p>
                    </div>
                    <div className="col-md-3">
                        <h3>{t('administrativeDivisions')}</h3>
                        <p>{stats?.administrative_divisions}</p>
                    </div>
                    <div className="col-md-3">
                        <h3>{t('geographicEntities')}</h3>
                        <p>{stats?.geographic_entities}</p>
                    </div>
                    <div className="col-md-3">
                        <h3>{t('places')}</h3>
                        <p>{stats?.places}</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AethraGeoEngine;
