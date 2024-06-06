import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './SearchEngine.css';

const SearchEngine: React.FC = () => {
    const { t } = useTranslation('Search'); // Specify the namespace
    const [query, setQuery] = useState('');
    const navigate = useNavigate();

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        console.log('Searching for:', query);
        if (query.trim()) {
            navigate(`/place/${query.trim()}`);
        }
    };

    return (
        <div className="search-engine-container">
            <form className="search-engine" onSubmit={handleSearch}>
                <input
                    type="text"
                    className="search-input"
                    placeholder={t('searchPlaceholder')}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button type="submit" className="search-button">{t('searchButton')}</button>
            </form>
        </div>
    );
};

export default SearchEngine;
