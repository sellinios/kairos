import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header/Header';
import LocationDisplay from './components/LocationDisplay/LocationDisplay';
import Home from './components/Home/Home';
import About from './components/About/About';
import Contact from './components/Contact/Contact';
import NotFound from './components/NotFound/NotFound';
import Footer from './components/Footer/Footer';
import PlaceDetail from './components/PlaceDetail/PlaceDetail';
import WeatherDetail from './components/Weather/WeatherDetail/WeatherDetail';
import AethraGeoEngine from './components/AethraGeoEngine/AethraGeoEngine';
import PrivacyPolicy from './components/PrivacyPolicy/PrivacyPolicy';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const App: React.FC = () => {
  const [location, setLocation] = useState<string>('Locating...');
  const [latitude, setLatitude] = useState<number | null>(null);
  const [longitude, setLongitude] = useState<number | null>(null);

  const handleLocationUpdate = (location: string, latitude: number, longitude: number) => {
    setLocation(location);
    setLatitude(latitude);
    setLongitude(longitude);
  };

  return (
    <Router>
      <div className="App">
        <LocationDisplay onLocationUpdate={handleLocationUpdate} />
        <Header />
        <main className="pt-5 mt-5">
          <Routes>
            <Route
              path="/"
              element={
                latitude !== null && longitude !== null ? (
                  <Home latitude={latitude} longitude={longitude} location={location} />
                ) : (
                  <div>Loading location...</div>
                )
              }
            />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/place/:placeName" element={<PlaceDetail />} />
            <Route path="/weather/:placeName" element={<WeatherDetail />} />
            <Route path="/aethra-geo-engine" element={<AethraGeoEngine />} />
            <Route path="/privacy-policy" element={<PrivacyPolicy />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
