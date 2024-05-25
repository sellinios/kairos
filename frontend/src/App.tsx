import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
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
import NavigationMenu from './components/NavigationMenu/NavigationMenu'; // Import the NavigationMenu
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const App: React.FC = () => {
  return (
    <Router>
      <div className="App">
        <UpperHeader />
        <Header />
        <NavigationMenu /> {/* Add the NavigationMenu here */}
        <div className="container">
          <main className="content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/place/:placeName" element={<PlaceDetail />} />
              <Route path="/weather/:placeName" element={<WeatherDetail />} />
              <Route path="/aethra-geo-engine" element={<AethraGeoEngine />} />
              <Route path="/privacy-policy" element={<PrivacyPolicy />} />
              <Route path="/articles/:slug" element={<ArticleDetail />} />  {/* Use slug */}
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
        </div>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
