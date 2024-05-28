import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CookieConsent from 'react-cookie-consent';
import Home from './components/Home/Home';
import About from './components/About/About';
import Contact from './components/Contact/Contact';
import NotFound from './components/NotFound/NotFound';
import Footer from './components/Footer/Footer';
import PlaceDetail from './components/PlaceDetail/PlaceDetail';
import WeatherDetail from './components/Weather/WeatherDetail/WeatherDetail';
import AethraGeoEngine from './components/AethraGeoEngine/AethraGeoEngine';
import PrivacyPolicy from './components/PrivacyPolicy/PrivacyPolicy';
import Header from './components/Header/Header';
import UpperHeader from './components/UpperHeader/UpperHeader';
import ArticleDetail from './components/Blog/ArticleDetail/ArticleDetail';
import NavigationMenu from './components/NavigationMenu/NavigationMenu';
import ContinentDetail from './components/ContinentDetail/ContinentDetail';
import CountryDetail from './components/CountryDetail/CountryDetail';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const App: React.FC = () => {
    return (
        <Router>
            <div className="App">
                <UpperHeader />
                <Header />
                <NavigationMenu />
                <div className="container">
                    <main className="content">
                        <Routes>
                            <Route path="/" element={<Home />} />
                            <Route path="/about" element={<About />} />
                            <Route path="/contact" element={<Contact />} />
                            <Route path="/place/:placeName" element={<PlaceDetail />} />
                            <Route path="/weather/:continent/:country/:region/:municipality/:placeSlug" element={<WeatherDetail />} />
                            <Route path="/aethra-geo-engine" element={<AethraGeoEngine />} />
                            <Route path="/privacy-policy" element={<PrivacyPolicy />} />
                            <Route path="/articles/:slug" element={<ArticleDetail />} />
                            <Route path="/geography/:continent" element={<ContinentDetail />} />
                            <Route path="/geography/:continent/:country" element={<CountryDetail />} />
                            <Route path="*" element={<NotFound />} />
                        </Routes>
                    </main>
                </div>
                <Footer />
                <CookieConsent
                    location="bottom"
                    buttonText="I understand"
                    cookieName="mySiteCookieConsent"
                    style={{ background: "#2B373B" }}
                    buttonStyle={{ color: "#4e503b", fontSize: "13px" }}
                    expires={150}
                >
                    This website uses cookies to enhance the user experience. By continuing to browse the site, you consent to our use of cookies.
                </CookieConsent>
            </div>
        </Router>
    );
};

export default App;
