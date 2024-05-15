// src/config/i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import HttpBackend from 'i18next-http-backend'; // import the backend plugin

i18n
  .use(HttpBackend) // activate the backend plugin
  .use(initReactI18next) // pass i18n instance to react-i18next module.
  .init({
    lng: 'en', // initial language to use
    fallbackLng: 'en', // fallback language when resource is not available
    debug: true, // enable debugging to see logs in the console
    backend: {
      // path to load the translation files from
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },
    interpolation: {
      escapeValue: false, // not needed for React as it escapes by default
    },
  });

export default i18n;
