import { generate } from 'critical';
import fs from 'fs';
import path from 'path';

// Function to find the main CSS file with the hash in the filename
function findMainCss() {
  const cssDir = path.join('build', 'static', 'css');
  const files = fs.readdirSync(cssDir);
  const mainCssFile = files.find(file => file.startsWith('main') && file.endsWith('.css'));
  if (!mainCssFile) {
    throw new Error('Main CSS file not found');
  }
  return path.join('static', 'css', mainCssFile);
}

const mainCssPath = findMainCss();

generate({
  base: 'build/',
  src: 'index.html',
  target: {
    css: 'static/css/critical.css',
    html: 'index.html',
    uncritical: 'uncritical.css'
  },
  inline: true,
  extract: true,
  css: [mainCssPath], // Correct path to the CSS file
  dimensions: [
    { width: 375, height: 565 },   // Mobile
    { width: 1440, height: 900 }   // Desktop
  ],
}).then(({ css, html, uncritical }) => {
  console.log('Critical CSS generated successfully!');
}).catch(err => {
  console.error('Error generating critical CSS:', err);
});
