import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getRegion } from '../../services/apiServiceGeography';

interface Region {
    id: number;
    name: string;
    description?: string; // Mark as optional
    // Add other fields as necessary
}

const RegionDetail: React.FC = () => {
    const { continent, region } = useParams<{ continent: string; region: string }>();
    const [regionData, setRegionData] = useState<Region | null>(null);

    useEffect(() => {
        if (continent && region) { // Ensure parameters are defined
            getRegion(continent, region).then(response => {
                setRegionData(response);
            }).catch(error => {
                console.error("There was an error fetching the region data!", error);
            });
        }
    }, [continent, region]);

    if (!regionData) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>{regionData.name}</h1>
            <p>{regionData.description}</p>
            {/* Render more details as necessary */}
        </div>
    );
};

export default RegionDetail;
