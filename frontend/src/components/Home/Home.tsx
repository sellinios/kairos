import React from 'react';
import WeatherBlock from '../WeatherBlock/WeatherBlock';
import './Home.css';

interface HomeProps {
  location: string;
  locationData: Record<string, any>; // Or use your more detailed interface
}

const Home: React.FC<HomeProps> = ({ location, locationData }) => {
  return (
    <div className="container home-container">
      <WeatherBlock location={location} locationData={locationData} />
      <div className="home-content text-center">
        <h1 className="home-title">Welcome to the Home page!</h1>
        <p className="home-text">This is a simple homepage for our React application.</p>
        <button className="btn btn-primary home-button">Learn More</button>
      </div>
    </div>
  );
}

export default Home;
