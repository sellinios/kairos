import React, { useState } from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import './LanguageSelector.css'; // Ensure the CSS file is correctly linked

interface LanguageSelectorProps {
    setLocale: (language: string) => void;
    languages: { code: string; label: string }[];
}

const LanguageSelector: React.FC<LanguageSelectorProps> = ({ setLocale, languages }) => {
    const { t } = useTranslation('LanguageSelector'); // Specify the namespace
    const [selectedLanguage, setSelectedLanguage] = useState<string>(languages[0].code);

    const handleLanguageChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const newLanguage = event.target.value;
        setSelectedLanguage(newLanguage);
        setLocale(newLanguage);
    };

    return (
        <div className="language-selector">
            <Helmet>
                <title>{t('languageSelectorTitle')} - Kairos</title>
                <meta name="description" content={t('languageSelectorDescription')} />
                <meta name="keywords" content={t('languageSelectorKeywords')} />
            </Helmet>
            <select value={selectedLanguage} onChange={handleLanguageChange} className="custom-select">
                {languages.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                        {lang.label}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default LanguageSelector;
