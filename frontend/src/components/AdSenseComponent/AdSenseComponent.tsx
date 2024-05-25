// src/components/AdSenseComponent/AdSenseComponent.tsx
import React, { useEffect } from 'react';

// Extend the global Window interface
declare global {
  interface Window {
    adsbygoogle: { push: () => void }[];
  }
}

const AdSenseComponent: React.FC = () => {
  useEffect(() => {
    try {
      // Ensure window.adsbygoogle exists and has a push method
      window.adsbygoogle = window.adsbygoogle || [];
      // Push a new object that TypeScript will recognize
      (window.adsbygoogle as any).push({});
    } catch (e) {
      console.error('AdSense error:', e);
    }
  }, []);

  return (
    <ins className="adsbygoogle"
         style={{ display: 'block' }}
         data-ad-client="ca-pub-3131616609445146"
         data-ad-slot="YOUR_AD_SLOT"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
  );
};

export default AdSenseComponent;
