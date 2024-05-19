import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Header.css';
import SearchEngine from '../Search/SearchEngine';
import logo from '../../assets/logo.png';  // Import the logo image

const Header: React.FC = () => {
    return (
        <header className="header bg-blue py-3">
            <div className="container d-flex justify-content-between align-items-center">
                <div className="header__logo d-flex align-items-center">
                    <img src={logo} alt="logo" className="logo-image" />  {/* Add the logo image */}
                </div>
            </div>
            <div className="container d-flex justify-content-center mt-3">
                <SearchEngine />
            </div>
        </header>
    );
};

export default Header;
