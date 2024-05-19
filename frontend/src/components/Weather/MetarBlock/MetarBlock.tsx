import React from 'react';
import './MetarBlock.css';

interface MetarData {
  station: string;
  metar_text: string;
  metar_timestamp: string;
}

interface MetarBlockProps {
  metarData: MetarData[];
}

const MetarBlock: React.FC<MetarBlockProps> = ({ metarData }) => {
  return (
    <div className="metar-block">
      <h2 className="text-center mb-4">METAR Data</h2>
      <table className="table table-hover">
        <thead className="thead-dark">
          <tr>
            <th>Station</th>
            <th>METAR Text</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {metarData.map((data, index) => (
            <tr key={index}>
              <td>{data.station}</td>
              <td>{data.metar_text}</td>
              <td>{new Date(data.metar_timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default MetarBlock;
