// src/components/ContinentDetail/ContinentDetail.tsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getContinent, Continent } from '../../services/apiServiceGeography';

const ContinentDetail: React.FC = () => {
  const { continent } = useParams<{ continent: string }>();
  const [continentData, setContinentData] = useState<Continent | null>(null);

  useEffect(() => {
    if (continent) {
      getContinent(continent).then(response => {
        setContinentData(response);
      }).catch(error => {
        console.error("There was an error fetching the continent data!", error);
      });
    }
  }, [continent]);

  if (!continentData) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>{continentData.name}</h1>
      <h2>Countries:</h2>
      <ul>
        {continentData.countries.map(country => (
          <li key={country.id}>
            <h3>{country.name}</h3>
            {country.iso_alpha2 && <p>ISO Alpha-2: {country.iso_alpha2}</p>}
            {country.iso_alpha3 && <p>ISO Alpha-3: {country.iso_alpha3}</p>}
            {country.iso_numeric && <p>ISO Numeric: {country.iso_numeric}</p>}
            {country.capital && <p>Capital: {country.capital}</p>}
            {country.official_languages && <p>Languages: {country.official_languages}</p>}
            {country.currency && <p>Currency: {country.currency}</p>}
            {country.area && <p>Area: {country.area} sq km</p>}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ContinentDetail;
