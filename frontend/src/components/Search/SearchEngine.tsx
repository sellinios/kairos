import React, { useState } from 'react';
import './SearchEngine.css';

const SearchEngine: React.FC = () => {
    const [query, setQuery] = useState('');

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        console.log('Searching for:', query);
        // Add your search functionality here
    };

    return (
        <div className="search-engine-container">
            <form className="search-engine" onSubmit={handleSearch}>
                <input
                    type="text"
                    className="search-input"
                    placeholder="Search Your Place..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button type="submit" className="search-button">Search</button>
            </form>
        </div>
    );
};

export default SearchEngine;
