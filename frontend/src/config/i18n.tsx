import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import HttpBackend from 'i18next-http-backend';
import config from './config'; // Ensure this path is correct

i18n
  .use(HttpBackend)
  .use(initReactI18next)
  .init({
    lng: config.defaultLanguage,
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
  });

export default i18n;
