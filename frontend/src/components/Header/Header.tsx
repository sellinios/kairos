import React from 'react';
import LanguageSelector from '../LanguageSelector/LanguageSelector';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Header.css';

const Header: React.FC = () => {
    const handleLocaleChange = (newLocale: string) => {
        console.log("Locale changed to:", newLocale);
    };

    const languages = [
        { code: 'en-US', label: 'English' },
        { code: 'gr', label: 'Greek' },
        // Add more languages here
        { code: 'es', label: 'Spanish' },
        { code: 'fr', label: 'French' },
    ];

    return (
        <header className="header bg-light py-3">
            <div className="container d-flex justify-content-between align-items-center">
                <div className="header__logo">
                    <h1 className="site-logo mb-0">Kairos</h1>
                    <h4 className="site-tagline mb-0">beta V1.0</h4>
                </div>
                <div className="header__language-selector">
                    <LanguageSelector setLocale={handleLocaleChange} languages={languages} />
                </div>
            </div>
        </header>
    );
};

export default Header;
