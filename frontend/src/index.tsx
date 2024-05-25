import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import './config/i18n';
import 'bootstrap/dist/css/bootstrap.min.css';
import './webVitals';
import ReactGA from 'react-ga4';

declare global {
  interface Window {
    dataLayer: any[];
    gtag: (...args: any[]) => void;
  }
}

// Google Analytics and AdSense initialization
if (process.env.NODE_ENV === 'production') {
  // Initialize Google Analytics 4
  ReactGA.initialize('G-80GYPERD24');

  // Load additional Google Analytics and AdSense scripts
  const loadScript = (src: string, onload?: () => void, crossorigin?: string) => {
    const script = document.createElement('script');
    script.async = true;
    script.src = src;
    if (crossorigin) {
      script.crossOrigin = crossorigin;
    }
    if (onload) {
      script.onload = onload;
    }
    document.head.appendChild(script);
  };

  loadScript('https://www.googletagmanager.com/gtag/js?id=G-80GYPERD24', () => {
    window.dataLayer = window.dataLayer || [];
    function gtag(...args: any[]) {
      window.dataLayer.push(args);
    }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', 'G-80GYPERD24', {
      'custom_map': {
        'dimension1': 'CLS',
        'dimension2': 'FID',
        'dimension3': 'LCP',
        'dimension4': 'FCP',
        'dimension5': 'TTFB',
        'dimension6': 'INP',
      }
    });
  });

  loadScript('https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3131616609445146', undefined, 'anonymous');
}

// Adding this export statement makes the file a module
export {};

const rootElement = document.getElementById('root') as HTMLElement;
const root = ReactDOM.createRoot(rootElement);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
