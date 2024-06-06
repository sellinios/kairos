import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import './i18n';
import 'bootstrap/dist/css/bootstrap.min.css';
import './webVitals';

const rootElement = document.getElementById('root') as HTMLElement;
const root = ReactDOM.createRoot(rootElement);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

// Adding this export statement makes the file a module
export {};
