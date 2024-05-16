import React, { useState } from 'react';
import './LanguageSelector.css'; // Make sure this path is correct

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
        <div className="languageSelector">
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
