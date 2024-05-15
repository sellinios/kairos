import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import './config/i18n'; // Ensure this import is correctly handling i18n setup
import 'bootstrap/dist/css/bootstrap.min.css'; // Bootstrap CSS import

const rootElement = document.getElementById('root') as HTMLElement;
const root = ReactDOM.createRoot(rootElement);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
