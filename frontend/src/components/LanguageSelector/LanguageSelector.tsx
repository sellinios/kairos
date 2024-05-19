import React, { useState } from 'react';
import { Helmet } from 'react-helmet';
import './LanguageSelector.css'; // Ensure the CSS file is correctly linked

interface LanguageSelectorProps {
    setLocale: (language: string) => void;
    languages: { code: string; label: string }[];
}

const LanguageSelector: React.FC<LanguageSelectorProps> = ({ setLocale, languages }) => {
    const [selectedLanguage, setSelectedLanguage] = useState<string>(languages[0].code);

    const handleLanguageChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const newLanguage = event.target.value;
        setSelectedLanguage(newLanguage);
        setLocale(newLanguage);
    };

    return (
        <div className="language-selector">
            <Helmet>
                <title>Language Selector - Kairos</title>
                <meta name="description" content="Select your preferred language for the Kairos application." />
                <meta name="keywords" content="Kairos, language selector, translation, i18n" />
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
