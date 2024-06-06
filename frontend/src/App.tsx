// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CookieConsent from 'react-cookie-consent';
import Home from './components/Home/Home';
import About from './components/Footer/About/About';
import Contact from './components/Footer/Contact/Contact';
import NotFound from './components/NotFound/NotFound';
import Footer from './components/Footer/Footer';
import PlaceDetail from './components/Weather/PlaceDetail/PlaceDetail';
import WeatherPage from './components/Weather/WeatherPage/WeatherPage';
import AethraGeoEngine from './components/Footer/AethraGeoEngine/AethraGeoEngine';
import AethraWeatherEngine from './components/Footer/AethraWeatherEngine/AethraWeatherEngine';
import PrivacyPolicy from './components/Footer/PrivacyPolicy/PrivacyPolicy';
import Header from './components/Header/Header';
import UpperHeader from './components/Header/UpperHeader/UpperHeader';
import NavigationMenu from './components/NavigationMenu/NavigationMenu';
import ArticleDetail from './components/Blog/ArticleDetail/ArticleDetail';
import ContinentDetail from './components/Weather/ContinentDetail/ContinentDetail';
import CountryDetail from './components/CountryDetail/CountryDetail';
import PlaceList from './components/Weather/PlaceList/PlaceList';
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
              <Route path="/weather/:continent/:country/:region/:subregion/:city" element={<WeatherPage />} />
              <Route path="/aethra-geo-engine" element={<AethraGeoEngine />} />
              <Route path="/aethra-weather-engine" element={<AethraWeatherEngine />} />
              <Route path="/privacy-policy" element={<PrivacyPolicy />} />
              <Route path="/articles/:slug" element={<ArticleDetail />} />
              <Route path="/geography/:continent" element={<ContinentDetail />} />
              <Route path="/geography/:continent/:country" element={<CountryDetail />} />
              <Route path="/places" element={<PlaceList />} />
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
