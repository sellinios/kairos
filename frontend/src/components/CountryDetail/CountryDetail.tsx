import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getContinent, getCountriesInContinent, Continent, Country } from '../../services';

const CountryDetail: React.FC = () => {
  const { continentName } = useParams<{ continentName: string }>();
  const [continent, setContinent] = useState<Continent | null>(null);
  const [countries, setCountries] = useState<Country[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchContinentData = async () => {
      if (!continentName) {
        setError('Continent name is undefined');
        setLoading(false);
        return;
      }

      try {
        const continentData = await getContinent(continentName);
        setContinent(continentData);
        const countriesData = await getCountriesInContinent(continentName);
        setCountries(countriesData);
        setLoading(false);
      } catch (err) {
        console.error('Failed to fetch continent data:', err);
        setError('Failed to fetch continent data');
        setLoading(false);
      }
    };

    fetchContinentData();
  }, [continentName]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>{continent?.name}</h1>
      <ul>
        {countries && countries.map((country) => (
          <li key={country.id}>{country.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CountryDetail;
