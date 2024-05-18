import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import Header from './components/Header/Header';
import LocationDisplay from './components/LocationDisplay/LocationDisplay';
import Home from './components/Home/Home';
import About from './components/About/About';
import Contact from './components/Contact/Contact';
import NotFound from './components/NotFound/NotFound';
import Footer from './components/Footer/Footer';
import PlaceDetail from './components/PlaceDetail/PlaceDetail';
import WeatherDetail from './components/Weather/WeatherDetail/WeatherDetail';
import LocationRequestModal from './components/LocationRequestModal/LocationRequestModal';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const App: React.FC = () => {
  const [location, setLocation] = useState<string>('Locating...');
  const [latitude, setLatitude] = useState<number | null>(null);
  const [longitude, setLongitude] = useState<number | null>(null);
  const [showModal, setShowModal] = useState<boolean>(true);

  useEffect(() => {
    const storedConsent = localStorage.getItem('locationConsent');
    const storedLatitude = localStorage.getItem('latitude');
    const storedLongitude = localStorage.getItem('longitude');

    if (storedConsent && storedLatitude && storedLongitude) {
      setLatitude(Number(storedLatitude));
      setLongitude(Number(storedLongitude));
      fetchLocationData(Number(storedLatitude), Number(storedLongitude));
      setShowModal(false);
    } else {
      setShowModal(true);
    }
  }, []);

  const fetchLocationData = async (latitude: number, longitude: number) => {
    try {
      const locationResponse = await axios.get('/api/geography/places/nearest/', {
        params: { latitude, longitude }
      });
      console.log('Location response:', locationResponse.data);
      setLocation(locationResponse.data.name || 'Unknown Location');
    } catch (error) {
      console.error('Error fetching location data:', error);
      setLocation('Failed to fetch location');
    }
  };

  const handleAllowLocation = () => {
    setShowModal(false);
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setLatitude(latitude);
          setLongitude(longitude);
          fetchLocationData(latitude, longitude);
          localStorage.setItem('locationConsent', 'true');
          localStorage.setItem('latitude', latitude.toString());
          localStorage.setItem('longitude', longitude.toString());
        },
        (error) => {
          console.error('Geolocation error:', error);
          setLocation('Geolocation not supported');
        }
      );
    } else {
      setLocation('Geolocation not supported');
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setLocation('Location access denied');
  };

  return (
    <Router>
      <div className="App">
        <LocationRequestModal
          show={showModal}
          handleClose={handleCloseModal}
          handleAllow={handleAllowLocation}
        />
        <LocationDisplay location={location} />
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
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
