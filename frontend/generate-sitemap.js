const { SitemapStream, streamToPromise } = require('sitemap');
const { createWriteStream } = require('fs');
const path = require('path');
const fetch = require('node-fetch');

async function fetchData(endpoint, fallbackData) {
  try {
    const response = await fetch(endpoint);
    if (!response.ok) {
      throw new Error(`Failed to fetch data from ${endpoint}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching data from ${endpoint}:`, error);
    return fallbackData;
  }
}

async function generateSitemap() {
  // Fallback data
  const fallbackPlaces = [{ slug: 'place1' }, { slug: 'place2' }];
  const fallbackArticles = [{ slug: 'article1' }, { slug: 'article2' }];
  const fallbackContinents = [{ slug: 'continent1' }, { slug: 'continent2' }];
  const fallbackCountries = [
    { slug: 'greece', continentSlug: 'europe' },
    { slug: 'france', continentSlug: 'europe' }
  ];

  // Fetch dynamic data
  const places = await fetchData('https://kairos.gr/api/places', fallbackPlaces);
  const articles = await fetchData('https://kairos.gr/api/articles', fallbackArticles);
  const continents = await fetchData('https://kairos.gr/api/continents', fallbackContinents);
  const countries = await fetchData('https://kairos.gr/api/countries', fallbackCountries);

  // Map continent slugs to countries
  const continentMap = {};
  continents.forEach(continent => {
    continentMap[continent.id] = continent.slug;
  });

  countries.forEach(country => {
    if (continentMap[country.continent]) {
      country.continentSlug = continentMap[country.continent];
    } else {
      console.error(`Missing continentSlug for country: ${country.slug}`);
    }
  });

  const links = [
    { url: '/', changefreq: 'daily', priority: 1.0 },
    { url: '/about', changefreq: 'weekly', priority: 0.8 },
    { url: '/contact', changefreq: 'monthly', priority: 0.7 },
    { url: '/aethra-geo-engine', changefreq: 'monthly', priority: 0.7 },
    { url: '/privacy-policy', changefreq: 'monthly', priority: 0.7 },
  ];

  // Add dynamic routes
  places.forEach(place => {
    links.push({ url: `/place/${place.slug}`, changefreq: 'daily', priority: 0.9 });
    links.push({ url: `/weather/${place.slug}`, changefreq: 'daily', priority: 0.9 });
  });

  articles.forEach(article => {
    links.push({ url: `/articles/${article.slug}`, changefreq: 'weekly', priority: 0.8 });
  });

  continents.forEach(continent => {
    links.push({ url: `/geography/${continent.slug}`, changefreq: 'monthly', priority: 0.7 });
  });

  countries.forEach(country => {
    if (country.continentSlug) {
      links.push({ url: `/geography/${country.continentSlug}/${country.slug}`, changefreq: 'monthly', priority: 0.7 });
    }
  });

  const sitemap = new SitemapStream({ hostname: 'https://kairos.gr' });

  const writeStream = createWriteStream(path.join(__dirname, 'public', 'sitemap.xml'));
  sitemap.pipe(writeStream);

  links.forEach(link => sitemap.write(link));
  sitemap.end();

  writeStream.on('finish', () => {
    console.log('Sitemap generated successfully.');
  });
}

generateSitemap().catch(error => {
  console.error('Error generating sitemap:', error);
});
