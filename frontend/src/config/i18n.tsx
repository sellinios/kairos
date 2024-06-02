// src/i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import HttpBackend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';
import config from './config'; // Ensure this path is correct

i18n
  .use(HttpBackend)
  .use(LanguageDetector) // Add language detector
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    debug: config.featureFlag,
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}/translation.json', // Adjusted to match your directory structure
    },
    ns: [
      'About', 'Contact', 'Footer', 'Header', 'Home', 'LanguageSelector',
      'LocationDisplay', 'LocationRequestModal', 'Login', 'NotFound',
      'PlaceDetail', 'Search', 'Weather'
    ],
    defaultNS: 'common',
    interpolation: {
      escapeValue: false,
    },
    detection: {
      // Order and from where user language should be detected
      order: ['querystring', 'cookie', 'localStorage', 'sessionStorage', 'navigator', 'htmlTag', 'path', 'subdomain'],

      // Keys or params to lookup language from
      lookupQuerystring: 'lng',
      lookupCookie: 'i18next',
      lookupLocalStorage: 'i18nextLng',
      lookupSessionStorage: 'i18nextLng',
      lookupFromPathIndex: 0,
      lookupFromSubdomainIndex: 0,

      // Cache user language on
      caches: ['localStorage', 'cookie'],
      excludeCacheFor: ['cimode'], // Languages to not persist (cookie, localStorage)
    },
  });

export default i18n;
