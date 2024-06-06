import React, { useEffect, useState } from 'react';
import { fetchPlaceList, Place } from '../../../services';

const PlaceList: React.FC = () => {
  const [places, setPlaces] = useState<Place[]>([]);

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        const places = await fetchPlaceList();
        setPlaces(places);
      } catch (error) {
        console.error('Error fetching places:', error);
      }
    };

    fetchPlaces();
  }, []);

  return (
    <div>
      <h1>Place List</h1>
      <ul>
        {places.map(place => (
          <li key={place.id}>{place.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default PlaceList;
