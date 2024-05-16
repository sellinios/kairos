import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header/Header';
import LocationDisplay from './components/LocationDisplay/LocationDisplay';
import Home from './components/Home/Home';
import About from './components/About/About';
import Contact from './components/Contact/Contact';
import NotFound from './components/NotFound/NotFound';
import Footer from './components/Footer/Footer';
import './App.css';

const App: React.FC = () => {
  const [location, setLocation] = useState<string>('Locating...');
  const [locationData, setLocationData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchLocationData = async (latitude: number, longitude: number) => {
      try {
        setIsLoading(true);
        const locationResponse = await axios.get('/api/geography/places/nearest/', {
          params: { latitude, longitude }
        });
        setLocation(locationResponse.data.name);

        const weatherResponse = await axios.get('/api/weather/', {
          params: { latitude, longitude }
        });
        setLocationData(weatherResponse.data.forecasts);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching location or weather data:', error);
        setError('Failed to fetch data');
        setIsLoading(false);
      }
    };

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          fetchLocationData(latitude, longitude);
        },
        (error) => {
          console.error('Geolocation error:', error);
          setLocation('Geolocation not supported');
          setError('Geolocation not supported');
          setIsLoading(false);
        }
      );
    } else {
      setLocation('Geolocation not supported');
      setError('Geolocation not supported');
      setIsLoading(false);
    }
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <Router>
      <div className="App">
        <LocationDisplay location={location} />
        <Header />
        <main className="pt-5 mt-5">
          <Routes>
            <Route path="/" element={<Home location={location} locationData={locationData} />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
