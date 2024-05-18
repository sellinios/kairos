import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Header.css';
import SearchEngine from '../Search/SearchEngine';

const Header: React.FC = () => {
    return (
        <header className="header bg-blue py-3">
            <div className="container d-flex justify-content-between align-items-center">
                <div className="header__logo">
                    <h1 className="site-logo mb-0">Kairos</h1>
                    <h2 className="site-tagline mb-0">beta V1.0</h2> {/* Changed from h4 to h2 */}
                </div>
            </div>
            <div className="container d-flex justify-content-center mt-3">
                <SearchEngine />
            </div>
        </header>
    );
};

export default Header;
