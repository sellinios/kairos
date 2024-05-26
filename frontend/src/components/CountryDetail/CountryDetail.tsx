import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getCountriesInContinent, Country } from '../../services/apiServiceGeography';

const CountryDetail: React.FC = () => {
  const { continent, country } = useParams<{ continent: string; country: string }>();
  const [countryDetail, setCountryDetail] = useState<Country | null>(null);

  useEffect(() => {
    const fetchCountryDetail = async () => {
      try {
        const countries = await getCountriesInContinent(continent || '');
        const selectedCountry = countries.find(c => c.slug === country);
        setCountryDetail(selectedCountry || null);
      } catch (error) {
        console.error('Error fetching country details:', error);
      }
    };

    fetchCountryDetail();
  }, [continent, country]);

  if (!countryDetail) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>{countryDetail.name}</h1>
      {/* Add more details about the country as needed */}
    </div>
  );
};

export default CountryDetail;
