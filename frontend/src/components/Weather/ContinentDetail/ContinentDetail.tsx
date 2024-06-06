import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getContinent, Continent } from '../../../services';
import { Helmet } from 'react-helmet';
import './ContinentDetail.css';

const ContinentDetail: React.FC = () => {
  const { continent } = useParams<{ continent: string }>();
  const [continentData, setContinentData] = useState<Continent | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (continent) {
      getContinent(continent)
        .then(response => {
          // Sort countries alphabetically by name
          response.countries.sort((a, b) => a.name.localeCompare(b.name));
          setContinentData(response);
          setError(null); // Clear any previous error
        })
        .catch(error => {
          console.error("There was an error fetching the continent data!", error);
          setError("There was an error fetching the continent data. Please try again later.");
        });
    }
  }, [continent]);

  if (error) {
    return <div>{error}</div>;
  }

  if (!continentData) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <Helmet>
        <title>{continentData.name} - Continent Details</title>
      </Helmet>
      <h1>{continentData.name}</h1>
      <h2>Countries:</h2>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Country</th>
              <th>ISO Alpha-2</th>
              <th>ISO Alpha-3</th>
              <th>ISO Numeric</th>
              <th>Capital</th>
              <th>Languages</th>
              <th>Currency</th>
              <th>Area (sq km)</th>
            </tr>
          </thead>
          <tbody>
            {continentData.countries.map(country => (
              <tr key={country.id}>
                <td>{country.name}</td>
                <td>{country.iso_alpha2 || '-'}</td>
                <td>{country.iso_alpha3 || '-'}</td>
                <td>{country.iso_numeric || '-'}</td>
                <td>{country.capital || '-'}</td>
                <td>{country.official_languages || '-'}</td>
                <td>{country.currency || '-'}</td>
                <td>{country.area ? `${country.area} sq km` : '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ContinentDetail;
