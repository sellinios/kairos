// src/webVitals.js
import { onCLS, onFID, onLCP, onFCP, onTTFB, onINP } from 'web-vitals';

function sendToAnalytics({ name, delta, id }) {
  window.gtag('event', name, {
    event_category: 'Web Vitals',
    event_label: id, // id unique to current page load
    value: Math.round(name === 'CLS' ? delta * 1000 : delta), // values must be integers
    non_interaction: true, // avoids affecting bounce rate
  });
}

onCLS(sendToAnalytics);
onFID(sendToAnalytics);
onLCP(sendToAnalytics);
onFCP(sendToAnalytics);
onTTFB(sendToAnalytics);
onINP(sendToAnalytics);
